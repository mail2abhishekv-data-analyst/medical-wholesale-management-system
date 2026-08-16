from database import engine
from sqlalchemy import text


def search_medicine(search_text):
    """
    Search medicines by Medicine_Id or Medicine_Name.
    Returns matching medicines.
    """

    sql = text("""
        SELECT
            Medicine_Id,
            Medicine_Name,
            Manufacturer_Name,
            Price,
            Discount_Percent,
            Selling_Price,
            Quantity,
            Pack_Size_Label,
            Type
        FROM Medicine
        WHERE
            Medicine_Id LIKE :search
            OR Medicine_Name LIKE :search
        ORDER BY Medicine_Name;
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

        print("Medicine search failed!")
        print(e)

        return []
def get_medicine(medicine_id):
    """
    Get complete details for one medicine by Medicine_Id.
    """

    sql = text("""
        SELECT
            Medicine_Id,
            Medicine_Name,
            Manufacturer_Name,
            Cost_Price,
            Price,
            Discount_Percent,
            Selling_Price,
            Pack_Size_Label,
            Type,
            Man_Date,
            Expiry_Date,
            Quantity
        FROM Medicine
        WHERE Medicine_Id = :medicine_id;
    """)

    try:

        with engine.connect() as connection:

            result = connection.execute(
                sql,
                {
                    "medicine_id": medicine_id
                }
            )

            row = result.fetchone()

        return row

    except Exception as e:

        print("Medicine lookup failed!")
        print(e)

        return None