"""Conservative cross-field review rules for a historical listing snapshot.

Rules quarantine ambiguity; they never replace a published price or area. Only
numeric phrases are retained as evidence, without addresses or contact details.
They are automated consistency checks, not human validation of the advertisement.
"""
from __future__ import annotations

import math
import re

NUMBER = r"\d+(?:[.,]\d+)*"
CURRENCY = r"tỷ|tỉ|triệu|trieu|ty|tr"
MONEY = re.compile(rf"(?<![\w.,])({NUMBER})\s*({CURRENCY})(?![^\W\d_])", re.I)
UNIT_PRICE = re.compile(
    rf"(?<![\w.,])({NUMBER})\s*({CURRENCY})\s*(?:/\s*(?:1\s*)?|1\s*)(m2|m\^2|ha|sào|sao|công|cong)\b", re.I)
BUSINESS_TRANSFER = re.compile(
    r"\bsang\s+(?:(?:nhượng|lại)\s+)?(?:quán|tiệm|shop|cửa hàng|mặt bằng|ký túc xá)\b")
PRICE_CONTEXT = re.compile(
    rf"\b(?:giá(?:\s+(?:bán|chào|chỉ|còn|mới|thật|chốt)){{0,3}}|bán\s+giá)\s*[:：=\-]?\s*"
    rf"({NUMBER})\s*({CURRENCY})(?![^\W\d_])", re.I)


