CREATE INDEX idx_listings_search ON listings(province_id, type_id, price_per_m2_vnd, row_id);
ANALYZE;
