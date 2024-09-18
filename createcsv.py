import csv

# Define the sales inventory data
inventory_data = [
    ["Product ID", "Product Name", "Category", "Quantity in Stock", "Unit Price", "Total Sales"],
    [101, "Wireless Mouse", "Electronics", 150, 20.99, 3148.50],
    [102, "Keyboard", "Electronics", 80, 45.50, 3640.00],
    [103, "Monitor", "Electronics", 60, 150.00, 9000.00],
    [104, "Laptop", "Electronics", 30, 750.00, 22500.00],
    [105, "Smartphone", "Electronics", 100, 550.00, 27500.00],
    [106, "Notebook", "Stationery", 500, 3.50, 1750.00],
    [107, "Pen", "Stationery", 1000, 1.25, 1250.00],
    [108, "Desk Chair", "Furniture", 20, 85.00, 1700.00],
    [109, "Office Desk", "Furniture", 10, 200.00, 2000.00],
    [110, "Water Bottle", "Accessories", 300, 12.00, 3600.00]
]

# Create the CSV file and write the data
with open('sales_inventory.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(inventory_data)

print("CSV file 'sales_inventory.csv' created successfully.")

