import json
import os

base_dir = "c:/Users/DELL/Desktop/Retail Sales Data Preparation and Modelling Using Power BI"

dim_customer_m = (
    'let\n'
    '    Source = Csv.Document(File.Contents("' + base_dir + '/Customers.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"CustomerID", type text}, {"CustomerName", type text}, {"Email", type text}, {"Phone", type text}, {"City", type text}, {"State", type text}, {"Country", type text}, {"CustomerSegment", type text}, {"AssignedStoreID", type text}})\n'
    'in\n'
    '    #"Changed Type"'
)

dim_product_m = (
    'let\n'
    '    Source = Csv.Document(File.Contents("' + base_dir + '/Products.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"ProductID", type text}, {"ProductName", type text}, {"Category", type text}, {"SubCategory", type text}, {"CostPrice", Currency.Type}, {"StandardRetailPrice", Currency.Type}})\n'
    'in\n'
    '    #"Changed Type"'
)

dim_store_m = (
    'let\n'
    '    Source = Csv.Document(File.Contents("' + base_dir + '/Stores.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"StoreID", type text}, {"StoreName", type text}, {"City", type text}, {"State", type text}, {"Region", type text}, {"StoreType", type text}, {"ManagerName", type text}})\n'
    'in\n'
    '    #"Changed Type"'
)

fact_sales_m = (
    'let\n'
    '    Source = Csv.Document(File.Contents("' + base_dir + '/Cleaned_FactSales.csv"), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),\n'
    '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),\n'
    '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"Sales ID", type text}, {"Order Date", type date}, {"Customer ID", type text}, {"Product ID", type text}, {"Store ID", type text}, {"Quantity", Int64.Type}, {"Unit Price", Currency.Type}, {"Sales Amount", Currency.Type}})\n'
    'in\n'
    '    #"Changed Type"'
)

