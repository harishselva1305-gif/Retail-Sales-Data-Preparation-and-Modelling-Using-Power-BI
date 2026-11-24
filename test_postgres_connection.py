# ==============================================================================
# POSTGRESQL CONNECTION TEST UTILITY
# Tests connectivity to PostgreSQL (Default port 5432)
# ==============================================================================

import socket
import sys

def check_postgres_port(host='127.0.0.1', port=5432):
    print("=" * 60)
    print(" POSTGRESQL CONNECTION DIAGNOSTIC TOOL")
    print("=" * 60)
    print(f" Checking host: {host} on port: {port}...")
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect((host, port))
        print(f" [SUCCESS] PostgreSQL service is ACTIVE and LISTENING on port {port}!")
        print(" [INFO]    You can connect Power BI to PostgreSQL using:")
        print(f"           - Server:   {host}:{port}")
        print("           - Database: retail_sales_db (or postgres)")
        print("           - Username: postgres")
        return True
    except ConnectionRefusedError:
        print(f" [WARNING] Port {port} is closed. The PostgreSQL service might be stopped.")
        print("           To start it: Windows Services -> postgresql-x64-18 -> Start")
        return False
    except Exception as e:
        print(f" [NOTE] Socket check result: {e}")
        return False
    finally:
        s.close()

if __name__ == '__main__':
    check_postgres_port()
