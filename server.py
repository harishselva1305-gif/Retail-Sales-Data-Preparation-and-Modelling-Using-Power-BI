# ==============================================================================
# RETAIL SALES DATA PREPARATION & MODELLING - LOCAL WEB SERVER
# Avoids Port 8080 (Reserved by EDB PostgreSQL PEM)
# ==============================================================================

import http.server
import socketserver
import webbrowser
import socket
import os
import sys
import json
import csv

# Target ports to try in sequence (skips 8080 used by EDB Postgres PEM and 5432 used by Postgres DB)
PREFERRED_PORTS = [8500, 8501, 8050, 5500, 5000, 8888, 9000]

def find_available_port(ports):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('127.0.0.1', port))
                return port
            except OSError:
                continue
    # If none from preferred, let the OS assign an ephemeral port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def get_kpi_summary():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sales_file = os.path.join(base_dir, 'Cleaned_FactSales.csv')
    if not os.path.exists(sales_file):
        return {"status": "error", "message": "Cleaned_FactSales.csv not found"}
    
    total_sales = 0.0
    total_qty = 0
    orders = set()
    with open(sales_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            total_sales += float(r['Sales Amount'])
            total_qty += int(r['Quantity'])
            orders.add(r['Sales ID'])
    
    total_orders = len(orders)
    aov = (total_sales / total_orders) if total_orders > 0 else 0
    total_cost = 1068940.00
    profit = total_sales - total_cost
    margin = (profit / total_sales * 100) if total_sales > 0 else 0
    
    return {
        "status": "success",
        "total_sales": round(total_sales, 2),
        "total_orders": total_orders,
        "total_quantity": total_qty,
        "average_order_value": round(aov, 2),
        "total_profit": round(profit, 2),
        "profit_margin_pct": round(margin, 2)
    }

class RetailDashboardHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and disable caching so fresh data always loads
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        # API Endpoints
        if self.path == '/api/summary':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            data = get_kpi_summary()
            self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
            return
        
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            status_data = {
                "server": "Retail Sales Analytics Server",
                "status": "online",
                "active_port": self.server.server_address[1],
                "datasets_available": [
                    "Sales_Data_50_Records.xlsx",
                    "Customers.csv",
                    "Products.csv",
                    "Stores.csv",
                    "Cleaned_FactSales.csv"
                ],
                "database_integration": {
                    "sql_server": "RetailSalesDB_Setup.sql",
                    "postgresql": "RetailSalesDB_PostgreSQL_Setup.sql"
                }
            }
            self.wfile.write(json.dumps(status_data, indent=2).encode('utf-8'))
            return

        # Redirect root to index.html
        if self.path == '/' or self.path == '':
            self.path = '/index.html'

        return super().do_GET()

def run_server():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    port = find_available_port(PREFERRED_PORTS)
    url = f"http://localhost:{port}"

    print("=" * 70)
    print(" RETAIL SALES DATA PREPARATION & MODELLING WEB SERVER")
    print("=" * 70)
    print(f" [SUCCESS] Server active at: {url}")
    print(f" [INFO]    Port {port} selected (avoiding port 8080 used by EDB Postgres PEM).")
    print(f" [INFO]    Serving directory: {base_dir}")
    print(f" [INFO]    Datasets loaded: FactSales, DimCustomer, DimProduct, DimStore")
    print(f" [INFO]    API endpoints available:")
    print(f"           - {url}/api/summary")
    print(f"           - {url}/api/status")
    print("=" * 70)
    print(" Opening dashboard in your default browser...")
    print(" Press Ctrl+C to stop the server.")
    print("=" * 70)

    # Launch browser automatically
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f" [NOTE] Open {url} in your browser manually.")

    # Start socket server
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), RetailDashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n [INFO] Server stopped gracefully.")
            sys.exit(0)

if __name__ == '__main__':
    run_server()
