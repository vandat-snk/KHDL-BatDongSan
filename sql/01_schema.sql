PRAGMA foreign_keys = ON;
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