def check_source_consistency(row, area, price, basis, parse_number, normalize):
    """Return review reasons, flags and minimal numeric rule evidence.

    Source-description numbers are used to detect a conflict, never as ground
    truth to repair the top-level fields. A flagged row is preserved separately.
    """
    reasons, flags, evidence = [], [], []
    fields = {name: normalize(row.get(name)) for name in ("title", "description")}

    def add(reason, field, numeric_phrase):
        if reason not in reasons:
            reasons.append(reason)
        item = {"rule": reason, "source_field": field, "numeric_phrase": numeric_phrase}
        if item not in evidence:
            evidence.append(item)

    def amount(number, currency):
        n, number_flags = parse_number(number)
        return n * (1e9 if currency in ("tỷ", "tỉ", "ty") else 1e6), number_flags

    def plausible_numbers(number):
        """Do not call a notation ambiguity a confirmed cross-field conflict."""
        try:
            value, _ = parse_number(number)
        except ValueError:
            return []
        values = [value]
        if re.fullmatch(r"\d{1,3}\.\d{3}", number):
            values.append(float(number))
        if re.fullmatch(r"\d{1,3},\d{3}", number):
            values.append(float(number.replace(",", "")))
        return values

    def price_ratio(number, currency, core_price):
        multiplier = 1e9 if currency in ("tỷ", "tỉ", "ty") else 1e6
        candidates = [v * multiplier for v in plausible_numbers(number) if v > 0]
        return min((max(core_price / v, v / core_price) for v in candidates), default=1.)

    title = fields["title"]
    if BUSINESS_TRANSFER.search(title):
        # Exclude transfer of a trading operation/lease, not apartment resales.
        add("outside_scope_business_or_lease_transfer", "title", "business_transfer")

    if price is not None and basis == "total":
        for field, text in fields.items():
            for match in UNIT_PRICE.finditer(text):
                try:
                    unit_amount, _ = amount(match[1], match[2])
                except ValueError:
                    continue
                if math.isclose(price, unit_amount, rel_tol=.01, abs_tol=1):
                    # Even sào/công may differ regionally; quarantine unresolved
                    # basis rather than inventing a conversion or multiplying.
                    add("unresolved_price_basis_from_source_text", field, match[0])

            foreign = re.search(
                rf"\bgiá(?:\s+(?:bán|chào))?\s*[:：]?\s*({NUMBER})\s*(usd|dollar|đô la)\b", text)
            if foreign:
                add("currency_conflict_from_source_text", field, f"{foreign[1]} {foreign[2]}")

        # Direct title prices can be checked when there is one amount and no
        # installment/income/discount context. A large discrepancy is ambiguous,
        # not a license to decide which source field is correct.
        money_title = re.sub(r"\b\d+\s*tr\s*[,;]?\s*\d*\s*(?:lầu|lau|l\b|tầng|tang|t\b)", " ", title)
        matches = list(MONEY.finditer(money_title))
        blockers = r"giảm|cọc|thanh\s*toán|\btt\b|trả\s*(?:trước|góp)|vay|thu\s*nhập|thuê|lương|đợt|chiết\s*khấu|lợi\s*nhuận|tặng|bảo hiểm|\bbh\b|\blỗ\b|\bbớt\b|hoa hồng|\bhạ\b"
        if len(matches) == 1 and not re.search(blockers, title):
            match = matches[0]
            tail = money_title[match.end():]
            same_unit_quote = False
            try:
                quote, _ = amount(match[1], match[2])
                same_unit_quote = area is not None and math.isclose(quote*area, price, rel_tol=.1)
                for unit_match in UNIT_PRICE.finditer(fields["description"]):
                    unit_quote, _ = amount(unit_match[1], unit_match[2])
                    same_unit_quote |= math.isclose(quote, unit_quote, rel_tol=.01)
            except ValueError:
                pass
            if not re.match(r"\s*(?:/|\d)", tail) and not same_unit_quote and re.search(r"\bgiá\b|\bbán\b|\bnhà\b|\bcăn\b|\bchỉ\b", title):
                if price_ratio(match[1], match[2], price) >= 5:
                    add("price_conflict_from_title", "title", match[0])

        # Check one explicit price statement in description. Multiple offers,
        # historical prices and lists of amounts remain outside this rule.
        descriptions = []
        text = fields["description"]
        for match in PRICE_CONTEXT.finditer(text):
            tail = text[match.end():]
            if re.match(r"\s*(?:/|1\s*m2\b)", tail):
                continue
            try:
                quoted, number_flags = amount(match[1], match[2])
            except ValueError:
                continue
            # Common informal compound 3ty550 (3 billion 550 million).
            compound = re.match(r"(\d{2,3})(?!\d)", tail)
            phrase = f"{match[1]} {match[2]}"
            if compound and match[2] in ("tỷ", "tỉ", "ty"):
                quoted += int(compound[1]) * 1e6
                phrase += compound[1]
            elif re.match(r"\d", tail):
                # 2tr8, 1ty7 and floor-count abbreviations need a richer parser;
                # a prefix number is not a trustworthy quotation by itself.
                continue
            # Exclude a local installment, rental or construction-cost statement.
            prefix = text[max(0, match.start()-14):match.start()]
            suffix = text[match.end():match.end()+24]
            if re.search(r"giảm|bớt|lỗ|tặng|hoa hồng|cọc|trả trước|thanh toán|thuê|xây dựng|hỗ trợ|lương", prefix) or re.search(r"/\s*(?:tháng|năm)|\b(?:mỗi tháng|mỗi năm)\b", suffix):
                continue
            # Generic 'giá 30 triệu' may be a discount, deposit or rental
            # amount elsewhere in a long advertisement. Require an explicit
            # sale/asking-price statement for these sub-billion amounts.
            if match[2] in ("triệu", "trieu", "tr") and not re.match(r"(?:giá\s+(?:bán|chào)|bán\s+giá)\b", match[0]):
                continue
            ratio = price_ratio(match[1], match[2], price) if not compound else max(price/quoted, quoted/price)
            descriptions.append((quoted, phrase, number_flags, ratio))
        # Identical restatements are one price; don't compare an arbitrary one
        # when a description contains several different prices.
        distinct = {round(v[0], 2) for v in descriptions}
        if len(distinct) == 1:
            quoted, phrase, _, ratio = descriptions[0]
            if quoted > 0 and ratio >= 5:
                add("price_conflict_from_description", "description", phrase)

    if area is not None:
        # Strong unit mismatch: title names N hectares but core says N m².
        # Do not compare a nearby park/project or silently choose a replacement.
        direct_ha = re.search(rf"^(?:bán\s+|cần\s+|gấp\s+|lô\s+)*({NUMBER})\s*ha\b\s*(?:đất|rẫy|vườn)\b", title)
        if direct_ha:
            try:
                hectares, _ = parse_number(direct_ha[1])
            except ValueError:
                hectares = None
            if hectares is not None and math.isclose(area, hectares, rel_tol=.001):
                add("area_unit_conflict_from_title", "title", f"{direct_ha[1]} ha")

        # A directly declared m² area in the title/description is evidence when
        # the two numbers differ grossly (>= 5x). Multiple areas are ambiguous;
        # do not infer which plot or house-floor area the advertiser meant.
        area_context = re.compile(rf"\b(?:diện tích(?:\s+đất)?|dt)\s*[:：]?\s*(?:là\s+)?({NUMBER})\s*(m2|m\^2)\b")
        for field, text in fields.items():
            declarations = list(area_context.finditer(text))
            values = []
            for match in declarations:
                # "DT: 3m2 x 5" is a dimension expression, despite its malformed
                # width unit. Comparing 3 alone with the plot area is invalid.
                if re.match(r"\s*[x×*]\s*\d", text[match.end():]):
                    flags.append("source_dimension_expression_requires_review")
                    continue
                if re.search(r"mật độ|quy mô|tổng diện tích|khuôn viên dự án", text[max(0, match.start()-24):match.end()+30]):
                    continue
                try:
                    declared_values = plausible_numbers(match[1])
                except ValueError:
                    declared_values = []
                if declared_values:
                    values.append((declared_values, match[1], match[2]))
            if len({v[1] for v in values}) == 1:
                declared_values, number, unit = values[0]
                ratios = [max(area/v, v/area) for v in declared_values if v > 0]
                if ratios and min(ratios) >= 5:
                    add("area_conflict_from_source_text", field, f"{number} {unit}")
    if reasons:
        flags.append("source_text_requires_review")
    return reasons, flags, evidence
