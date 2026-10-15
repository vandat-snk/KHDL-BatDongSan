-- 01: coverage and medians are in Python; SQLite AVG below is explicitly a MEAN.
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
SELECT row_id, area_m2, sale_price_vnd, price_per_m2_vnd
FROM listings
WHERE province_id = ? AND type_id = ?
  AND price_per_m2_vnd BETWEEN ? AND ?
ORDER BY price_per_m2_vnd, row_id LIMIT 100;
