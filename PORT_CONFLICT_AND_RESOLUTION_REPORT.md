# Technical Investigation & Resolution Report: EDB PostgreSQL Port 8080 Conflict & Dashboard Launch

**Project:** Retail Sales Data Preparation and Modelling Using Power BI  
**Author:** Antigravity AI Engineering Assistant  
**Date & Time:** November 20, 2026  
**Status:** RESOLVED & VERIFIED  

---

## 1. Executive Summary & Root Cause Discovery

### 1.1 The Reported Problem
When navigating to `http://localhost:8080`, the browser displayed the **EnterpriseDB (EDB) POSTGRES** logo with the text:
> *"Server is up and running."*

Instead of showing the Retail Sales Data Preparation and Modelling website, the EDB PostgreSQL web service default page was rendered.

```
┌────────────────────────────────────────────────────────────────────────┐
│                              SCREENSHOT AUDIT                          │
├────────────────────────────────────────────────────────────────────────┤
│ Browser Tab:  localhost:8080                                           │
│ Header Logo:  EDB POSTGRES                                             │
│ Body Content: "Server is up and running."                              │
│ Source File:  C:\Program Files\edb\pem\httpd\apache\www\index.html     │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.2 In-Depth Forensic Investigation
By conducting a system-level audit of the host environment, we identified the root cause:

1. **Active EDB PEM Installation Detected:**  
   The host machine has **Postgres Enterprise Manager (PEM)** installed at:  
   `C:\Program Files\edb\pem\`  
   alongside **PostgreSQL 18** at:  
   `C:\Program Files\PostgreSQL\18\`

2. **Apache HTTP Server Configuration Inspection:**  
   We inspected the Apache configuration file:  
   `C:\Program Files\edb\pem\httpd\apache\conf\httpd.conf`  
   - **Line 54:** `Listen 0.0.0.0:8080`
   - **Line 257:** `DocumentRoot "${SRVROOT}/www"`

3. **Inspection of the Apache Document Root:**  
   We read `C:\Program Files\edb\pem\httpd\apache\www\index.html`:
   ```html
   <html>
   <a href='http://www.enterprisedb.com'><img src='images/edblogo.png' border=0></a></br></br>
   Server is up and running.</br>
   </html>
   ```
   **Conclusion:** Port 8080 is permanently bound by EDB PEM's Apache HTTP daemon. Any application attempting to listen on port 8080 is blocked by Windows (`WinError 10013`), and visiting `localhost:8080` in Chrome connects directly to EDB's Apache web server.

---

## 2. Multi-Service Architecture & Resolution Strategy

To respect enterprise guidelines, we did not alter or break the existing PostgreSQL or EDB PEM installations. Instead, we established a **dedicated, conflict-free multi-service port architecture**:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                    ISOLATED SERVICE PORT ARCHITECTURE                        │
├─────────────────────┬───────────┬────────────────────────────────────────────┤
│ Service             │ Port      │ Role & Purpose                             │
├─────────────────────┼───────────┼────────────────────────────────────────────┤
│ Retail Dashboard    │ Port 8500 │ Dedicated Retail Sales Web Server (Python) │
│ EDB Postgres PEM    │ Port 8080 │ Pre-existing Apache HTTP Console           │
│ PostgreSQL Database │ Port 5432 │ Relational Database Engine (PostgreSQL 18) │
│ Power BI Desktop    │ IPC / TOM │ Direct Tabular Model (.pbip / model.bim)   │
└─────────────────────┴───────────┴────────────────────────────────────────────┘
```

---

## 3. Implementation Details: Changes & Enhancements

### 3.1 Dedicated Local Server Engine (`server.py`)
Created a custom HTTP server engine:
- **Port Management:** Evaluates preferred ports (`8500`, `8501`, `8050`, `5500`) and safely binds to the first unoccupied port, explicitly skipping `8080` and `5432`.
- **Automated Browser Launch:** Automatically triggers the default system browser (Chrome/Edge) to `http://localhost:8500`.
- **Integrated REST APIs:**
  - `GET /api/summary`: Returns live aggregated KPIs directly from `Cleaned_FactSales.csv` (Total Sales: ₹1,367,322.36, Orders: 50, Units: 142, Profit: ₹298,382.36).
  - `GET /api/status`: Provides server health, port information, and dataset status.
- **CORS & No-Cache Headers:** Configured to guarantee immediate visual refreshes without stale browser caching.

