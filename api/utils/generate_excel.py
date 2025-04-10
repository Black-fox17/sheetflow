import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from api.v1.services.row import row_service
from api.db.database import get_db
from sqlalchemy.orm import Session

def generate_db_excel(db: Session, template_id:str, filename:str = "result.xlsx"):
    # Create a Pandas Excel writer using XlsxWriter as the engine
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    result_data_db = row_service.fetch(db, template_id)
    print(result_data_db)
    
    # Get the xlsxwriter workbook object
    workbook = writer.book
    
    # Add some formatting
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'bg_color': '#D9D9D9',
        'border': 1
    })
    
    # Process each sheet
    for sheet_name, data in result_data_db.items():
        df_data = pd.DataFrame(data)
        df_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Get the worksheet object
        worksheet = writer.sheets[sheet_name]
        
        # Apply formatting to headers
        for col_num, value in enumerate(df_data.columns):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 15)  # Set column width
    
    # Save the Excel file
    writer.close()
    
    return filename
