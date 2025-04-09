import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_column_names(sheet):
    """Helper function to get column names from a worksheet"""
    if not sheet.max_row:
        return []
    return [cell.value for cell in sheet[1]]

def generate_mock_excel(filename: str = "mock_data.xlsx"):
    """
    Generates an Excel file with multiple sheets containing mock data
    """
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Sheet 1: Sales Data
    sales_data = {
        'Date': [datetime.now() - timedelta(days=x) for x in range(10)],
        'Product': ['Product A', 'Product B', 'Product C', 'Product A', 'Product B',
                   'Product C', 'Product A', 'Product B', 'Product C', 'Product A'],
        'Units': np.random.randint(50, 500, size=10),
        'Price': np.random.uniform(10.0, 100.0, size=10).round(2),
        'Revenue': np.random.uniform(1000.0, 10000.0, size=10).round(2)
    }
    df_sales = pd.DataFrame(sales_data)
    df_sales.to_excel(writer, sheet_name='Sales Data', index=False)

    # Sheet 2: Employee Information
    employee_data = {
        'Employee ID': [f'EMP{i:03d}' for i in range(1, 11)],
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Davis',
                'Eva Wilson', 'Frank Miller', 'Grace Lee', 'Henry Ford', 'Ivy Chen'],
        'Department': ['IT', 'HR', 'Sales', 'Marketing', 'IT',
                      'Finance', 'Sales', 'HR', 'Marketing', 'IT'],
        'Salary': np.random.uniform(50000.0, 100000.0, size=10).round(2),
        'Join Date': [datetime.now() - timedelta(days=x*30) for x in range(10)]
    }
    df_employees = pd.DataFrame(employee_data)
    df_employees.to_excel(writer, sheet_name='Employee Info', index=False)

    # Sheet 3: Inventory Status
    inventory_data = {
        'Item Code': [f'ITEM{i:03d}' for i in range(1, 16)],
        'Item Name': [f'Product {chr(65+i)}' for i in range(15)],
        'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Tools'], 15),
        'Quantity': np.random.randint(0, 1000, size=15),
        'Last Updated': [datetime.now() - timedelta(hours=x*2) for x in range(15)],
        'Status': np.random.choice(['In Stock', 'Low Stock', 'Out of Stock'], 15)
    }
    df_inventory = pd.DataFrame(inventory_data)
    df_inventory.to_excel(writer, sheet_name='Inventory', index=False)

    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book

    # Add some formatting
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#D9D9D9',
        'border': 1
    })

    # Apply formatting to each sheet
    for sheet_name in writer.sheets:
        worksheet = writer.sheets[sheet_name]
        # Get column names from the DataFrame
        if sheet_name == 'Sales Data':
            columns = df_sales.columns
        elif sheet_name == 'Employee Info':
            columns = df_employees.columns
        else:
            columns = df_inventory.columns
            
        for col_num, value in enumerate(columns):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)  # Set column width

    # Save the Excel file
    writer.close()

    return filename

if __name__ == "__main__":
    generate_mock_excel()
