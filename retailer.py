from database import engine
from sqlalchemy import text


def search_retailer(search_text):
    """
    Search retailers by Retailer_Id, Shop_Name, or Phone_No.
    """

    sql = text("""
        SELECT
            Retailer_Id,
            Shop_Name,
            Proprietor_Name,
            Address,
            City,
            State,
            Pin_Code,
            Phone_No,
            Status
        FROM Retailer
        WHERE
            CAST(Retailer_Id AS VARCHAR(20)) LIKE :search
            OR Shop_Name LIKE :search
            OR Phone_No LIKE :search
        ORDER BY Shop_Name;
    """)

    search_pattern = f"%{search_text}%"

    try:

        with engine.connect() as connection:

            result = connection.execute(
                sql,
                {
                    "search": search_pattern
                }
            )

            rows = result.fetchall()

        return rows

    except Exception as e:

        print("Retailer search failed!")
        print(e)

        return []
def get_retailer(retailer_id):
    """
    Get complete details for one retailer by Retailer_Id.
    """

    sql = text("""
        SELECT
            Retailer_Id,
            Shop_Name,
            Proprietor_Name,
            Address,
            City,
            State,
            Pin_Code,
            Phone_No,
            Status
        FROM Retailer
        WHERE Retailer_Id = :retailer_id;
    """)

    try:

        with engine.connect() as connection:

            result = connection.execute(
                sql,
                {
                    "retailer_id": retailer_id
                }
            )

            row = result.fetchone()

        return row

    except Exception as e:

        print("Retailer lookup failed!")
        print(e)

        return None