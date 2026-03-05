# import urllib

# class Config:
#     SECRET_KEY = 'igstore_secret_key_123'
#     # Chuỗi kết nối SQL Server (Windows Authentication)
#     connection_string = (
#         "DRIVER={ODBC Driver 17 for SQL Server};"
#         "SERVER=LAPTOP-PJ5RVOO6\SQLEXPRESS;" 
#         "DATABASE=IGStoreDB;"
#         "Trusted_Connection=yes;"
#     )
#     params = urllib.parse.quote_plus(connection_string)
#     SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
import os

# Lấy đường dẫn thư mục gốc của dự án (nơi chứa file config.py)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'igstore_secret_key_123'
    
    # --- THAY ĐỔI Ở ĐÂY ---
    # Thay vì dùng MSSQL, ta dùng SQLite trỏ vào file database.db
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    # ----------------------
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False