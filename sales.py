from database import engine
from sqlalchemy import text


def create_sale(
    customer_type,
    retailer_id,
    name,
    address,
    city,
    phone_no,
    paid_amount,
    round_off_amount,
    sale_items
):
    """
    Create a sale using SQL Server stored procedure sp_CreateSale.

    sale_items example:
    [
        {
            "medicine_id": "MED000001",
            "quantity": 2
        },
        {
            "medicine_id": "MED000005",
            "quantity": 5
        }
    ]
    """

    # Build the SaleDetailType data
    values = []

    for item in sale_items:

        medicine_id = item["medicine_id"]
        quantity = item["quantity"]

        values.append(
            f"('{medicine_id}', {quantity})"
        )

    values_sql = ", ".join(values)

    sql = text(f"""
        DECLARE @Items dbo.SaleDetailType;

        INSERT INTO @Items
        (
            Medicine_Id,
            Quantity
        )
        VALUES
        {values_sql};

        EXEC sp_CreateSale
            @Customer_Type = :customer_type,
            @Retailer_Id = :retailer_id,
            @Name = :name,
            @Address = :address,
            @City = :city,
            @Phone_No = :phone_no,
            @Paid_Amount = :paid_amount,
            @Round_Off_Amount = :round_off_amount,
            @SaleItems = @Items;
    """)

    try:

        with engine.begin() as connection:

            connection.execute(
                sql,
                {
                    "customer_type": customer_type,
                    "retailer_id": retailer_id,
                    "name": name,
                    "address": address,
                    "city": city,
                    "phone_no": phone_no,
                    "paid_amount": paid_amount,
                    "round_off_amount": round_off_amount
                }
            )

        return True, "Sale created successfully."

    except Exception as e:

        return False, str(e)
def get_retailers():

    query = text("""
        SELECT
            Retailer_Id,
            Shop_Name,
            Phone_No
        FROM Retailer
        WHERE Status = 'Active'
        ORDER BY Shop_Name
    """)

    with engine.connect() as connection:

        result = connection.execute(query)

        retailers = result.fetchall()

    return retailers