from sqlalchemy import create_engine, text
import urllib.parse


# SQL Server connection details
server = r"ABHISHEK\SQLEXPRESS"
database = "Medical_Wholesale_DB"
driver = "ODBC Driver 17 for SQL Server"


# Connection string
params = urllib.parse.quote_plus(
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(
    f"mssql+pyodbc:///?odbc_connect={params}"
)


# Test connection
try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT DB_NAME() AS DatabaseName")
        )

        row = result.fetchone()

        print("SQL Server connected successfully!")
        print("Database:", row.DatabaseName)

except Exception as e:
    print("Database connection failed!")
    print(e)