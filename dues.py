from database import engine
from sqlalchemy import text


def get_due(order_id):
    """
    Get outstanding due information for an order.
    """

    sql = text("""
        SELECT
            Dues_Id,
            Order_Id,
            Retailer_Id,
            Shop_Name,
            Order_Amount,
            Paid_Amount,
            Dues_Amount,
            Due_Date,
            Payment_Date,
            Payment_Status
        FROM Dues
        WHERE Order_Id = :order_id;
    """)

    try:

        with engine.connect() as connection:

            result = connection.execute(
                sql,
                {
                    "order_id": order_id
                }
            )

            row = result.fetchone()

        return row

    except Exception as e:

        print("Due lookup failed!")
        print(e)

        return None


def record_due_payment(order_id, payment_amount, payment_date=None):
    """
    Record a payment against an existing due
    using sp_RecordDuePayment.
    """

    if payment_date is None:

        sql = text("""
            EXEC sp_RecordDuePayment
                @Order_Id = :order_id,
                @Payment_Amount = :payment_amount;
        """)

    else:

        sql = text("""
            EXEC sp_RecordDuePayment
                @Order_Id = :order_id,
                @Payment_Amount = :payment_amount,
                @Payment_Date = :payment_date;
        """)

    try:

        with engine.begin() as connection:

            result = connection.execute(
                sql,
                {
                    "order_id": order_id,
                    "payment_amount": payment_amount,
                    "payment_date": payment_date
                }
            )

        return True, "Payment recorded successfully."

    except Exception as e:

        return False, str(e)