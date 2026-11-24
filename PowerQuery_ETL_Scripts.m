// =========================================================================
// POWER QUERY ETL TRANSFORMATION SCRIPTS (M CODE)
// Project: Retail Sales Data Preparation and Modelling Using Power BI
// =========================================================================

// -------------------------------------------------------------------------
// QUERY 1: DimCustomer (Extracted from Customers.csv)
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("c:/Users/DELL/Desktop/Retail Sales Data Preparation and Modelling Using Power BI/Customers.csv"), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Trimmed Text" = Table.TransformColumns(#"Promoted Headers",{
        {"CustomerID", Text.Trim, type text},
        {"CustomerName", Text.Trim, type text},
        {"Email", Text.Trim, type text},
        {"City", Text.Trim, type text},
        {"State", Text.Trim, type text},
        {"CustomerSegment", Text.Trim, type text}
    }),
    #"Cleaned Text" = Table.TransformColumns(#"Trimmed Text",{
        {"CustomerName", Text.Clean, type text},
        {"Email", Text.Clean, type text}
    }),
    #"Changed Type" = Table.TransformColumnTypes(#"Cleaned Text",{
        {"CustomerID", type text},
        {"CustomerName", type text},
        {"Email", type text},
        {"Phone", type text},
        {"City", type text},
        {"State", type text},
        {"Country", type text},
        {"CustomerSegment", type text},
        {"AssignedStoreID", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// QUERY 2: DimProduct (Extracted from Products.csv)
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("c:/Users/DELL/Desktop/Retail Sales Data Preparation and Modelling Using Power BI/Products.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Trimmed Text" = Table.TransformColumns(#"Promoted Headers",{
        {"ProductID", Text.Trim, type text},
        {"ProductName", Text.Trim, type text},
        {"Category", Text.Trim, type text},
        {"SubCategory", Text.Trim, type text}
    }),
    #"Changed Type" = Table.TransformColumnTypes(#"Trimmed Text",{
        {"ProductID", type text},
        {"ProductName", type text},
        {"Category", type text},
        {"SubCategory", type text},
        {"CostPrice", Currency.Type},
        {"StandardRetailPrice", Currency.Type}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// QUERY 3A: DimStore (Extracted from SQL Server Database: RetailSalesDB)
// -------------------------------------------------------------------------
let
    // Connect to SQL Server Instance (e.g. localhost, (localdb)\MSSQLLocalDB, or server name)
    Source = Sql.Database("localhost", "RetailSalesDB"),
    dbo_DimStore = Source{[Schema="dbo",Item="DimStore"]}[Data],
    #"Changed Type" = Table.TransformColumnTypes(dbo_DimStore,{
        {"StoreID", type text},
        {"StoreName", type text},
        {"City", type text},
        {"State", type text},
        {"Region", type text},
        {"StoreType", type text},
        {"ManagerName", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// QUERY 3B: DimStore_CSV (Alternative Standalone File Source)
// -------------------------------------------------------------------------
let
    Source = Csv.Document(File.Contents("c:/Users/DELL/Desktop/Retail Sales Data Preparation and Modelling Using Power BI/Stores.csv"), [Delimiter=",", Columns=7, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Trimmed Text" = Table.TransformColumns(#"Promoted Headers",{
        {"StoreID", Text.Trim, type text},
        {"StoreName", Text.Trim, type text},
        {"City", Text.Trim, type text},
        {"State", Text.Trim, type text},
        {"Region", Text.Trim, type text},
        {"StoreType", Text.Trim, type text},
        {"ManagerName", Text.Trim, type text}
    }),
    #"Changed Type" = Table.TransformColumnTypes(#"Trimmed Text",{
        {"StoreID", type text},
        {"StoreName", type text},
        {"City", type text},
        {"State", type text},
        {"Region", type text},
        {"StoreType", type text},
        {"ManagerName", type text}
    })
in
    #"Changed Type"


// -------------------------------------------------------------------------
// QUERY 4: FactSales (Extracted from Sales_Data_50_Records.xlsx and enriched)
// -------------------------------------------------------------------------
let
    // Step 1: Ingest Excel Sales Workbook
    Source = Excel.Workbook(File.Contents("c:/Users/DELL/Desktop/Retail Sales Data Preparation and Modelling Using Power BI/Sales_Data_50_Records.xlsx"), null, true),
    SalesData_Sheet = Source{[Item="SalesData",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(SalesData_Sheet, [PromoteAllScalars=true]),
    
    // Step 2: Clean and Standardize Raw Columns
    #"Cleaned Raw Types" = Table.TransformColumnTypes(#"Promoted Headers",{
        {"Order ID", type text},
        {"Order Date", type date},
        {"Customer Name", type text},
        {"Product", type text},
        {"Quantity", Int64.Type},
        {"Sales Amount (₹)", Currency.Type}
    }),
    #"Trimmed Columns" = Table.TransformColumns(#"Cleaned Raw Types",{
        {"Customer Name", Text.Trim, type text},
        {"Product", Text.Trim, type text}
    }),
    
    // Step 3: Merge with DimCustomer to extract CustomerID and AssignedStoreID
    #"Merged DimCustomer" = Table.NestedJoin(#"Trimmed Columns", {"Customer Name"}, DimCustomer, {"CustomerName"}, "DimCustomer_Joined", JoinKind.LeftOuter),
    #"Expanded DimCustomer" = Table.ExpandTableColumn(#"Merged DimCustomer", "DimCustomer_Joined", {"CustomerID", "AssignedStoreID"}, {"Customer ID", "Store ID"}),
    
    // Step 4: Merge with DimProduct to extract ProductID
    #"Merged DimProduct" = Table.NestedJoin(#"Expanded DimCustomer", {"Product"}, DimProduct, {"ProductName"}, "DimProduct_Joined", JoinKind.LeftOuter),
    #"Expanded DimProduct" = Table.ExpandTableColumn(#"Merged DimProduct", "DimProduct_Joined", {"ProductID"}, {"Product ID"}),
    
    // Step 5: Add Calculated Column Unit Price = Sales Amount / Quantity
    #"Added Unit Price" = Table.AddColumn(#"Expanded DimProduct", "Unit Price", each Number.Round([#"Sales Amount (₹)"] / [Quantity], 2), Currency.Type),
    
    // Step 6: Rename and Standardize Columns
    #"Renamed Columns" = Table.RenameColumns(#"Added Unit Price",{
        {"Order ID", "Sales ID"},
        {"Sales Amount (₹)", "Sales Amount"}
    }),
    
    // Step 7: Remove Redundant Denormalized Descriptive Columns (Customer Name, Product)
    #"Removed Redundant Columns" = Table.RemoveColumns(#"Renamed Columns",{"Customer Name", "Product"}),
    
    // Step 8: Reorder Columns into Standard Fact Table Layout
    #"Reordered Columns" = Table.ReorderColumns(#"Removed Redundant Columns",{
        "Sales ID",
        "Order Date",
        "Customer ID",
        "Product ID",
        "Store ID",
        "Quantity",
        "Unit Price",
        "Sales Amount"
    }),
    
    // Step 9: Final Strict Type Casting
    #"Final Type Cast" = Table.TransformColumnTypes(#"Reordered Columns",{
        {"Sales ID", type text},
        {"Order Date", type date},
        {"Customer ID", type text},
        {"Product ID", type text},
        {"Store ID", type text},
        {"Quantity", Int64.Type},
        {"Unit Price", Currency.Type},
        {"Sales Amount", Currency.Type}
    })
in
    #"Final Type Cast"