### 3.2 Fixed Startup Script (`Start_Website.bat`)
Updated the startup script with logging and error-recovery:
```bat
@echo off
title Retail Sales Power BI Project Dashboard Server
cls
echo ======================================================================
echo    RETAIL SALES DATA PREPARATION AND MODELLING USING POWER BI
echo ======================================================================
echo.
echo [1/3] Port Configuration:
echo       - Port 8080 is reserved by EDB PostgreSQL PEM.
echo       - Retail Sales Dashboard runs on: http://localhost:8500
echo.
echo [2/3] Opening Dashboard in your browser: http://localhost:8500 ...
start "" "http://localhost:8500"
echo.
echo [3/3] Starting Local Web Server on Port 8500...
echo       (Keep this command window open while viewing the dashboard)
echo.
python "%~dp0server.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FALLBACK] Python server command finished or not in PATH.
    echo Opening index.html directly in your default browser...
    start "" "%~dp0index.html"
)
pause
```

### 3.3 Enhanced Frontend Interface (`index.html`)
- Built-in fallback styling to guarantee complete rendering even if internet access is interrupted.
- Interactive tab switching between all 3 required analytical dashboards:
  1. **Dashboard 1: Sales Overview** (4 KPI Cards, Stacked Bar Chart, Monthly Line Chart, Regional Share Pie Chart).
  2. **Dashboard 2: Product Performance** (5 KPI Cards, Category Monthly Line Chart, Revenue Share Donut Chart, SKU Units Sold Pie Chart).
  3. **Dashboard 3: Profit & Business Analysis** (5 KPI Cards, COGS vs Gross Profit Stacked Bar Chart, Revenue vs Profit Line Chart, Category Profit Donut Chart).
- Live interactive Slicers for Store (`STR-001` through `STR-005`) and Product Category.

### 3.4 PostgreSQL Relational Database Assets
- **`RetailSalesDB_PostgreSQL_Setup.sql`:** Provided DDL and DML scripts creating schema `retail`, dimension tables `dim_store`, `dim_customer`, `dim_product`, and transaction table `fact_sales`.
- **`test_postgres_connection.py`:** Standalone Python script for validating database connectivity on port 5432.

---

## 4. Verification & Testing Evidence

We performed an end-to-end automated server test probing `http://127.0.0.1:8500`:

```text
======================================================================
 RETAIL SALES DATA PREPARATION & MODELLING WEB SERVER
======================================================================
 [SUCCESS] Server active at: http://localhost:8500
 [INFO]    Port 8500 selected (avoiding port 8080 used by EDB Postgres PEM).
 [INFO]    Serving directory: C:\Users\DELL\Desktop\Retail Sales Data Preparation and Modelling Using Power BI
 [INFO]    Datasets loaded: FactSales, DimCustomer, DimProduct, DimStore
 [INFO]    API endpoints available:
           - http://localhost:8500/api/summary
           - http://localhost:8500/api/status
======================================================================
PROBE STATUS:        200 OK
PROBE TITLE FOUND:   True
RETAIL SALES FOUND:  True
SERVER TEST RESULT:  PASSED 100%
```

---

## 5. How to View Your Retail Sales Dashboard

### Option 1: Run the Startup Batch File (Recommended)
1. In your project folder, double-click:  
   👉 **`Start_Website.bat`**
2. The server will start on **Port 8500** and automatically open **`http://localhost:8500`** in your browser.
3. Your Retail Sales Dashboard will display immediately (not the EDB PostgreSQL page).

### Option 2: Direct Local Browser Link
You can also open the project without running any server:  
👉 **`index.html`** (Right-click > Open with > Google Chrome)

### Option 3: Direct Power BI Desktop Model
To explore or edit the full Tabular Model:  
👉 **`Retail_Sales_Model.pbip`** (Double-click to open in Power BI Desktop)

---

## 6. Summary of Key Financial Data Displayed

| Metric Name | Dashboard Value | Status |
| :--- | :--- | :--- |
| **Total Sales Revenue** | **₹1,367,322.36 (₹13.67 Lakhs)** | Verified across all 50 transactions |
| **Total Unique Orders** | **50 Orders** | Verified |
| **Total Units Sold** | **142 Units** | Verified |
| **Average Order Value (AOV)** | **₹27,346.45** | Verified |
| **Total Cost of Goods (COGS)**| **₹1,068,940.00** | Verified |
| **Total Gross Profit** | **₹298,382.36** | Verified |
| **Overall Profit Margin** | **21.82%** | Verified |
| **Peak Sales Month** | **February 2026 (₹5,52,318.17)** | 40.4% of total annual sales |
| **Top Store Branch** | **TechHub Chennai (₹4,03,105.53)** | 29.5% of total sales |
