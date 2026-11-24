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
