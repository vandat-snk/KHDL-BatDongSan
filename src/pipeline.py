"""Reproducible, auditable analysis of the published Chotot listing snapshot.

Run from the repository root: python src/pipeline.py
Only five top-level source fields are trusted. Detail fields show possible scraper
carryover and are deliberately not used. Raw data is read, never overwritten.
All prices are advertised prices, not observed transaction prices.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sqlite3
import statistics
import sys
import tempfile
import time
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))
from artifact_contract import CORE_CODE, file_sha256, read_verified_source
from source_checks import check_source_consistency
SEED = 20261015
CORE_FIELDS = ("title", "price", "area", "location", "description")
TYPE_LABELS = {"land": "Đất", "house": "Nhà", "apartment": "Căn hộ", "other_unknown": "Khác / chưa rõ"}
COLORS = ["#187D8D", "#EB9E37", "#6873AD", "#BA5F70", "#62A384"]
# Historical locality labels in this 2021 snapshot, not present-day boundaries.
PROVINCES_2021 = """An Giang|Bà Rịa - Vũng Tàu|Bắc Giang|Bắc Kạn|Bạc Liêu|Bắc Ninh|Bến Tre|Bình Định|Bình Dương|Bình Phước|Bình Thuận|Cà Mau|Cần Thơ|Cao Bằng|Đà Nẵng|Đắk Lắk|Đắk Nông|Điện Biên|Đồng Nai|Đồng Tháp|Gia Lai|Hà Giang|Hà Nam|Hà Nội|Hà Tĩnh|Hải Dương|Hải Phòng|Hậu Giang|Hòa Bình|Hưng Yên|Khánh Hòa|Kiên Giang|Kon Tum|Lai Châu|Lâm Đồng|Lạng Sơn|Lào Cai|Long An|Nam Định|Nghệ An|Ninh Bình|Ninh Thuận|Phú Thọ|Phú Yên|Quảng Bình|Quảng Nam|Quảng Ngãi|Quảng Ninh|Quảng Trị|Sóc Trăng|Sơn La|Tây Ninh|Thái Bình|Thái Nguyên|Thanh Hóa|Thừa Thiên Huế|Tiền Giang|Tp Hồ Chí Minh|Trà Vinh|Tuyên Quang|Vĩnh Long|Vĩnh Phúc|Yên Bái""".split("|")


def normalize(value: object) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", str(value or ""))).strip().casefold()


def parse_location(text: object) -> tuple[str, str, list[str]]:
    """Validate only explicit province/district tokens; never infer from a street."""
    parts = [part.strip() for part in str(text or "").split(",") if part.strip()]
    canonical = {normalize(name): name for name in PROVINCES_2021}
    aliases = {"hcm": "Tp Hồ Chí Minh", "tp hcm": "Tp Hồ Chí Minh", "tp.hcm": "Tp Hồ Chí Minh", "hồ chí minh": "Tp Hồ Chí Minh", "tp hồ chí minh": "Tp Hồ Chí Minh"}
    last = normalize(parts[-1]).rstrip(". ") if parts else ""
    last = re.sub(r"^tỉnh\s+", "", last)
    province = canonical.get(last, aliases.get(last, "Chưa xác định"))
    flags = []
    if province == "Chưa xác định":
        flags.append("unknown_province")
    elif parts and normalize(parts[-1]) != normalize(province):
        flags.append("province_alias_normalized")
    district = "Chưa xác định"
    if province != "Chưa xác định" and len(parts) >= 2:
        candidate = parts[-2]
        if re.match(r"^(quận|huyện|thị xã|thành phố|tp\.?\s)\b", normalize(candidate)):
            district = candidate
    if district == "Chưa xác định":
        flags.append("unknown_district")
    return province, district, flags


def parse_number(text: str) -> tuple[float, list[str]]:
    """Vietnamese numeric notation: comma decimal, dot grouping if groups of 3.

    A single dot with 3 trailing digits is flagged because without source locale
    it can be ambiguous. We follow the source's observed Vietnamese convention;
    the uncertainty is preserved and a sensitivity table excludes these rows.
    """
    value = text.strip().replace(" ", "")
    if not re.fullmatch(r"[+-]?\d+(?:[.,]\d+)*", value):
        raise ValueError("invalid_number")
    flags = []
    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            if not re.fullmatch(r"[+-]?\d{1,3}(?:\.\d{3})+,\d+", value):
                raise ValueError("invalid_mixed_number_grouping")
            value = value.replace(".", "").replace(",", ".")
        else:
            # Accept standard international mixed notation only when grouping is clear.
            if not re.fullmatch(r"[+-]?\d{1,3}(?:,\d{3})+\.\d+", value):
                raise ValueError("invalid_mixed_number_grouping")
            value = value.replace(",", "")
            flags.append("international_number_format")
    elif "," in value:
        if value.count(",") != 1:
            raise ValueError("ambiguous_comma_number")
        value = value.replace(",", ".")
    elif "." in value:
        parts = value.lstrip("+-").split(".")
        if len(parts) > 1 and len(parts[0]) <= 3 and all(len(x) == 3 for x in parts[1:]) and parts[0] != "0":
            if len(parts) == 2:
                flags.append("dot_thousands_convention")
            value = value.replace(".", "")
        elif len(parts) > 2:
            raise ValueError("ambiguous_dot_number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("nonfinite_number")
    return number, flags


def parse_area(text: object) -> tuple[float | None, list[str]]:
    value = normalize(text)
    # Leading '-' in the source is a separator (e.g. '- 100 m2'), not negative area.
    value = re.sub(r"^\s*-\s+", "", value)
    if re.search(r"\d\s*[-–]\s*\d[\d.,]*\s*(?:m2|m\^2|ha)\b", value):
        return None, ["ambiguous_area_range"]
    matches = re.findall(r"([+-]?\d+(?:[.,]\d+)*)\s*(m2|m\^2|ha)\b", value)
    if len(matches) != 1:
        return None, ["missing_or_ambiguous_area"]
    try:
        area, flags = parse_number(matches[0][0])
    except ValueError as exc:
        return None, [str(exc)]
    if matches[0][1] == "ha":
        area *= 10000
        flags.append("area_ha_to_m2")
    if area <= 0:
        return None, flags + ["nonpositive_area"]
    return area, flags


def parse_price(text: object, area: float | None = None) -> tuple[float | None, str, list[str]]:
    value = normalize(text).replace("giá tốt", "").strip()
    # Remove only a labelled area suffix. Do not accidentally remove a minus sign in a price.
    value = re.split(r"\s*-\s*(?=\d[\d.,]*\s*(?:m2|m\^2|ha)\b)", value, maxsplit=1)[0].strip()
    if not value or re.search(r"thỏa thuận|thoả thuận|liên hệ", value):
        return None, "unknown", ["missing_or_negotiable_price"]
    per_m2 = bool(re.search(r"/\s*m2\b|mỗi\s*m2\b", value))
    value = re.sub(r"/\s*m2\b|mỗi\s*m2\b", "", value).strip()
    units = {"tỷ": 1e9, "tỉ": 1e9, "triệu": 1e6, "nghìn": 1e3, "đồng": 1., "vnd": 1., "đ": 1.}
    pattern = r"([+-]?\d+(?:[.,]\d+)*)\s*(tỷ|tỉ|triệu|nghìn|đồng|vnd|đ)\b"
    matches = list(re.finditer(pattern, value))
    residue = re.sub(pattern, "", value).strip()
    if not matches or residue:
        return None, "unknown", ["ambiguous_price_or_unit"]
    total, flags, previous_unit = 0., [], float("inf")
    for match in matches:
        try:
            number, number_flags = parse_number(match.group(1))
        except ValueError as exc:
            return None, "unknown", [str(exc)]
        unit = units[match.group(2)]
        # Compound prices must be nonnegative descending units (1 tỷ 200 triệu).
        # A range/negative component or repeated unit is not an additive price.
        if number < 0 or unit >= previous_unit:
            return None, "unknown", ["ambiguous_compound_price"]
        previous_unit = unit
        total += number * unit
        flags.extend(number_flags)
    if total <= 0:
        return None, "unknown", flags + ["nonpositive_price"]
    if per_m2:
        if area is None or area <= 0:
            return None, "per_m2", flags + ["unit_price_requires_area"]
        total *= area
        flags.append("total_derived_from_explicit_unit_price")
    return total, "per_m2" if per_m2 else "total", flags


def classify_title(title: object) -> tuple[str, str, list[str]]:
    title = normalize(title)
    original_title = title
    # Narrow, documented spelling repairs; no general fuzzy matching.
    title = re.sub(r"\bbán(?=đất\b|nhà\b)", "bán ", title)
    title = re.sub(r"\bđấtbán\b", "đất bán", title)
    title = re.sub(r"\bđat\b", "đất", title)
    title = re.sub(r"\bcho thê\b", "cho thuê", title)
    title = re.sub(r"\bhoạc\b", "hoặc", title)
    context_flags = ["title_spelling_normalized"] if title != original_title else []
    # Location/investor phrases do not name the advertised asset.
    asset_title = re.sub(r"\bnha trang\b|\bnha đam\b|\bnhà bè\b|\bnhà đầu tư\b|\bnhà nước\b|\bnhà máy\b", " ", title)
    # Nearby amenities and hypothetical construction do not name this asset.
    asset_title = re.sub(r"\b(?:gần|cạnh|kề|sát|đối diện|liền kề)\s+(?:khu\s+|tòa\s+)?(?:chung cư|căn hộ|nhà máy|nhà thờ)\b", " ", asset_title)
    asset_title = re.sub(r"\b(?:xây|xây dựng)\s+(?:tòa\s+)?(?:căn hộ|chung cư|nhà trọ)\b", " ", asset_title)
    comparative = bool(re.search(r"(?:chung cư|căn hộ).{0,12}\bhay\s+nhà\b|\bnhà.{0,12}\bhay\s+(?:chung cư|căn hộ)", title))
    explicit_land = bool(re.search(r"(?:\bbán\s+(?:gấp\s+)?(?:lô\s+)?)?\bđất\b|\bđất nền\b|\bnền\s+(?:biệt thự|thổ cư)\b", asset_title))
    land_asset_first = bool(re.search(r"^(?:chính chủ\s+|cần\s+|bán\s+|gấp\s+|lô\s+|\d+[\d.,]*m2\s+)*?(?:đất|nền)\b", asset_title))
    explicit_house_first = bool(re.search(r"^(?:chính chủ\s+|cần\s+|bán\s+|gấp\s+|căn\s+)*?(?:nhà|biệt thự)\b", asset_title))
    if comparative:
        kind = "other_unknown"
        context_flags.append("ambiguous_property_comparison_requires_review")
    elif re.search(r"căn hộ|chung cư|apartment|condo|\bccmn\b|\bcc\b.*\b\d+pn\b", asset_title):
        kind = "apartment"
    elif land_asset_first and explicit_land and not explicit_house_first:
        kind = "land"
    elif re.search(r"\bnhà\b|biệt thự|\bnha\b|\bbiệt\s*thự\b|\bdãy\s+(?:phòng\s+)?trọ\b|\bdạy trọ\b", asset_title):
        kind = "house"
    elif re.search(r"\bđất\b|\bdat\b|\bnền\b|\bruộng\b|\brẫy\b", asset_title):
        kind = "land"
    else:
        kind = "other_unknown"
    rent_title = re.sub(r"\b(?:tiện|thích hợp|phù hợp)(?:\s+để)?\s+cho thuê\b", " ", title)
    rent = bool(re.search(r"cho thuê|cần thuê|thuê căn|thuê nhà", rent_title))
    sale = bool(re.search(r"\bbán\b|\bban\b|chuyển nhượng", title))
    income = bool(re.search(r"đang cho thuê|hiện.*cho thuê|hợp đồng thuê|vừa ở vừa cho thuê|1 ở.*cho thuê", title))
    if rent and (re.match(r"cho thuê", title) or "thuê hoặc bán" in title or "bán hoặc cho thuê" in title):
        transaction = "ambiguous_mixed" if sale else "rental"
    elif rent and sale:
        transaction = "sale_with_rental_income" if income else "ambiguous_mixed"
    elif rent:
        transaction = "sale_with_rental_income" if income else "rental_or_ambiguous"
    else:
        transaction = "sale" if sale else "sale_assumed"
    flags = ["property_type_inferred_from_title"] + context_flags
    if kind == "other_unknown":
        flags.append("unknown_property_type")
    if transaction == "sale_assumed":
        flags.append("transaction_assumed_sale_from_dataset_context")
    if income:
        flags.append("rental_income_mentioned")
    return kind, transaction, flags


def clean_records(records: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    kept, rejected, lineage = [], [], []
    fingerprints: dict[str, int] = {}
    missing_before = {key: sum(not normalize(row.get(key)) for row in records) for key in CORE_FIELDS}
    raw_unparseable_area_count = sum(parse_area(row.get("area"))[0] is None for row in records)
    unique_unparseable_area_before_recovery = 0
    parse_before = {"area_m2": 0, "sale_price_vnd": 0}
    for row_id, row in enumerate(records, start=1):
        # All five core fields must agree. Repeated ads are not distinct transactions.
        fingerprint = hashlib.sha256(json.dumps([normalize(row.get(k)) for k in CORE_FIELDS], ensure_ascii=False).encode("utf8")).hexdigest()
        if fingerprint in fingerprints:
            lineage.append({"row_id": row_id, "listing_id": fingerprint[:20], "status": "duplicate", "canonical_row_id": fingerprints[fingerprint], "reasons": "same_five_normalized_core_fields"})
            continue
        fingerprints[fingerprint] = row_id
        flags, reasons = [], []
        area, area_flags = parse_area(row.get("area"))
        unique_unparseable_area_before_recovery += area is None
        price_area, price_area_flags = parse_area(row.get("price"))
        source = "top_level_area"
        if area is None and price_area is not None:
            area, area_flags, source = price_area, price_area_flags, "top_level_price_embedded_area"
            flags.append("area_recovered_from_price_text")
        elif area is not None and price_area is not None and not np.isclose(area, price_area, rtol=1e-6, atol=1e-6):
            reasons.append("area_conflict_between_core_fields")
        flags.extend(area_flags)
        price, basis, price_flags = parse_price(row.get("price"), area)
        flags.extend(price_flags)
        parse_before["area_m2"] += area is None
        parse_before["sale_price_vnd"] += price is None
        if area is None:
            reasons.append("invalid_or_missing_area")
        if price is None:
            reasons.append("invalid_or_missing_price")
        kind, transaction, title_flags = classify_title(row.get("title"))
        flags.extend(title_flags)
        review_reasons, review_flags, review_evidence = check_source_consistency(
            row, area, price, basis, parse_number, normalize)
        reasons.extend(review_reasons)
        flags.extend(review_flags)
        if transaction not in ("sale", "sale_assumed", "sale_with_rental_income"):
            reasons.append("exclude_rental_or_mixed_transaction")
        title = normalize(row.get("title"))
        if re.search(r"trả trước|đặt cọc|thanh toán trước|trả góp|góp chỉ", title):
            reasons.append("payment_not_confirmed_total_price")
        # A review threshold, never a correction/multiplication. Preserve in rejected CSV.
        if price is not None and price < 10_000_000:
            reasons.append("quarantine_total_price_below_10m_vnd")
        province, district, location_flags = parse_location(row.get("location"))
        flags.extend(location_flags)
        value = {"row_id": row_id, "listing_id": fingerprint[:20], "province": province,
                 "district": district, "property_type": kind, "transaction_status": transaction,
                 "area_m2": area, "sale_price_vnd": price,
                 "price_per_m2_vnd": price / area if area and price else None,
                 "price_basis": basis, "area_source": source,
                 "source_review_evidence": json.dumps(review_evidence, ensure_ascii=False, separators=(",", ":")),
                 "quality_flags": ";".join(sorted(set(flags)))}
        status = "rejected" if reasons else "kept"
        lineage.append({"row_id": row_id, "listing_id": fingerprint[:20], "status": status, "canonical_row_id": row_id, "reasons": ";".join(sorted(set(reasons)))})
        if reasons:
            rejected.append({**value, "rejection_reasons": ";".join(sorted(set(reasons)))})
        else:
            kept.append(value)
    clean = pd.DataFrame(kept)
    if clean.empty:
        raise ValueError("No usable sale listings; inspect raw input and rejection log.")
    lineage_df = pd.DataFrame(lineage)
    rejected_df = pd.DataFrame(rejected, columns=list(clean.columns) + ["rejection_reasons"])
    info = {"raw_count": len(records), "clean_count": len(clean), "rejected_count": len(rejected),
            "duplicate_count": int((lineage_df.status == "duplicate").sum()),
            "unique_core_count": len(fingerprints), "raw_missing_fields": missing_before,
            "raw_unparseable_area_count": raw_unparseable_area_count,
            "unique_unparseable_area_before_recovery": unique_unparseable_area_before_recovery,
            "unparseable_unique_core_fields_before_rejection": parse_before,
            "area_recovered_count": int(clean.area_source.eq("top_level_price_embedded_area").sum()),
            "rejection_reasons": dict(pd.Series([reason for row in rejected for reason in row["rejection_reasons"].split(";")], dtype=str).value_counts().items())}
    assert info["raw_count"] == info["clean_count"] + info["rejected_count"] + info["duplicate_count"]
    return clean, rejected_df, lineage_df, info


def iqr_flags(values: pd.Series) -> tuple[pd.Series, dict]:
    q1, q3 = values.quantile([.25, .75])
    width = q3 - q1
    lower, upper = q1 - 1.5 * width, q3 + 1.5 * width
    return (values < lower) | (values > upper), {"q1": float(q1), "q3": float(q3), "lower": float(lower), "upper": float(upper)}


def add_outlier_flags(clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    clean = clean.copy()
    clean["is_outlier_global"], global_bounds = iqr_flags(clean.price_per_m2_vnd)
    clean["is_outlier_group"] = False
    clean["iqr_group"] = ""
    bounds = []
    for (province, kind), rows in clean.groupby(["province", "property_type"], sort=True):
        if len(rows) >= 30:
            reference, group_name, level = rows, f"{province}|{kind}", "province_type"
        else:
            type_rows = clean[clean.property_type.eq(kind)]
            reference = type_rows if len(type_rows) >= 30 else clean
            group_name = kind if len(type_rows) >= 30 else "all"
            level = "type_fallback" if len(type_rows) >= 30 else "global_fallback"
        _, limits = iqr_flags(reference.price_per_m2_vnd)
        mask = (rows.price_per_m2_vnd < limits["lower"]) | (rows.price_per_m2_vnd > limits["upper"])
        clean.loc[rows.index, "is_outlier_group"] = mask
        clean.loc[rows.index, "iqr_group"] = group_name
        bounds.append({"province": province, "property_type": kind, "n_target": len(rows), "n_reference": len(reference), "level": level, "iqr_group": group_name, **limits})
    return clean, pd.DataFrame(bounds), global_bounds


def kmeans(x: np.ndarray, k: int, seed: int = SEED, n_init: int = 10, max_iter: int = 150) -> tuple[np.ndarray, np.ndarray, float]:
    """NumPy implementation, KMeans++ starts; fixed seed and multiple restarts."""
    x = np.asarray(x, dtype=float)
    if x.ndim != 2 or not np.isfinite(x).all() or x.shape[1] == 0:
        raise ValueError("kmeans_requires_finite_matrix")
    if any(not isinstance(v, (int, np.integer)) or v < 1 for v in (k, n_init, max_iter)):
        raise ValueError("kmeans_requires_positive_integer_parameters")
    if len(x) < k or len(np.unique(x, axis=0)) < k:
        raise ValueError("k_exceeds_distinct_points")
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(n_init):
        centers = [x[rng.integers(len(x))]]
        for _ in range(1, k):
            distance = np.min(((x[:, None, :] - np.array(centers)[None, :, :]) ** 2).sum(axis=2), axis=1)
            centers.append(x[rng.choice(len(x), p=distance / distance.sum())])
        centers = np.array(centers)
        for _ in range(max_iter):
            distances = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
            labels = distances.argmin(axis=1)
            updated = np.array([x[labels == j].mean(axis=0) if np.any(labels == j) else x[np.argmax(distances.min(axis=1))] for j in range(k)])
            if np.max(np.abs(updated - centers)) < 1e-7:
                centers = updated
                break
            centers = updated
        distances = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
        labels = distances.argmin(axis=1)
        inertia = float(distances[np.arange(len(x)), labels].sum())
        if best is None or inertia < best[2]:
            best = labels.copy(), centers.copy(), inertia
    return best


def sampled_silhouette(x: np.ndarray, labels: np.ndarray, seed: int = SEED, sample_size: int = 1000) -> float:
    x, labels = np.asarray(x, dtype=float), np.asarray(labels)
    if x.ndim != 2 or not np.isfinite(x).all() or labels.ndim != 1 or len(x) != len(labels):
        raise ValueError("silhouette_requires_aligned_finite_data")
    if not isinstance(sample_size, (int, np.integer)) or sample_size < 2:
        raise ValueError("silhouette_sample_too_small")
    rng = np.random.default_rng(seed)
    selected = np.sort(rng.choice(len(x), size=min(sample_size, len(x)), replace=False))
    points, classes = x[selected], labels[selected]
    if not 2 <= len(np.unique(classes)) < len(points):
        raise ValueError("silhouette_sample_requires_two_to_n_minus_one_clusters")
    distances = np.sqrt(np.maximum(((points[:, None, :] - points[None, :, :]) ** 2).sum(axis=2), 0))
    scores = np.zeros(len(points))
    for i, label in enumerate(classes):
        own = classes == label
        if own.sum() <= 1:
            continue
        a = distances[i, own].sum() / (own.sum() - 1)
        other = [distances[i, classes == j].mean() for j in np.unique(classes) if j != label]
        b = min(other)
        scores[i] = (b - a) / max(a, b) if max(a, b) else 0
    return float(scores.mean())


def adjusted_rand_index(a: np.ndarray, b: np.ndarray) -> float:
    """Partition agreement invariant to label numbering; not ground-truth accuracy."""
    if len(a) != len(b):
        raise ValueError("partition_lengths_differ")
    if len(a) < 2:
        return 1.
    _, ai = np.unique(a, return_inverse=True)
    _, bi = np.unique(b, return_inverse=True)
    contingency = np.zeros((ai.max()+1, bi.max()+1), dtype=np.int64)
    np.add.at(contingency, (ai, bi), 1)
    choose2 = lambda values: (values * (values - 1) / 2).sum()
    index = choose2(contingency)
    row_pairs, col_pairs = choose2(contingency.sum(axis=1)), choose2(contingency.sum(axis=0))
    expected = row_pairs * col_pairs / (len(a) * (len(a) - 1) / 2)
    maximum = (row_pairs + col_pairs) / 2
    return float((index - expected) / (maximum - expected)) if maximum != expected else 1.


def cluster_records(clean: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    clean = clean.copy()
    # Keep outliers in analysis but leave them outside this illustrative segmentation.
    mask = ~clean.is_outlier_group
    subset = clean.loc[mask]
    logged = np.log(subset[["area_m2", "price_per_m2_vnd"]].to_numpy(float))
    means, scales = logged.mean(axis=0), logged.std(axis=0)
    if len(subset) < 10 or np.any(scales == 0):
        raise ValueError("insufficient_variable_data_for_clustering")
    x = (logged - means) / scales
    models, trials = {}, []
    for k in range(2, 6):
        labels, centers, inertia = kmeans(x, k)
        score = sampled_silhouette(x, labels)
        trials.append({"k": k, "silhouette_sample": score, "inertia": inertia, "min_cluster_size": int(np.bincount(labels).min())})
        models[k] = (labels, centers)
    chosen = max(trials, key=lambda row: (row["silhouette_sample"], -row["k"]))["k"]
    labels, centers = models[chosen]
    stability = []
    for alternate_seed in (7, 42):
        alternate_labels, _, alternate_inertia = kmeans(x, chosen, seed=alternate_seed)
        stability.append({"seed": alternate_seed, "adjusted_rand_vs_primary": adjusted_rand_index(labels, alternate_labels), "inertia": alternate_inertia})
    # Stable presentation ordering by centroid unit price, then area.
    order = np.lexsort((centers[:, 0], centers[:, 1]))
    mapping = {int(old): new + 1 for new, old in enumerate(order)}
    clean["cluster"] = -1
    clean.loc[mask, "cluster"] = [mapping[int(label)] for label in labels]
    summaries = clean[mask].groupby("cluster").agg(n=("row_id", "size"), median_area_m2=("area_m2", "median"), median_price_vnd=("sale_price_vnd", "median"), median_price_per_m2_vnd=("price_per_m2_vnd", "median")).reset_index()
    metadata = {"method": "NumPy KMeans++ / Lloyd, 10 starts, 150 iterations maximum", "features": ["ln(area_m2)", "ln(price_per_m2_vnd)"],
                "standardization": "population z-score after natural logarithm", "seed": SEED, "chosen_k": chosen,
                "fit_count": len(subset), "excluded_group_outliers": int((~mask).sum()),
                "silhouette_sample_size": min(1000, len(x)), "log_means": means.tolist(), "log_std": scales.tolist(),
                "stability_checks": stability,
                "purpose": "exploratory segmentation; no ground truth, prediction, investment recommendation or market validation"}
    return clean, pd.DataFrame(trials), summaries, metadata


def summarize_groups(clean: pd.DataFrame, keys: list[str], bootstrap: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    result = []
    for name, rows in clean.groupby(keys, sort=True):
        names = name if isinstance(name, tuple) else (name,)
        unit = rows.price_per_m2_vnd.to_numpy()
        q1, q3 = np.quantile(unit, [.25, .75])
        record = dict(zip(keys, names))
        record.update(n=len(rows), median_area_m2=float(rows.area_m2.median()), median_price_vnd=float(rows.sale_price_vnd.median()), median_price_per_m2_vnd=float(np.median(unit)), q1_price_per_m2_vnd=float(q1), q3_price_per_m2_vnd=float(q3), share_group_outlier=float(rows.is_outlier_group.mean()))
        if bootstrap and len(unit) >= 30:
            medians = np.median(rng.choice(unit, size=(500, len(unit)), replace=True), axis=1)
            record.update(bootstrap_low_vnd=float(np.quantile(medians, .025)), bootstrap_high_vnd=float(np.quantile(medians, .975)))
        result.append(record)
    return pd.DataFrame(result).sort_values("n", ascending=False, kind="stable").reset_index(drop=True)


def sensitivity_table(clean: pd.DataFrame) -> pd.DataFrame:
    scenarios = {"all_clean_sales": np.ones(len(clean), bool), "without_global_iqr_outliers": ~clean.is_outlier_global,
                 "without_group_iqr_outliers": ~clean.is_outlier_group,
                 "without_dot_grouping_uncertainty": ~clean.quality_flags.str.contains("dot_thousands_convention"),
                 "explicit_sale_titles_only": clean.transaction_status.eq("sale")}
    result = []
    baseline = clean.price_per_m2_vnd.median()
    for name, mask in scenarios.items():
        rows = clean.loc[mask]
        result.append({"scenario": name, "n": len(rows), "excluded": len(clean) - len(rows), "median_area_m2": float(rows.area_m2.median()), "median_price_vnd": float(rows.sale_price_vnd.median()), "median_price_per_m2_vnd": float(rows.price_per_m2_vnd.median()), "unit_price_median_change_pct": float((rows.price_per_m2_vnd.median() / baseline - 1) * 100)})
    return pd.DataFrame(result)


def chart_setup():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.labelcolor": "#36465C", "text.color": "#1D3045", "figure.facecolor": "#FAFCFE", "axes.facecolor": "#FAFCFE", "savefig.facecolor": "#FAFCFE", "grid.alpha": .2})


def save_chart(fig, path: Path):
    fig.text(.01, .008, "Nguồn: Mendeley / Chợ Tốt, công bố 01/2021 • Giá rao bán • Mẫu thuận tiện, không đại diện thị trường", fontsize=8, color="#65758A")
    fig.tight_layout(rect=[0, .035, 1, 1])
    fig.savefig(path, dpi=170, bbox_inches="tight")
    plt.close(fig)


def make_charts(clean, info, province, sensitivity, trials, folder: Path):
    chart_setup()
    n = len(clean)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    axes[0].hist(clean.sale_price_vnd / 1e9, bins=50, color=COLORS[0], edgecolor="white")
    axes[0].set(xlabel="Giá rao tổng (tỷ VND)", ylabel="Số tin", title=f"Phân phối giá trên thang gốc • n={n:,}")
    axes[1].hist(np.log10(clean.sale_price_vnd / 1e9), bins=35, color=COLORS[1], edgecolor="white")
    axes[1].set(xlabel="log10(giá rao tổng / 1 tỷ VND)", ylabel="Số tin", title="Thang log giúp thấy phân phối lệch")
    save_chart(fig, folder / "01_price_distribution.png")
    fig, ax = plt.subplots(figsize=(9, 5.6))
    for kind, rows in clean.groupby("property_type"):
        ax.scatter(rows.area_m2, rows.sale_price_vnd / 1e9, s=10, alpha=.28, label=f"{TYPE_LABELS[kind]} (n={len(rows):,})")
    ax.set(xscale="log", yscale="log", xlabel="Diện tích (m², thang log)", ylabel="Giá rao tổng (tỷ VND, thang log)", title=f"Diện tích và giá rao bán • n={n:,}")
    ax.legend(fontsize=8)
    save_chart(fig, folder / "02_area_price_scatter.png")
    top = province[province.n >= 30].head(10).sort_values("median_price_per_m2_vnd")
    fig, ax = plt.subplots(figsize=(11, 5.8))
    vals = top.median_price_per_m2_vnd.to_numpy() / 1e6
    lows = top.bootstrap_low_vnd.to_numpy() / 1e6
    highs = top.bootstrap_high_vnd.to_numpy() / 1e6
    ax.barh([f"{r.province} (n={r.n:,})" for r in top.itertuples()], vals, color=COLORS[0])
    ax.errorbar(vals, np.arange(len(top)), xerr=np.vstack([np.maximum(vals - lows, 0), np.maximum(highs - vals, 0)]), fmt="none", ecolor="#24354B", capsize=3)
    ax.set(xlabel="Trung vị giá rao (triệu VND/m²)", title="10 địa phương có nhiều tin nhất • n ≥ 30\nKhoảng bootstrap 95% có điều kiện trên mẫu, 500 lần lấy mẫu")
    save_chart(fig, folder / "03_province_medians.png")
    fig, ax = plt.subplots(figsize=(10, 5.8))
    labels, vals = [], []
    for kind, rows in clean.groupby("property_type", sort=True):
        labels.append(f"{TYPE_LABELS[kind]}\nn={len(rows):,}")
        vals.append(rows.price_per_m2_vnd.to_numpy() / 1e6)
    ax.boxplot(vals, tick_labels=labels, showfliers=False, patch_artist=True, boxprops={"facecolor": "#C9E4E8"}, medianprops={"color": "#B55428", "linewidth": 2})
    ax.set(yscale="log", ylabel="Giá rao (triệu VND/m², thang log)", title="So sánh loại bất động sản suy luận từ tiêu đề\nĐiểm ngoài râu ẩn trong hình, vẫn giữ trong dữ liệu")
    save_chart(fig, folder / "04_type_boxplot.png")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    coverage = province.head(10).sort_values("n")
    ax.barh(coverage.province, coverage.n, color=COLORS[2])
    ax.set(xlabel="Số tin đã làm sạch", title=f"Độ phủ mẫu theo địa phương • n={n:,}")
    for i, r in enumerate(coverage.itertuples()):
        ax.text(r.n + 10, i, f"{r.n:,}", va="center", fontsize=9)
    ax.set_xlim(0, coverage.n.max() * 1.15)
    save_chart(fig, folder / "05_sample_coverage.png")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    labels = ["Dữ liệu gốc", "Tin trùng", "Cách ly", "Giữ phân tích"]
    values = [info["raw_count"], info["duplicate_count"], info["rejected_count"], info["clean_count"]]
    axes[0].bar(labels, values, color=[COLORS[2], COLORS[1], COLORS[3], COLORS[0]])
    for i, value in enumerate(values):
        axes[0].text(i, value + 80, f"{value:,}", ha="center")
    axes[0].set(ylabel="Số dòng", title="Đối soát làm sạch (không bù giá/diện tích)")
    scenarios = ["Toàn bộ", "Bỏ IQR toàn cục", "Bỏ IQR theo nhóm", "Bỏ dấu chấm nghìn", "Tiêu đề bán rõ"]
    axes[1].barh(scenarios, sensitivity.median_price_per_m2_vnd / 1e6, color=COLORS[0])
    axes[1].set(xlabel="Trung vị giá (triệu VND/m²)", title="Độ nhạy với lựa chọn xử lý")
    save_chart(fig, folder / "06_cleaning_sensitivity.png")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))
    clustered = clean[clean.cluster > 0]
    for j, rows in clustered.groupby("cluster"):
        axes[0].scatter(rows.area_m2, rows.price_per_m2_vnd / 1e6, s=8, alpha=.3, label=f"Cụm {j} (n={len(rows):,})", color=COLORS[(j-1) % len(COLORS)])
    axes[0].set(xscale="log", yscale="log", xlabel="Diện tích (m², thang log)", ylabel="Giá rao (triệu VND/m², thang log)", title=f"K-means: phân khúc thăm dò • n={len(clustered):,}")
    axes[0].legend(fontsize=8)
    axes[1].plot(trials.k, trials.silhouette_sample, "o-", color=COLORS[0])
    axes[1].set(xticks=trials.k, xlabel="Số cụm k", ylabel="Silhouette trên mẫu tối đa 1.000 tin", title="So sánh k=2…5, cùng seed / 10 khởi tạo")
    save_chart(fig, folder / "07_exploratory_clusters.png")
    fig, ax = plt.subplots(figsize=(7.5, 5.3))
    features = clean[["area_m2", "sale_price_vnd", "price_per_m2_vnd"]]
    corr = features.rank().corr().to_numpy()
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdBu_r")
    names = ["Diện tích", "Giá tổng", "Giá/m²"]
    ax.set(xticks=range(3), yticks=range(3), xticklabels=names, yticklabels=names, title=f"Tương quan Spearman • n={n:,}\nGiá/m² là biến dẫn xuất; tương quan không chứng minh nhân quả")
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{corr[i,j]:.3f}", ha="center", va="center", color="white" if abs(corr[i,j]) > .6 else "#182D43", fontsize=15)
    fig.colorbar(im, ax=ax, shrink=.8)
    save_chart(fig, folder / "08_spearman_correlation.png")


SCHEMA_SQL = """PRAGMA foreign_keys = ON;
CREATE TABLE provinces (province_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE property_types (type_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE listings (
    row_id INTEGER PRIMARY KEY,
    listing_id TEXT NOT NULL UNIQUE,
    province_id INTEGER NOT NULL REFERENCES provinces(province_id),
    type_id INTEGER NOT NULL REFERENCES property_types(type_id),
    district TEXT NOT NULL,
    transaction_status TEXT NOT NULL,
    area_m2 REAL NOT NULL CHECK (area_m2 > 0),
    sale_price_vnd REAL NOT NULL CHECK (sale_price_vnd >= 10000000),
    price_per_m2_vnd REAL NOT NULL CHECK (price_per_m2_vnd > 0),
    is_outlier_group INTEGER NOT NULL CHECK (is_outlier_group IN (0,1)),
    cluster INTEGER NOT NULL,
    CHECK (ABS(price_per_m2_vnd * area_m2 - sale_price_vnd) < MAX(1, sale_price_vnd * 0.000001))
);
"""
BENCH_QUERY = """SELECT row_id, area_m2, sale_price_vnd, price_per_m2_vnd
FROM listings
WHERE province_id = ? AND type_id = ?
  AND price_per_m2_vnd BETWEEN ? AND ?
ORDER BY price_per_m2_vnd, row_id LIMIT 100"""
INDEX_SQL = "CREATE INDEX idx_listings_search ON listings(province_id, type_id, price_per_m2_vnd, row_id);"
QUERIES_SQL = """-- 01: coverage and medians are in Python; SQLite AVG below is explicitly a MEAN.
SELECT p.name AS province, COUNT(*) AS n, AVG(l.price_per_m2_vnd)/1000000.0 AS mean_million_vnd_m2
FROM listings l JOIN provinces p USING(province_id)
GROUP BY p.province_id, p.name HAVING COUNT(*) >= 30 ORDER BY n DESC;

-- 02: compare inferred property types within one province (control compositional mix).
SELECT p.name AS province, t.name AS property_type, COUNT(*) AS n,
       AVG(l.price_per_m2_vnd)/1000000.0 AS mean_million_vnd_m2
FROM listings l JOIN provinces p USING(province_id) JOIN property_types t USING(type_id)
WHERE p.name = 'Tp Hồ Chí Minh'
GROUP BY p.province_id, t.type_id HAVING COUNT(*) >= 30;

-- 03: flagged outliers remain queryable, never silently removed.
SELECT l.row_id, p.name AS province, t.name AS property_type, l.area_m2, l.sale_price_vnd, l.price_per_m2_vnd
FROM listings l JOIN provinces p USING(province_id) JOIN property_types t USING(type_id)
WHERE l.is_outlier_group = 1 ORDER BY l.price_per_m2_vnd DESC LIMIT 20;

-- 04: parameterized search benchmark. Bind EXACT params in outputs/sql_benchmark.json.
""" + BENCH_QUERY + ";\n"


def build_database(clean: pd.DataFrame, database: Path, sql_folder: Path) -> dict:
    if database.exists():
        database.unlink()  # Only this generated DB under output root; source is never touched.
    conn = sqlite3.connect(database)
    conn.executescript(SCHEMA_SQL)
    province_map = {name: i + 1 for i, name in enumerate(sorted(clean.province.unique()))}
    type_map = {name: i + 1 for i, name in enumerate(sorted(clean.property_type.unique()))}
    conn.executemany("INSERT INTO provinces VALUES (?, ?)", [(i, name) for name, i in province_map.items()])
    conn.executemany("INSERT INTO property_types VALUES (?, ?)", [(i, name) for name, i in type_map.items()])
    rows = [(int(r.row_id), r.listing_id, province_map[r.province], type_map[r.property_type], r.district,
             r.transaction_status, float(r.area_m2), float(r.sale_price_vnd), float(r.price_per_m2_vnd), int(r.is_outlier_group), int(r.cluster)) for r in clean.itertuples()]
    conn.executemany("INSERT INTO listings VALUES (?,?,?,?,?,?,?,?,?,?,?)", rows)
    conn.commit()
    # Both stages have table statistics; the second additionally has index statistics.
    conn.execute("ANALYZE")
    common = clean.groupby(["province", "property_type"]).size().sort_values(ascending=False).index[0]
    subset = clean[clean.province.eq(common[0]) & clean.property_type.eq(common[1])]
    low, high = subset.price_per_m2_vnd.quantile([.35, .65]).tolist()
    params = (province_map[common[0]], type_map[common[1]], low, high)

    def measure():
        plan = [list(row) for row in conn.execute("EXPLAIN QUERY PLAN " + BENCH_QUERY, params)]
        result = conn.execute(BENCH_QUERY, params).fetchall()
        encoded = json.dumps(result, separators=(",", ":"))
        result_hash = hashlib.sha256(encoded.encode()).hexdigest()
        # Warm-cache latency: 10 warm-ups, 51 repeated identical queries.
        for _ in range(10):
            conn.execute(BENCH_QUERY, params).fetchall()
        timings = []
        for _ in range(51):
            start = time.perf_counter_ns()
            conn.execute(BENCH_QUERY, params).fetchall()
            timings.append((time.perf_counter_ns() - start) / 1e6)
        return {"plan": plan, "result_count": len(result), "result_sha256": result_hash,
                "median_ms": statistics.median(timings), "p10_ms": float(np.quantile(timings, .1)), "p90_ms": float(np.quantile(timings, .9))}

    before = measure()
    conn.execute(INDEX_SQL)
    conn.commit()
    conn.execute("ANALYZE")
    after = measure()
    if before["result_sha256"] != after["result_sha256"]:
        conn.close()
        raise ValueError('SQL index changed query results; refusing to publish this run.')
    integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
    foreign_key_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
    conn.close()
    if integrity != 'ok' or foreign_key_errors:
        raise ValueError('Database integrity or foreign-key verification failed.')
    (sql_folder / "01_schema.sql").write_text(SCHEMA_SQL, encoding="utf8")
    (sql_folder / "02_queries.sql").write_text(QUERIES_SQL, encoding="utf8")
    (sql_folder / "03_indexes.sql").write_text(INDEX_SQL + "\nANALYZE;\n", encoding="utf8")
    return {"sqlite_version": sqlite3.sqlite_version, "listing_count": len(clean), "province_count": len(province_map),
            "query": BENCH_QUERY, "parameters": list(params), "parameter_labels": {"province": common[0], "property_type": common[1]},
            "before": before, "after": after, "median_speedup": before["median_ms"] / after["median_ms"],
            "identical_results": True, "integrity_check": integrity, "foreign_key_errors": foreign_key_errors,
            "protocol": "One real source snapshot. Same connection, SQL and parameters; ANALYZE before each stage, second stage has composite index and its statistics; 10 warmups + 51 timings per stage. Sequential before/after warm-cache illustration, not randomized or a production speedup claim."}


def json_default(value):
    if isinstance(value, (np.integer, np.bool_)):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    raise TypeError(f"Cannot serialize {type(value)}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=ROOT / "data/raw/chotot_data.json")
    parser.add_argument("--output-root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root, raw = args.output_root.resolve(), args.raw.resolve()
    records, original_hash = read_verified_source(raw)
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
    stage_parent = root / 'tmp'
    stage_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='pipeline_stage_', dir=stage_parent) as temporary:
        staging = Path(temporary).resolve()
        if not staging.is_relative_to(stage_parent.resolve()):
            raise ValueError('Unexpected staging path outside the project.')
        analysis = generate_outputs(staging, raw, records, original_hash, run_id)
        artifacts = {path.relative_to(staging).as_posix(): file_sha256(path)
                     for path in sorted(staging.rglob('*')) if path.is_file()}
        manifest = {'schema_version': '2.0', 'run_id': run_id,
                    'created_at_utc': datetime.now(timezone.utc).isoformat(),
                    'source_sha256': original_hash,
                    'source_files': {name: file_sha256(ROOT / name) for name in CORE_CODE},
                    'artifacts': artifacts}
        for relative in artifacts:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            (staging / relative).replace(target)
        manifest_tmp = root / 'outputs/run_manifest.pending.json'
        manifest_tmp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        manifest_tmp.replace(root / 'outputs/run_manifest.json')
    print(json.dumps({'run_id': run_id, 'counts': analysis['counts'], 'overall': analysis['overall'],
                      'chosen_k': analysis['clustering']['chosen_k'],
                      'sql_speedup': analysis['sql_benchmark']['median_speedup']},
                     ensure_ascii=True, default=json_default))


def generate_outputs(root, raw, records, original_hash, run_id):
    """Build in a temporary tree; publish nothing if any generation step fails."""
    processed, outputs, charts, tables, sql = root / "data/processed", root / "outputs", root / "outputs/charts", root / "outputs/tables", root / "sql"
    for folder in (processed, outputs, charts, tables, sql):
        folder.mkdir(parents=True, exist_ok=True)
    clean, rejected, lineage, counts = clean_records(records)
    clean, iqr_bounds, global_bounds = add_outlier_flags(clean)
    clean, cluster_trials, clusters, cluster_meta = cluster_records(clean)
    province = summarize_groups(clean, ["province"], bootstrap=True)
    property_type = summarize_groups(clean, ["property_type"])
    province_type = summarize_groups(clean, ["province", "property_type"])
    sensitivity = sensitivity_table(clean)
    describe = clean[["area_m2", "sale_price_vnd", "price_per_m2_vnd"]].describe(percentiles=[.01, .25, .5, .75, .99]).T.reset_index(names="feature")
    clean["area_band"] = pd.cut(clean.area_m2, bins=[0, 30, 60, 100, 200, 500, np.inf], labels=["(0,30]", "(30,60]", "(60,100]", "(100,200]", "(200,500]", ">500"], right=True).astype(str)
    area_bands = summarize_groups(clean, ["area_band"])
    for filename, frame in {"listings_clean": clean, "listings_rejected": rejected, "row_lineage": lineage}.items():
        frame.to_csv(processed / f"{filename}.csv", index=False, encoding="utf-8-sig", float_format="%.17g")
    clean.to_json(processed / "listings_clean.json", orient="records", force_ascii=False, indent=2, double_precision=15)
    for filename, frame in {"province_summary": province, "type_summary": property_type, "province_type_summary": province_type,
                            "descriptive_statistics": describe, "iqr_bounds": iqr_bounds, "sensitivity": sensitivity,
                            "cluster_trials": cluster_trials, "cluster_summary": clusters, "area_band_summary": area_bands}.items():
        frame.to_csv(tables / f"{filename}.csv", index=False, encoding="utf-8-sig", float_format="%.10g")
    benchmark = build_database(clean, outputs / "real_estate.sqlite", sql)
    (outputs / "sql_benchmark.json").write_text(json.dumps(benchmark, ensure_ascii=False, indent=2, default=json_default), encoding="utf8")
    make_charts(clean, counts, province, sensitivity, cluster_trials, charts)
    correlations = clean[["area_m2", "sale_price_vnd", "price_per_m2_vnd"]].rank().corr().round(6).to_dict()
    quality_flags = pd.Series([flag for item in clean.quality_flags for flag in item.split(";") if flag]).value_counts().to_dict()
    analysis = {"schema_version": "2.0", "run_id": run_id, "seed": SEED,
                "environment": {"python": sys.version.split()[0], "numpy": np.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__, "sqlite": sqlite3.sqlite_version},
                "source": {"path": str(raw.relative_to(ROOT)) if raw.is_relative_to(ROOT) else str(raw),
                "sha256": original_hash, "dataset_url": "https://data.mendeley.com/datasets/5477zhnmn2/2", "doi": "10.17632/5477zhnmn2.2",
                "published": "2021-01-12", "license": "CC BY 4.0", "source_claimed_count": 10000, "actual_count": len(records),
                "time_scope": "Historical snapshot; no per-listing timestamp, not current market data"},
                "counts": {**counts, "group_iqr_outlier_count": int(clean.is_outlier_group.sum()), "global_iqr_outlier_count": int(clean.is_outlier_global.sum()),
                           "province_count": int(clean.loc[clean.province.ne("Chưa xác định"), "province"].nunique()), "province_category_count": int(clean.province.nunique()),
                           "unknown_province_count": int(clean.province.eq("Chưa xác định").sum()), "quality_flags": quality_flags, "transaction_status": clean.transaction_status.value_counts().to_dict()},
                "overall": {"median_area_m2": float(clean.area_m2.median()), "median_price_vnd": float(clean.sale_price_vnd.median()), "median_price_per_m2_vnd": float(clean.price_per_m2_vnd.median()),
                            "mean_price_vnd": float(clean.sale_price_vnd.mean()), "mean_price_per_m2_vnd": float(clean.price_per_m2_vnd.mean())},
                "province_summary": province.replace({np.nan: None}).to_dict(orient="records"), "type_summary": property_type.to_dict(orient="records"),
                "province_type_summary": province_type.to_dict(orient="records"), "area_band_summary": area_bands.to_dict(orient="records"),
                "sensitivity": sensitivity.to_dict(orient="records"), "spearman": correlations, "global_iqr_bounds": global_bounds,
                "clustering": {**cluster_meta, "trials": cluster_trials.to_dict(orient="records"), "summary": clusters.to_dict(orient="records")},
                "sql_benchmark": benchmark,
                "policies": ["No imputation of price or area; recover explicit area from top-level price only.", "Deduplicate only when all five normalized core fields match; preserve canonical raw row id.",
                             "Cross-check title/description for explicit unit, currency and gross price/area contradictions; quarantine unresolved cases with numeric evidence, never overwrite source values.",
                             "Text-review flags are conservative rules, not proof that a source entry is wrong; installment, multi-offer and dimension expressions can be ambiguous.",
                             "Quarantine parsed total price below 10m VND for manual review; do not correct presumed units.", "IQR outliers flagged and retained in main analysis; group fallback requires n>=30.",
                             "Type inferred from title, sale status partly assumed; sensitivity shows explicit sale titles.", "Ignore suspicious detail fields; no bedroom/legal/coordinates/date inference.",
                             "Area dot thousands convention flagged; sensitivity excludes affected rows.",
                             "Province requires explicit match to historical 2021 allowlist or known alias; unrecognized locations become Chưa xác định, never inferred from streets.",
                             "CSV clean output omits titles, description, contacts and exact street addresses."],
                "limitations": ["Convenience sample, listing duplicates may remain, no representative market inference.", "Historical locality names from original snapshot; no conversion to 2026 administrative boundaries.",
                                "Asking prices may be erroneous, installments or per-area prices entered as totals; automatic flags cannot resolve all.", "Property type heuristics require human audit; no transaction-level identifiers or dates.",
                                "Bootstrap intervals assume independent ads conditionally on this sample; repeated agents/dependence can understate uncertainty.", "Correlation is descriptive; derived price-per-area variables cause mathematical coupling.", "KMeans has no external validation and is an optional teaching extension."]}
    if file_sha256(raw) != original_hash:
        raise ValueError('Raw file changed while processing; no results were published.')
    (outputs / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2, default=json_default), encoding="utf8")
    return analysis


if __name__ == "__main__":
    main()