model_bim = {
    "name": "Retail_Sales_Model",
    "compatibilityLevel": 1550,
    "model": {
        "culture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True
        },
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "tables": [
            {
                "name": "DimCustomer",
                "columns": [
                    {"name": "CustomerID", "dataType": "string", "isNullable": False, "sourceColumn": "CustomerID"},
                    {"name": "CustomerName", "dataType": "string", "isNullable": True, "sourceColumn": "CustomerName"},
                    {"name": "Email", "dataType": "string", "isNullable": True, "sourceColumn": "Email"},
                    {"name": "Phone", "dataType": "string", "isNullable": True, "sourceColumn": "Phone"},
                    {"name": "City", "dataType": "string", "isNullable": True, "sourceColumn": "City"},
                    {"name": "State", "dataType": "string", "isNullable": True, "sourceColumn": "State"},
                    {"name": "Country", "dataType": "string", "isNullable": True, "sourceColumn": "Country"},
                    {"name": "CustomerSegment", "dataType": "string", "isNullable": True, "sourceColumn": "CustomerSegment"},
                    {"name": "AssignedStoreID", "dataType": "string", "isNullable": True, "sourceColumn": "AssignedStoreID"}
                ],
                "partitions": [
                    {
                        "name": "DimCustomer",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [dim_customer_m]
                        }
                    }
                ]
            },
            {
                "name": "DimProduct",
                "columns": [
                    {"name": "ProductID", "dataType": "string", "isNullable": False, "sourceColumn": "ProductID"},
                    {"name": "ProductName", "dataType": "string", "isNullable": True, "sourceColumn": "ProductName"},
                    {"name": "Category", "dataType": "string", "isNullable": True, "sourceColumn": "Category"},
                    {"name": "SubCategory", "dataType": "string", "isNullable": True, "sourceColumn": "SubCategory"},
                    {"name": "CostPrice", "dataType": "decimal", "formatString": "\"₹\"#,0.00", "sourceColumn": "CostPrice"},
                    {"name": "StandardRetailPrice", "dataType": "decimal", "formatString": "\"₹\"#,0.00", "sourceColumn": "StandardRetailPrice"}
                ],
                "partitions": [
                    {
                        "name": "DimProduct",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [dim_product_m]
                        }
                    }
                ]
            },
            {
                "name": "DimStore",
                "columns": [
                    {"name": "StoreID", "dataType": "string", "isNullable": False, "sourceColumn": "StoreID"},
                    {"name": "StoreName", "dataType": "string", "isNullable": True, "sourceColumn": "StoreName"},
                    {"name": "City", "dataType": "string", "isNullable": True, "sourceColumn": "City"},
                    {"name": "State", "dataType": "string", "isNullable": True, "sourceColumn": "State"},
                    {"name": "Region", "dataType": "string", "isNullable": True, "sourceColumn": "Region"},
                    {"name": "StoreType", "dataType": "string", "isNullable": True, "sourceColumn": "StoreType"},
                    {"name": "ManagerName", "dataType": "string", "isNullable": True, "sourceColumn": "ManagerName"}
                ],
                "partitions": [
                    {
                        "name": "DimStore",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [dim_store_m]
                        }
                    }
                ]
            },
            {
                "name": "FactSales",
                "columns": [
                    {"name": "Sales ID", "dataType": "string", "isNullable": False, "sourceColumn": "Sales ID"},
                    {"name": "Order Date", "dataType": "dateTime", "formatString": "yyyy-mm-dd", "sourceColumn": "Order Date"},
                    {"name": "Customer ID", "dataType": "string", "isNullable": False, "sourceColumn": "Customer ID"},
                    {"name": "Product ID", "dataType": "string", "isNullable": False, "sourceColumn": "Product ID"},
                    {"name": "Store ID", "dataType": "string", "isNullable": False, "sourceColumn": "Store ID"},
                    {"name": "Quantity", "dataType": "int64", "formatString": "0", "sourceColumn": "Quantity"},
                    {"name": "Unit Price", "dataType": "decimal", "formatString": "\"₹\"#,0.00", "sourceColumn": "Unit Price"},
                    {"name": "Sales Amount", "dataType": "decimal", "formatString": "\"₹\"#,0.00", "sourceColumn": "Sales Amount"}
                ],
                "measures": [
                    {"name": "Total Sales", "expression": "SUM(FactSales[Sales Amount])", "formatString": "\"₹\"#,0.00"},
                    {"name": "Total Quantity", "expression": "SUM(FactSales[Quantity])", "formatString": "#,0"},
                    {"name": "Total Orders", "expression": "DISTINCTCOUNT(FactSales[Sales ID])", "formatString": "#,0"},
                    {"name": "Average Order Value", "expression": "DIVIDE([Total Sales], [Total Orders], 0)", "formatString": "\"₹\"#,0.00"},
                    {"name": "Average Unit Price", "expression": "DIVIDE([Total Sales], [Total Quantity], 0)", "formatString": "\"₹\"#,0.00"},
                    {"name": "Total Cost", "expression": "SUMX(FactSales, FactSales[Quantity] * RELATED(DimProduct[CostPrice]))", "formatString": "\"₹\"#,0.00"},
                    {"name": "Total Profit", "expression": "[Total Sales] - [Total Cost]", "formatString": "\"₹\"#,0.00"},
                    {"name": "Profit Margin %", "expression": "DIVIDE([Total Profit], [Total Sales], 0)", "formatString": "0.00%"},
                    {"name": "Total Products", "expression": "DISTINCTCOUNT(DimProduct[ProductID])", "formatString": "#,0"},
                    {"name": "Units Per Order", "expression": "DIVIDE([Total Quantity], [Total Orders], 0)", "formatString": "0.00"},
                    {"name": "Profit Per Order", "expression": "DIVIDE([Total Profit], [Total Orders], 0)", "formatString": "\"₹\"#,0.00"},
                    {"name": "ROI Return on Cost %", "expression": "DIVIDE([Total Profit], [Total Cost], 0)", "formatString": "0.00%"},
                    {"name": "Sales YTD", "expression": "TOTALYTD([Total Sales], DimDate[Date])", "formatString": "\"₹\"#,0.00"}
                ],
                "partitions": [
                    {
                        "name": "FactSales",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [fact_sales_m]
                        }
                    }
                ]
            },
            {
                "name": "DimDate",
                "dataCategory": "Time",
                "columns": [
                    {"name": "Date", "dataType": "dateTime", "isKey": True, "formatString": "yyyy-mm-dd", "sourceColumn": "[Date]"},
                    {"name": "Year", "dataType": "int64", "sourceColumn": "[Year]"},
                    {"name": "Month Number", "dataType": "int64", "sourceColumn": "[Month Number]"},
                    {"name": "Month Name", "dataType": "string", "sortByColumn": "Month Number", "sourceColumn": "[Month Name]"},
                    {"name": "Month Short", "dataType": "string", "sortByColumn": "Month Number", "sourceColumn": "[Month Short]"},
                    {"name": "Quarter", "dataType": "string", "sourceColumn": "[Quarter]"},
                    {"name": "Day of Month", "dataType": "int64", "sourceColumn": "[Day of Month]"},
                    {"name": "Day of Week", "dataType": "string", "sourceColumn": "[Day of Week]"},
                    {"name": "Is Weekend", "dataType": "string", "sourceColumn": "[Is Weekend]"}
                ],
                "partitions": [
                    {
                        "name": "DimDate",
                        "mode": "import",
                        "source": {
                            "type": "calculated",
                            "expression": [
                                'ADDCOLUMNS (\n    CALENDAR ( DATE(2026, 1, 1), DATE(2026, 12, 31) ),\n    "Year", YEAR([Date]),\n    "Month Number", MONTH([Date]),\n    "Month Name", FORMAT([Date], "MMMM"),\n    "Month Short", FORMAT([Date], "MMM"),\n    "Quarter", "Q" & FORMAT([Date], "Q"),\n    "Day of Month", DAY([Date]),\n    "Day of Week", FORMAT([Date], "dddd"),\n    "Is Weekend", IF(WEEKDAY([Date], 2) >= 6, "Weekend", "Weekday")\n)'
                            ]
                        }
                    }
                ]
            }
        ],
        "relationships": [
            {
                "name": "rel_Customer_FactSales",
                "fromTable": "FactSales",
                "fromColumn": "Customer ID",
                "toTable": "DimCustomer",
                "toColumn": "CustomerID"
            },
            {
                "name": "rel_Product_FactSales",
                "fromTable": "FactSales",
                "fromColumn": "Product ID",
                "toTable": "DimProduct",
                "toColumn": "ProductID"
            },
            {
                "name": "rel_Store_FactSales",
                "fromTable": "FactSales",
                "fromColumn": "Store ID",
                "toTable": "DimStore",
                "toColumn": "StoreID"
            },
            {
                "name": "rel_Date_FactSales",
                "fromTable": "FactSales",
                "fromColumn": "Order Date",
                "toTable": "DimDate",
                "toColumn": "Date"
            }
        ]
    }
}

with open("Retail_Sales_Model.Dataset/model.bim", "w", encoding="utf-8") as f:
    json.dump(model_bim, f, indent=2)

print("Updated model.bim with all new analytical DAX measures!")
