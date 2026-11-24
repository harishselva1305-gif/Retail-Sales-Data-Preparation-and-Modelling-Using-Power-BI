-- ==============================================================================
-- Retail Sales Database Setup Script for PostgreSQL (Version 12 - 18+)
-- Target: PostgreSQL / EDB Postgres Advanced Server
-- ==============================================================================

-- 1. Create Schema (or use default public schema)
CREATE SCHEMA IF NOT EXISTS retail;

-- 2. Create DimStore Table
DROP TABLE IF EXISTS retail.dim_store CASCADE;

CREATE TABLE retail.dim_store (
    store_id VARCHAR(10) NOT NULL PRIMARY KEY,
    store_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    region VARCHAR(20) NOT NULL,
    store_type VARCHAR(30) NOT NULL,
    manager_name VARCHAR(50) NOT NULL
);

-- 3. Populate DimStore with 5 Retail Store Locations
INSERT INTO retail.dim_store (store_id, store_name, city, state, region, store_type, manager_name) VALUES
('STR-001', 'TechHub Chennai Flagship', 'Chennai', 'Tamil Nadu', 'South', 'Flagship', 'Rajesh Sharma'),
('STR-002', 'Digital World Bengaluru', 'Bengaluru', 'Karnataka', 'South', 'Superstore', 'Priya Nair'),
('STR-003', 'CyberMart Express Hyderabad', 'Hyderabad', 'Telangana', 'South', 'Express Store', 'Vikram Reddy'),
('STR-004', 'SmartRetail Mega Mumbai', 'Mumbai', 'Maharashtra', 'West', 'Superstore', 'Neha Mehta'),
('STR-005', 'Metro Electronics Delhi', 'Delhi', 'Delhi NCR', 'North', 'Flagship', 'Amit Verma')
ON CONFLICT (store_id) DO NOTHING;

-- 4. Create DimCustomer Table
DROP TABLE IF EXISTS retail.dim_customer CASCADE;

CREATE TABLE retail.dim_customer (
    customer_id VARCHAR(10) NOT NULL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    country VARCHAR(30) NOT NULL,
    customer_segment VARCHAR(30) NOT NULL,
    assigned_store_id VARCHAR(10) REFERENCES retail.dim_store(store_id)
);

-- 5. Create DimProduct Table
DROP TABLE IF EXISTS retail.dim_product CASCADE;

CREATE TABLE retail.dim_product (
    product_id VARCHAR(10) NOT NULL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    cost_price NUMERIC(10, 2) NOT NULL,
    standard_retail_price NUMERIC(10, 2) NOT NULL
);

-- 6. Create FactSales Table
DROP TABLE IF EXISTS retail.fact_sales CASCADE;

CREATE TABLE retail.fact_sales (
    sales_id VARCHAR(20) NOT NULL PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(10) NOT NULL REFERENCES retail.dim_customer(customer_id),
    product_id VARCHAR(10) NOT NULL REFERENCES retail.dim_product(product_id),
    store_id VARCHAR(10) NOT NULL REFERENCES retail.dim_store(store_id),
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    sales_amount NUMERIC(10, 2) NOT NULL
);

-- 7. Verification Query
SELECT * FROM retail.dim_store;
