-- ==============================================================
-- Retail Sales Database Setup Script for Power BI Data Modelling
-- Target Database: Microsoft SQL Server / Azure SQL / PostgreSQL
-- ==============================================================

-- 1. Create Database
CREATE DATABASE RetailSalesDB;
GO

USE RetailSalesDB;
GO

-- 2. Create DimStore Table
IF OBJECT_ID('dbo.DimStore', 'U') IS NOT NULL
    DROP TABLE dbo.DimStore;
GO

CREATE TABLE dbo.DimStore (
    StoreID VARCHAR(10) NOT NULL PRIMARY KEY,
    StoreName VARCHAR(100) NOT NULL,
    City VARCHAR(50) NOT NULL,
    State VARCHAR(50) NOT NULL,
    Region VARCHAR(20) NOT NULL,
    StoreType VARCHAR(30) NOT NULL,
    ManagerName VARCHAR(50) NOT NULL
);
GO

-- 3. Populate DimStore Table
INSERT INTO dbo.DimStore (StoreID, StoreName, City, State, Region, StoreType, ManagerName) VALUES
('STR-001', 'TechHub Chennai Flagship', 'Chennai', 'Tamil Nadu', 'South', 'Flagship', 'Rajesh Sharma'),
('STR-002', 'Digital World Bengaluru', 'Bengaluru', 'Karnataka', 'South', 'Superstore', 'Priya Nair'),
('STR-003', 'CyberMart Express Hyderabad', 'Hyderabad', 'Telangana', 'South', 'Express Store', 'Vikram Reddy'),
('STR-004', 'SmartRetail Mega Mumbai', 'Mumbai', 'Maharashtra', 'West', 'Superstore', 'Neha Mehta'),
('STR-005', 'Metro Electronics Delhi', 'Delhi', 'Delhi NCR', 'North', 'Flagship', 'Amit Verma');
GO

-- 4. Verification Query
SELECT * FROM dbo.DimStore;
GO
