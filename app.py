import streamlit as st
import pandas as pd
from sqlalchemy import text
import plotly.express as px
from database import engine
from datetime import date


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Medical Wholesale Management System",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def get_medicines():

    query = text("""
        SELECT
            Medicine_Id,
            Medicine_Name
        FROM Medicine
        ORDER BY Medicine_Name
    """)

    with engine.connect() as connection:
        return connection.execute(query).fetchall()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main application background */
    .stApp {
        background-color: #FDF5E6;
    }

    /* Main content */
    .main {
        background-color: #FDF5E6;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFDF8;
        border-right: 1px solid #E0D8C8;
    }

    /* Sidebar title */
        section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        height: 52px;
        border: none;
        border-radius: 10px;
        background-color: #FDF5E6;
        color: #263238;
        font-size: 15px;
        font-weight: 600;
        text-align: left;
        padding-left: 18px;
        margin-bottom: 8px;
        box-shadow: none;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #D9F7F8;
        color: #008B8F;
        border: none;
    }

    /* Header */
    .app-header {
        background-color: #00BFC4;
        padding: 18px 25px;
        border-radius: 10px;
        margin-bottom: 25px;
    }

    .app-title {
        color: white;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
    }

    .app-subtitle {
        color: white;
        font-size: 14px;
        margin-top: 4px;
    }

    .page-subtitle {
        color: #607D8B;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* KPI cards */
    .kpi-card {
        background-color: #FFFDF8;
        border: 1px solid #E0D8C8;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        min-height: 120px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    .kpi-title {
        color: #607D8B;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #008B8F;
        font-size: 28px;
        font-weight: 700;
        margin-top: 8px;
    }

    /* Section cards */
    .section-card {
        background-color: #FFFDF8;
        border: 1px solid #E0D8C8;
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">💊 VERMA MEDICAL</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    if "page" not in st.session_state:
        st.session_state.page = "🏠 Dashboard"


    def navigation_tile(label):
        if st.button(
                label,
                key=f"nav_{label}",
                use_container_width=True
        ):
            st.session_state.page = label


    navigation_tile("🏠 Dashboard")
    navigation_tile("🛒 Sales")
    navigation_tile("💊 Medicine")
    navigation_tile("🏪 Retailers & Payments")

    page = st.session_state.page

    st.markdown("---")
    st.caption("VERMA Medical Wholesale Management System")
    st.caption("SQL Server + Python + Streamlit")
    st.markdown("---")

    st.markdown("---")

    st.caption("DEVELOPED BY")

    st.markdown(
        "**Abhishek Verma**"
    )

    st.caption(
        "Data Analyst"
    )

    st.caption(
        "Excel | SQL | Power BI | Python"
    )

# =========================================================
# APPLICATION HEADER
# =========================================================

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">
            VERMA MEDICAL WHOLESALE MANAGEMENT SYSTEM
        </div>
        <div class="app-subtitle">
            Sales, Inventory, Retailers & Payment Management
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    # ---------------------------------------------------------
    # KPI QUERY
    # ---------------------------------------------------------

    dashboard_kpi_query = text("""
        SELECT
            ISNULL(SUM(Order_Amount), 0) AS Total_Sale,
            COUNT(DISTINCT Order_Id) AS Total_Orders,
            ISNULL(SUM(Dues_Amount), 0) AS Total_Dues
        FROM Sales
    """)

    # ---------------------------------------------------------
    # ACTIVE RETAILERS QUERY
    # ---------------------------------------------------------

    active_retailers_query = text("""
        SELECT COUNT(*)
        FROM Retailer
        WHERE Status = 'Active'
    """)

    # ---------------------------------------------------------
    # GET KPI VALUES
    # ---------------------------------------------------------

    with engine.connect() as connection:

        kpi_result = connection.execute(
            dashboard_kpi_query
        ).fetchone()

        active_retailers = connection.execute(
            active_retailers_query
        ).scalar() or 0

    # ---------------------------------------------------------
    # KPI CALCULATIONS
    # ---------------------------------------------------------

    total_sale = float(
        kpi_result.Total_Sale or 0
    )

    total_orders = int(
        kpi_result.Total_Orders or 0
    )

    total_dues = float(
        kpi_result.Total_Dues or 0
    )

    active_retailers = int(
        active_retailers
    )

    # =========================================================
    # KPI CARDS
    # =========================================================

    col1, col2, col3, col4 = st.columns(4)

    # ---------------------------------------------------------
    # 1. TODAY'S SALE
    # ---------------------------------------------------------

    with col1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Sale</div>
                <div class="kpi-value">
                    ₹ {total_sale:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # 2. TODAY'S ORDERS
    # ---------------------------------------------------------

    with col2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">
                    {total_orders:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # 3. TODAY'S DUES
    # ---------------------------------------------------------

    with col3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Dues</div>
                <div class="kpi-value">
                    ₹ {total_dues:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------------------------------------------------------
    # 4. ACTIVE RETAILERS
    # ---------------------------------------------------------

    with col4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Active Retailers</div>
                <div class="kpi-value">
                    {active_retailers:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("")

    # =========================================================
    # DASHBOARD CHARTS
    # =========================================================

    # ---------------------------------------------------------
    # SALES TREND QUERY
    # ---------------------------------------------------------

    sales_trend_query = text("""
        SELECT
            CAST(Date AS DATE) AS Sale_Date,
            SUM(Order_Amount) AS Total_Sales
        FROM Sales
        GROUP BY CAST(Date AS DATE)
        ORDER BY Sale_Date
    """)

    # ---------------------------------------------------------
    # TOP SELLING MEDICINES QUERY
    # ---------------------------------------------------------

    top_medicines_query = text("""
        SELECT TOP 10
            Medicine_Name,
            SUM(Quantity) AS Total_Sold
        FROM Sales_Details
        GROUP BY Medicine_Name
        ORDER BY Total_Sold DESC
    """)

    # ---------------------------------------------------------
    # GET CHART DATA
    # ---------------------------------------------------------

    with engine.connect() as connection:

        sales_trend_rows = connection.execute(
            sales_trend_query
        ).fetchall()

        top_medicine_rows = connection.execute(
            top_medicines_query
        ).fetchall()

    # =========================================================
    # PREPARE DATAFRAMES
    # =========================================================

    sales_trend_df = pd.DataFrame(
        sales_trend_rows,
        columns=[
            "Sale_Date",
            "Total_Sales"
        ]
    )

    top_medicine_df = pd.DataFrame(
        top_medicine_rows,
        columns=[
            "Medicine_Name",
            "Total_Sold"
        ]
    )

    # =========================================================
    # DASHBOARD CHARTS
    # =========================================================

    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # SALES TREND
    # ---------------------------------------------------------

    with col1:

        st.markdown(
            """
            <div class="section-card">

            <h4 style="color:#008B8F;">
            📈 Sales Trend
            </h4>

            </div>
            """,
            unsafe_allow_html=True
        )

        if not sales_trend_df.empty:

            fig_sales_trend = px.line(
                sales_trend_df,
                x="Sale_Date",
                y="Total_Sales",
                markers=True
            )

            fig_sales_trend.update_traces(
                line=dict(
                    color="#00BCD4",
                    width=3
                ),
                marker=dict(
                    color="#00BCD4",
                    size=6
                )
            )

            fig_sales_trend.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=10,
                    b=40
                ),
                xaxis_title="Date",
                yaxis_title="Sales Amount",
                showlegend=False
            )

            st.plotly_chart(
                fig_sales_trend,
                use_container_width=True
            )

        else:

            st.info(
                "No sales data available."
            )

    # ---------------------------------------------------------
    # TOP SELLING MEDICINES
    # ---------------------------------------------------------

    with col2:

        st.markdown(
            """
            <div class="section-card">

            <h4 style="color:#008B8F;">
            📊 Top Selling Medicines
            </h4>

            </div>
            """,
            unsafe_allow_html=True
        )

        if not top_medicine_df.empty:

            fig_top_medicines = px.bar(
                top_medicine_df,
                x="Medicine_Name",
                y="Total_Sold",
                text="Total_Sold"
            )

            fig_top_medicines.update_traces(
                marker_color="#00BCD4",
                textposition="outside"
            )

            fig_top_medicines.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=10,
                    b=80
                ),
                xaxis_title="Medicine",
                yaxis_title="Quantity Sold",
                showlegend=False
            )

            fig_top_medicines.update_xaxes(
                tickangle=-45
            )

            st.plotly_chart(
                fig_top_medicines,
                use_container_width=True
            )

        else:

            st.info(
                "No medicine sales data available."
            )

    # =========================================================
    # DASHBOARD — SECOND ROW OF CHARTS
    # =========================================================

    # ---------------------------------------------------------
    # SALES VS DUES QUERY
    # ---------------------------------------------------------

    sales_dues_query = text("""
        SELECT
            ISNULL(SUM(Order_Amount), 0) AS Total_Sales,
            ISNULL(SUM(Dues_Amount), 0) AS Total_Dues
        FROM Sales
    """)

    # ---------------------------------------------------------
    # TOP RETAILERS BY SALES QUERY
    # ---------------------------------------------------------

    top_retailers_dashboard_query = text("""
        SELECT TOP 10
            r.Shop_Name,
            SUM(s.Order_Amount) AS Total_Sales
        FROM Sales s
        INNER JOIN Retailer r
            ON s.Retailer_Id = r.Retailer_Id
        GROUP BY r.Shop_Name
        ORDER BY Total_Sales DESC
    """)

    # ---------------------------------------------------------
    # GET DATA
    # ---------------------------------------------------------

    with engine.connect() as connection:

        sales_dues_result = connection.execute(
            sales_dues_query
        ).fetchone()

        top_retailer_dashboard_rows = connection.execute(
            top_retailers_dashboard_query
        ).fetchall()

    # =========================================================
    # PREPARE SALES VS DUES DATA
    # =========================================================

    sales_vs_dues_df = pd.DataFrame(
        {
            "Category": [
                "Total Sales",
                "Total Dues"
            ],
            "Amount": [
                float(sales_dues_result.Total_Sales or 0),
                float(sales_dues_result.Total_Dues or 0)
            ]
        }
    )

    # =========================================================
    # PREPARE TOP RETAILERS DATA
    # =========================================================

    top_retailers_dashboard_df = pd.DataFrame(
        top_retailer_dashboard_rows,
        columns=[
            "Shop_Name",
            "Total_Sales"
        ]
    )

    # =========================================================
    # SECOND ROW
    # =========================================================

    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # SALES VS DUES
    # ---------------------------------------------------------

    with col1:

        st.markdown(
            """
            <div class="section-card">

            <h4 style="color:#008B8F;">
            💰 Sales vs Dues
            </h4>

            </div>
            """,
            unsafe_allow_html=True
        )

        fig_sales_dues = px.bar(
            sales_vs_dues_df,
            x="Category",
            y="Amount",
            text="Amount"
        )

        fig_sales_dues.update_traces(
            marker_color="#00BCD4",
            texttemplate="₹ %{text:,.2f}",
            textposition="outside"
        )

        fig_sales_dues.update_layout(
            height=350,
            margin=dict(
                l=20,
                r=20,
                t=10,
                b=40
            ),
            xaxis_title="",
            yaxis_title="Amount",
            showlegend=False
        )

        st.plotly_chart(
            fig_sales_dues,
            use_container_width=True
        )

    # ---------------------------------------------------------
    # TOP RETAILERS BY SALES
    # ---------------------------------------------------------

    with col2:

        st.markdown(
            """
            <div class="section-card">

            <h4 style="color:#008B8F;">
            🏪 Top Retailers by Sales
            </h4>

            </div>
            """,
            unsafe_allow_html=True
        )

        if not top_retailers_dashboard_df.empty:

            fig_top_retailers = px.bar(
                top_retailers_dashboard_df,
                x="Shop_Name",
                y="Total_Sales",
                text="Total_Sales"
            )

            fig_top_retailers.update_traces(
                marker_color="#00BCD4",
                texttemplate="₹ %{text:,.0f}",
                textposition="outside"
            )

            fig_top_retailers.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=10,
                    b=80
                ),
                xaxis_title="Retailer",
                yaxis_title="Selling Amount",
                showlegend=False
            )

            fig_top_retailers.update_xaxes(
                tickangle=-45
            )

            st.plotly_chart(
                fig_top_retailers,
                use_container_width=True
            )

        else:

            st.info(
                "No retailer sales data available."
            )
# =========================================================
# SALES
# =========================================================

elif page == "🛒 Sales":

    # =====================================================
    # SELECTED DATE RANGE
    # =====================================================

    if "sales_from_date" not in st.session_state:
        st.session_state.sales_from_date = date.today()

    if "sales_to_date" not in st.session_state:
        st.session_state.sales_to_date = date.today()

    # =====================================================
    # DATE RANGE
    # =====================================================

    kpi1, kpi2, kpi3, kpi4, from_col, to_col = st.columns(
        [1.2, 1.2, 1.2, 1.2, 0.9, 0.9]
    )

    # -----------------------------------------------------
    # FROM DATE
    # -----------------------------------------------------

    with from_col:

        st.markdown(
            "<div style='font-size:13px;font-weight:600;"
            "margin-bottom:4px;'>📅 From</div>",
            unsafe_allow_html=True
        )

        from_date = st.date_input(
            "From Date",
            value=st.session_state.sales_from_date,
            label_visibility="collapsed",
            key="sales_from_date_filter"
        )

        st.session_state.sales_from_date = from_date

    # -----------------------------------------------------
    # TO DATE
    # -----------------------------------------------------

    with to_col:

        st.markdown(
            "<div style='font-size:13px;font-weight:600;"
            "margin-bottom:4px;'>📅 To</div>",
            unsafe_allow_html=True
        )

        to_date = st.date_input(
            "To Date",
            value=st.session_state.sales_to_date,
            label_visibility="collapsed",
            key="sales_to_date_filter"
        )

        st.session_state.sales_to_date = to_date

    # =====================================================
    # VALIDATE DATE RANGE
    # =====================================================

    if from_date > to_date:
        st.error(
            "From Date cannot be greater than To Date."
        )

        st.stop()

    # =====================================================
    # KPI QUERY
    # =====================================================

    kpi_query = text("""
        SELECT
            ISNULL(SUM(Order_Amount), 0) AS Total_Sale,
            COUNT(*) AS Total_Orders,
            ISNULL(SUM(Dues_Amount), 0) AS Total_Dues
        FROM Sales
        WHERE CAST(Date AS DATE)
              BETWEEN :from_date AND :to_date
    """)

    active_retailer_query = text("""
        SELECT COUNT(*)
        FROM Retailer
        WHERE Status = 'Active'
    """)

    with engine.connect() as connection:

        kpi_result = connection.execute(
            kpi_query,
            {
                "from_date": from_date,
                "to_date": to_date
            }
        ).fetchone()

        active_retailers = connection.execute(
            active_retailer_query
        ).scalar()

    # =====================================================
    # KPI VALUES
    # =====================================================

    total_sale = float(
        kpi_result.Total_Sale or 0
    )

    total_orders = int(
        kpi_result.Total_Orders or 0
    )

    total_dues = float(
        kpi_result.Total_Dues or 0
    )

    active_retailers = int(
        active_retailers or 0
    )

    # =====================================================
    # KPI 1
    # =====================================================

    with kpi1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Sale</div>
                <div class="kpi-value">
                    ₹ {total_sale:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # KPI 2
    # =====================================================

    with kpi2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Orders</div>
                <div class="kpi-value">
                    {total_orders:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # KPI 3
    # =====================================================

    with kpi3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Dues</div>
                <div class="kpi-value">
                    ₹ {total_dues:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # KPI 4
    # =====================================================

    with kpi4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">Active Retailers</div>
                <div class="kpi-value">
                    {active_retailers:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    # =====================================================
    # SECOND ROW
    # DASHBOARD 1 + SMALL SALES CONTROLS
    # =====================================================

    st.markdown("")

    dashboard_col, action_col = st.columns(
        [2.2, 1]
    )

    # -----------------------------
    # DASHBOARD 1
    # -----------------------------

    with dashboard_col:

        st.markdown(
            "<div style='font-size:25px;font-weight:900;"
            "color:#000000;margin-bottom:5px;'>📊 SALES DAY WISE </div>",
            unsafe_allow_html=True
        )

        # =====================================
        # SALES TREND CHART
        # =====================================

        sales_trend_query = text("""
                    SELECT
                        CAST(Date AS DATE) AS Sale_Date,
                        SUM(Order_Amount) AS Total_Sales
                    FROM Sales
                    WHERE CAST(Date AS DATE) BETWEEN :from_date AND :to_date
                    GROUP BY CAST(Date AS DATE)
                    ORDER BY Sale_Date
                """)

        sales_trend_df = pd.read_sql(
            sales_trend_query,
            engine,
            params={
                "from_date": from_date,
                "to_date": to_date
            }
        )

        if not sales_trend_df.empty:

            sales_trend_df["Sale_Date"] = pd.to_datetime(
                sales_trend_df["Sale_Date"]
            )

            fig = px.line(
                sales_trend_df,
                x="Sale_Date",
                y="Total_Sales",
                markers=True,
                title="Sales Trend"
            )

            fig.update_layout(
                height=350,

                margin=dict(
                    l=15,
                    r=15,
                    t=45,
                    b=15
                ),

                # Cyan background
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",

                # White font
                font=dict(
                    color="#000000",
                    size=13
                ),

                title_font=dict(
                    color="#000000",
                    size=18
                ),

                xaxis=dict(
                    title="Sale Date",
                    title_font=dict(
                        color="#000000",
                        size=14
                    ),
                    tickfont=dict(
                        color="#000000",
                        size=12
                    ),
                    gridcolor="rgba(255,255,255,0.25)"
                ),

                yaxis=dict(
                    title="Sales Amount (₹)",
                    title_font=dict(
                        color="#000000",
                        size=14
                    ),
                    tickfont=dict(
                        color="#000000",
                        size=12
                    ),
                    gridcolor="rgba(255,255,255,0.25)"
                )
            )

            fig.update_traces(
                line=dict(
                    color="#00BCD4",
                    width=3
                ),
                marker=dict(
                    color="#00BCD4",
                    size=7
                ),
                hovertemplate=
                "<b>Date:</b> %{x|%d-%b-%Y}<br>"
                "<b>Sales:</b> ₹ %{y:,.2f}"
                "<extra></extra>"
            )

            # =====================================
            # CHART CONTAINER
            # =====================================


            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

            st.markdown(
                """
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "No sales data available for the sales trend chart."
            )
    # -----------------------------
    # SALES ACTIONS
    # -----------------------------

    # -----------------------------
    # SALES ACTIONS + TOP 5 SALES DAYS
    # -----------------------------

    with action_col:

        st.markdown(
            "<div style='font-size:14px;font-weight:700;"
            "margin-bottom:8px;'>Sales Entry</div>",
            unsafe_allow_html=True
        )


        # =====================================================
        # NEW SALE RESET FUNCTION
        # =====================================================

        def reset_new_sale():

            st.session_state.sale_cart = []

            # Clear retailer
            st.session_state.selected_retailer = None
            st.session_state.selected_retailer_data = None
            st.session_state.retailer_search = ""
            st.session_state.retailer_selection = "Select Retailer"

            # Clear medicine
            st.session_state.medicine_search = ""
            st.session_state.sales_medicine = "Select Medicine"

            # Reset quantity
            st.session_state.sales_quantity = 1

            # Reset paid amount
            st.session_state["sales_paid"] = 0.0

            st.session_state.sale_reset_counter = (
                    st.session_state.get("sale_reset_counter", 0) + 1
            )

            # Reset customer type
            st.session_state.customer_type = "Old Retailer"

            # Reset SALE DATE
            today = date.today()

            st.session_state.sale_date = today

            # Reset Dashboard Date Range
            st.session_state.sales_from_date = today
            st.session_state.sales_to_date = today

            # Reset visible date-input widgets
            st.session_state.sales_from_date_filter = today
            st.session_state.sales_to_date_filter = today


        # =====================================================
        # ACTION BUTTONS
        # =====================================================

        action1, action2 = st.columns(2)

        with action1:

            st.button(
                "🛒 New Sale",
                key="new_sale_action",
                use_container_width=True,
                on_click=reset_new_sale
            )

        with action2:

            if st.button(
                    "New Retailer",
                    key="new_retailer_action",
                    use_container_width=True
            ):
                st.session_state.customer_type = "New Retailer"

        # =====================================================
        # TOP 5 SALES DAYS
        # =====================================================

        st.markdown(
            """
            <div style="
                font-size:16px;
                font-weight:800;
                color:#000000;
                margin-top:0px;
                margin-bottom:5px;
            ">
            🏆 Top 5 Sales Days
            </div>
            """,
            unsafe_allow_html=True
        )

        top_sales_days_query = text("""
            SELECT TOP 5
                CAST(Date AS DATE) AS Sale_Date,
                SUM(Order_Amount) AS Total_Sales
            FROM Sales
            WHERE CAST(Date AS DATE)
                  BETWEEN :from_date AND :to_date
            GROUP BY CAST(Date AS DATE)
            ORDER BY Total_Sales DESC
        """)

        top_sales_days_df = pd.read_sql(
            top_sales_days_query,
            engine,
            params={
                "from_date": from_date,
                "to_date": to_date
            }
        )

        if not top_sales_days_df.empty:

            top_sales_days_df["Sale_Date"] = pd.to_datetime(
                top_sales_days_df["Sale_Date"]
            )

            fig_top_sales_days = px.bar(
                top_sales_days_df,
                x="Total_Sales",
                y="Sale_Date",
                orientation="h",
                text="Total_Sales"
            )

            fig_top_sales_days.update_traces(
                marker_color="#00BCD4",
                texttemplate="₹ %{text:,.0f}",
                textposition="outside"
            )

            fig_top_sales_days.update_layout(
                height=280,

                margin=dict(
                    l=5,
                    r=35,
                    t=10,
                    b=10
                ),

                paper_bgcolor="white",
                plot_bgcolor="white",

                font=dict(
                    color="#000000",
                    size=11
                ),

                xaxis=dict(
                    title="Sales Amount (₹)",
                    tickfont=dict(
                        color="#000000",
                        size=10
                    ),
                    title_font=dict(
                        color="#000000",
                        size=11
                    ),
                    gridcolor="#E0E0E0"
                ),

                yaxis=dict(
                    title="",
                    tickformat="%d-%b-%Y",
                    tickfont=dict(
                        color="#000000",
                        size=10
                    ),
                    autorange="reversed"
                ),

                showlegend=False
            )

            fig_top_sales_days.update_traces(
                hovertemplate=
                "<b>Date:</b> %{y|%d-%b-%Y}<br>"
                "<b>Sales:</b> ₹ %{x:,.2f}"
                "<extra></extra>"
            )

            # =================================================
            # CHART CONTAINER
            # =================================================


            st.plotly_chart(
                fig_top_sales_days,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

            st.markdown(
                """
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "No sales data available for the selected date range."
            )


    # =====================================================
    # ENTRY / BILLING AREA
    # =====================================================

    st.markdown("---")

    entry_col, bill_col = st.columns(
        [1.5, 1]
    )

    # -----------------------------
    # ENTRY
    # -----------------------------

    with entry_col:

        st.markdown(
            "<div style='font-size:16px;font-weight:700;"
            "margin-bottom:5px;'>🧾 Entry</div>",
            unsafe_allow_html=True
        )

        entry1, entry2 = st.columns(2)

        # ---------------------------------
        # RETAILER SEARCH
        # ---------------------------------

        with entry1:
            retailer_search = st.text_input(
                "🔍 Search Retailer",
                placeholder="Retailer ID or Shop Name",
                key="retailer_search"
            )

        # ---------------------------------
        # SELECT RETAILER
        # ---------------------------------

        with entry2:
            query = text("""
                SELECT
                    Retailer_Id,
                    Shop_Name,                                
                    Address,
                    City,
                    State,
                    Phone_No
                FROM Retailer
                WHERE Status = 'Active'
                  AND (
                      CAST(Retailer_Id AS VARCHAR) LIKE :search
                      OR Shop_Name LIKE :search
                  )
                ORDER BY Shop_Name
            """)

            with engine.connect() as connection:
                retailers = connection.execute(
                    query,
                    {
                        "search": f"%{retailer_search}%" if retailer_search else "%"
                    }
                ).fetchall()

            retailer_options = {
                f"{r.Retailer_Id} - {r.Shop_Name}": r
                for r in retailers
            }

            if st.session_state.get("customer_type", "Old Retailer") == "Old Retailer":

                selected_retailer = st.selectbox(
                    "🏪 Select Retailer",
                    ["Select Retailer"] + list(retailer_options.keys()),
                    key="retailer_selection"
                )

                if selected_retailer != "Select Retailer":
                    retailer = retailer_options[selected_retailer]

                    st.session_state.selected_retailer_data = retailer

                    st.session_state.customer_type = "Old Retailer"

        # =====================================================
        # SALE DATE
        # =====================================================

        if "sale_date" not in st.session_state:
            st.session_state.sale_date = date.today()

        sale_date_col, empty_col = st.columns([1, 4])

        with sale_date_col:

            st.markdown(
                "<div style='font-size:13px;font-weight:600;"
                "margin-bottom:4px;'>📅 Sale Date</div>",
                unsafe_allow_html=True
            )

            sale_date = st.date_input(
                "Sale Date",
                value=st.session_state.sale_date,
                label_visibility="collapsed",
                key="sale_date"
            )
        # =====================================================
        # NEW RETAILER
        # =====================================================

        if st.session_state.get("customer_type") == "New Retailer":
            st.markdown("#### 🏪 New Retailer Details")

            retailer_col1, retailer_col2 = st.columns(2)

            with retailer_col1:
                new_shop_name = st.text_input(
                    "Shop Name",
                    key="new_retailer_shop_name"
                )

                new_proprietor_name = st.text_input(
                    "Proprietor Name",
                    key="new_retailer_proprietor_name"
                )

                new_address = st.text_input(
                    "Address",
                    key="new_retailer_address"
                )

                new_phone = st.text_input(
                    "Phone No",
                    key="new_retailer_phone"
                )

            with retailer_col2:
                new_city = st.text_input(
                    "City",
                    value="Hazaribagh",
                    key="new_retailer_city"
                )

                new_state = st.text_input(
                    "State",
                    value="Jharkhand",
                    key="new_retailer_state"
                )

                new_pin_code = st.text_input(
                    "Pin Code",
                    value="825301",
                    key="new_retailer_pin_code"
                )
        medicine_col, qty_col, price_col, discount_col = st.columns(
            [3, 1, 1.2, 1]
        )

        # =====================================================
        # MEDICINE
        # =====================================================

        with medicine_col:

            medicine_search = st.text_input(
                "💊 Search Medicine",
                placeholder="Type medicine name...",
                key="medicine_search"
            )

            medicine_options = {}
            selected_medicine = "Select Medicine"

            if medicine_search:
                medicine_query = text("""
                    SELECT TOP 30
                        Medicine_Id,
                        Medicine_Name,
                        Selling_Price,
                        Discount_Percent
                    FROM Medicine
                    WHERE Medicine_Name LIKE :search
                    ORDER BY Medicine_Name
                """)

                with engine.connect() as connection:
                    medicines = connection.execute(
                        medicine_query,
                        {"search": f"%{medicine_search}%"}
                    ).fetchall()

                medicine_options = {
                    f"{m.Medicine_Id} - {m.Medicine_Name}": m
                    for m in medicines
                }

                selected_medicine = st.selectbox(
                    "Select Medicine",
                    ["Select Medicine"] + list(medicine_options.keys()),
                    key="sales_medicine"
                )

        # =====================================================
        # QUANTITY
        # =====================================================

        with qty_col:

            quantity = st.number_input(
                "Qty",
                min_value=1,
                value=1,
                step=1,
                key="sales_quantity"
            )

        # =====================================================
        # PRICE
        # =====================================================

        with price_col:

            price_value = 0.0

            if selected_medicine != "Select Medicine":
                medicine = medicine_options[selected_medicine]
                price_value = float(medicine.Selling_Price or 0)

            st.markdown("**Price**")
            st.write(f"₹ {price_value:,.2f}")
        # =====================================================
        # DISCOUNT
        # =====================================================

        with discount_col:

            discount_value = 0.0

            if selected_medicine != "Select Medicine":
                medicine = medicine_options[selected_medicine]
                discount_value = float(medicine.Discount_Percent or 0)

            st.markdown("**Disc. %**")
            st.write(f"{discount_value:.2f}%")
        # =====================================================
        # ADD BUTTON
        # =====================================================
        if st.button(
                "➕ Add",
                key="sales_add_cart",
                use_container_width=True
        ):

            if selected_medicine == "Select Medicine":

                st.warning("Please select a medicine.")

            else:

                medicine = medicine_options[selected_medicine]

                price_value = float(medicine.Selling_Price or 0)
                discount_value = float(medicine.Discount_Percent or 0)

                gross_amount = quantity * price_value
                discount_amount = gross_amount * discount_value / 100
                net_amount = gross_amount - discount_amount

                if "sale_cart" not in st.session_state:
                    st.session_state.sale_cart = []

                st.session_state.sale_cart.append({
                    "Medicine": medicine.Medicine_Name,
                    "Medicine_Id": medicine.Medicine_Id,
                    "Qty": quantity,
                    "Price": price_value,
                    "Discount %": discount_value,
                    "Amount": net_amount
                })

                st.success(
                    f"{medicine.Medicine_Name} added to sale."
                )
        # =====================================================
        # SALE CART
        # =====================================================

        if st.session_state.get("sale_cart"):
            st.markdown("#### 🛒 Current Sale")

            cart_df = pd.DataFrame(
                st.session_state.sale_cart
            )

            st.dataframe(
                cart_df[
                    [
                        "Medicine",
                        "Qty",
                        "Price",
                        "Discount %",
                        "Amount"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )
        # =====================================================
        # SAVE BILL
        # =====================================================

        if st.session_state.get("sale_cart"):

            st.markdown("#### 💾 Bill")

            cart_total = sum(
                item["Amount"]
                for item in st.session_state.sale_cart
            )

            st.metric(
                "Bill Total",
                f"₹ {cart_total:,.2f}"
            )

            if st.button(
                    "💾 SAVE BILL",
                    use_container_width=True,
                    key="save_sale_bill"
            ):

                if not st.session_state.get("sale_cart"):

                    st.warning("Please add at least one medicine.")

                else:

                    # =========================================
                    # BILL TOTAL
                    # =========================================

                    order_amount = sum(
                        item["Amount"]
                        for item in st.session_state.sale_cart
                    )

                    paid_key = f"sales_paid_{st.session_state.get('sale_reset_counter', 0)}"

                    paid_amount = float(
                        st.session_state.get(paid_key, 0)
                    )

                    dues_amount = order_amount - paid_amount

                    if dues_amount <= 0:
                        dues_amount = 0
                        payment_status = "Paid"

                    elif paid_amount > 0:
                        payment_status = "Partial"

                    else:
                        payment_status = "Pending"

                    # =========================================
                    # CUSTOMER DETAILS
                    # =========================================

                    customer_type = st.session_state.get(
                        "customer_type",
                        "Others"
                    )

                    retailer = st.session_state.get(
                        "selected_retailer_data"
                    )

                    retailer_id = None
                    customer_name = ""
                    customer_address = ""
                    customer_city = ""
                    customer_phone = ""

                    if customer_type == "Old Retailer" and retailer:
                        retailer_id = retailer.Retailer_Id
                        customer_name = retailer.Shop_Name or ""
                        customer_address = retailer.Address or ""
                        customer_city = retailer.City or ""
                        customer_phone = retailer.Phone_No or ""

                    if customer_type == "New Retailer":

                        if not new_shop_name.strip():
                            st.error("Please enter Shop Name.")
                            st.stop()

                        if not new_proprietor_name.strip():
                            st.error("Please enter Proprietor Name.")
                            st.stop()

                        if not new_address.strip():
                            st.error("Please enter Address.")
                            st.stop()

                        if not new_phone.strip():
                            st.error("Please enter Phone No.")
                            st.stop()

                    # =========================================
                    # ORDER ID
                    # =========================================

                    from datetime import datetime

                    order_id = (
                            "ORD-"
                            + datetime.now().strftime("%Y%m%d%H%M%S")
                    )

                    # =========================================
                    # SAVE BILL
                    # =========================================

                    try:

                        with engine.begin() as connection:

                            if customer_type == "New Retailer":
                                retailer_query = text("""
                                    INSERT INTO Retailer
                                    (
                                        Shop_Name,
                                        Proprietor_Name,
                                        Address,
                                        City,
                                        State,
                                        Pin_Code,
                                        Phone_No
                                    )
                                    OUTPUT INSERTED.Retailer_Id
                                    VALUES
                                    (
                                        :shop_name,
                                        :proprietor_name,
                                        :address,
                                        :city,
                                        :state,
                                        :pin_code,
                                        :phone_no
                                    )
                                """)

                                retailer_result = connection.execute(
                                    retailer_query,
                                    {
                                        "shop_name": new_shop_name.strip(),
                                        "proprietor_name": new_proprietor_name.strip(),
                                        "address": new_address.strip(),
                                        "city": new_city.strip(),
                                        "state": new_state.strip(),
                                        "pin_code": new_pin_code.strip(),
                                        "phone_no": new_phone.strip()
                                    }
                                )

                                retailer_id = retailer_result.scalar_one()

                                customer_name = new_shop_name.strip()
                                customer_address = new_address.strip()
                                customer_city = new_city.strip()
                                customer_phone = new_phone.strip()

                            # ---------------------------------
                            # SALES TABLE
                            # ---------------------------------

                            sales_query = text("""
                                       INSERT INTO Sales
                                       (
                                           Order_Id,
                                           Date,
                                           Customer_Type,
                                           Retailer_Id,
                                           Name,
                                           Address,
                                           City,
                                           Phone_No,
                                           Order_Amount,
                                           Paid_Amount,
                                           Dues_Amount,
                                           Round_Off_Amount,
                                           Payment_Status
                                       )
                                       OUTPUT INSERTED.Sales_Id
                                       VALUES
                                       (
                                           :order_id,
                                           :date,
                                           :customer_type,
                                           :retailer_id,
                                           :name,
                                           :address,
                                           :city,
                                           :phone_no,
                                           :order_amount,
                                           :paid_amount,
                                           :dues_amount,
                                           :round_off,
                                           :payment_status
                                       )
                                   """)

                            result = connection.execute(
                                sales_query,
                                {
                                    "order_id": order_id,
                                    "date": datetime.combine(
                                        sale_date,
                                        datetime.now().time()
                                    ),
                                    "customer_type": customer_type,
                                    "retailer_id": retailer_id,
                                    "name": customer_name,
                                    "address": customer_address,
                                    "city": customer_city,
                                    "phone_no": customer_phone,
                                    "order_amount": order_amount,
                                    "paid_amount": paid_amount,
                                    "dues_amount": dues_amount,
                                    "round_off": 0,
                                    "payment_status": payment_status
                                }
                            )

                            sales_id = result.scalar_one()

                            # ---------------------------------
                            # SALES DETAILS TABLE
                            # ---------------------------------

                            detail_query = text("""
                                       INSERT INTO Sales_Details
                                       (
                                           Sales_Id,
                                           Order_Id,
                                           Medicine_Id,
                                           Medicine_Name,
                                           Quantity,
                                           Price,
                                           Amount,
                                           Discount_Percent,
                                           Net_Amount
                                       )
                                       VALUES
                                       (
                                           :sales_id,
                                           :order_id,
                                           :medicine_id,
                                           :medicine_name,
                                           :quantity,
                                           :price,
                                           :amount,
                                           :discount_percent,
                                           :net_amount
                                       )
                                   """)

                            for item in st.session_state.sale_cart:
                                connection.execute(
                                    detail_query,
                                    {
                                        "sales_id": sales_id,
                                        "order_id": order_id,
                                        "medicine_id": item["Medicine_Id"],
                                        "medicine_name": item["Medicine"],
                                        "quantity": item["Qty"],
                                        "price": item["Price"],
                                        "amount": (
                                                item["Qty"] *
                                                item["Price"]
                                        ),
                                        "discount_percent": (
                                            item["Discount %"]
                                        ),
                                        "net_amount": item["Amount"]
                                    }
                                )
                            if dues_amount > 0:
                                dues_query = text("""
                                                           INSERT INTO Dues
                                                           (
                                                               Retailer_Id,
                                                               Shop_Name,
                                                               Order_Id,
                                                               Order_Amount,
                                                               Paid_Amount,
                                                               Dues_Amount,
                                                               Due_Date,
                                                               Payment_Date,
                                                               Payment_Status
                                                           )
                                                           VALUES
                                                           (
                                                               :retailer_id,
                                                               :shop_name,
                                                               :order_id,
                                                               :order_amount,
                                                               :paid_amount,
                                                               :dues_amount,
                                                               :due_date,
                                                               :payment_date,
                                                               :payment_status
                                                           )
                                                       """)

                                connection.execute(
                                    dues_query,
                                    {
                                        "retailer_id": retailer_id,
                                        "shop_name": customer_name,
                                        "order_id": order_id,
                                        "order_amount": order_amount,
                                        "paid_amount": paid_amount,
                                        "dues_amount": dues_amount,
                                        "due_date": datetime.now(),
                                        "payment_date": None,
                                        "payment_status": payment_status
                                    }
                                )

                        # =====================================
                        # SUCCESS
                        # =====================================

                        st.success(
                            f"Bill saved successfully — {order_id}"
                        )

                        # Store last saved bill for printing
                        st.session_state.last_saved_order_id = order_id
                        st.session_state.last_saved_sale_date = sale_date
                        st.session_state.last_saved_customer_name = customer_name
                        st.session_state.last_saved_order_amount = order_amount
                        st.session_state.last_saved_paid_amount = paid_amount
                        st.session_state.last_saved_dues_amount = dues_amount
                        st.session_state.last_saved_payment_status = payment_status
                        st.session_state.last_saved_cart = st.session_state.sale_cart.copy()

                        st.session_state.sale_cart = []

                        # =====================================
                        # PRINT / SAVE LAST BILL
                        # =====================================

                        if st.session_state.get("last_saved_order_id"):
                            st.markdown("### 🖨️ Bill")
                            # =====================================
                            # GENERATE WHOLESALE SALES INVOICE
                            # =====================================

                            from textwrap import dedent

                            cart = st.session_state.last_saved_cart

                            med_id_width = max(
                                len("Med ID"),
                                max(len(str(item["Medicine_Id"])) for item in cart)
                            )

                            medicine_width = max(
                                len("Medicine Name"),
                                max(len(str(item["Medicine"])) for item in cart)
                            )

                            qty_width = max(
                                len("Qty"),
                                max(len(str(item["Qty"])) for item in cart)
                            )

                            price_width = max(
                                len("Price"),
                                max(len(f'{float(item["Price"]):.2f}') for item in cart)
                            )

                            discount_width = max(
                                len("Discount"),
                                max(len(f'{float(item["Discount %"]):.2f}%') for item in cart)
                            )

                            amount_width = max(
                                len("Net Amount"),
                                max(len(f'{float(item["Amount"]):.2f}') for item in cart)
                            )

                            table_width = (
                                    med_id_width
                                    + medicine_width
                                    + qty_width
                                    + price_width
                                    + discount_width
                                    + amount_width
                                    + 15
                            )

                            separator = "-" * table_width

                            lines = []

                            lines.append("VERMA MEDICAL STORE")
                            lines.append("              WHOLESALE SALES INVOICE")
                            lines.append("")
                            lines.append(
                                f"Order ID: {st.session_state.last_saved_order_id}"
                            )
                            lines.append(
                                f"Date: {st.session_state.last_saved_sale_date.strftime('%d-%b-%Y')}"
                            )
                            lines.append(
                                f"Shop: {st.session_state.last_saved_customer_name}"
                            )
                            lines.append("")
                            lines.append(separator)

                            lines.append(
                                f'{"Med ID":<{med_id_width}} | '
                                f'{"Medicine Name":<{medicine_width}} | '
                                f'{"Qty":>{qty_width}} | '
                                f'{"Price":>{price_width}} | '
                                f'{"Discount":>{discount_width}} | '
                                f'{"Net Amount":>{amount_width}}'
                            )

                            lines.append(separator)

                            total_qty = 0
                            total_amount = 0

                            for item in cart:
                                qty = int(item["Qty"])
                                price = float(item["Price"])
                                discount = float(item["Discount %"])
                                amount = float(item["Amount"])

                                total_qty += qty
                                total_amount += amount

                                lines.append(
                                    f'{str(item["Medicine_Id"]):<{med_id_width}} | '
                                    f'{str(item["Medicine"]):<{medicine_width}} | '
                                    f'{qty:>{qty_width}} | '
                                    f'{price:>{price_width}.2f} | '
                                    f'{discount:>{discount_width - 1}.2f}% | '
                                    f'{amount:>{amount_width}.2f}'
                                )

                            lines.append(separator)

                            lines.append(
                                f'{"TOTAL":<{med_id_width}} | '
                                f'{"":<{medicine_width}} | '
                                f'{total_qty:>{qty_width}} | '
                                f'{"":>{price_width}} | '
                                f'{"":>{discount_width}} | '
                                f'{total_amount:>{amount_width}.2f}'
                            )

                            lines.append("")
                            lines.append(
                                f"Paid Amount : ₹ {st.session_state.last_saved_paid_amount:,.2f}"
                            )
                            lines.append(
                                f"Dues Amount : ₹ {st.session_state.last_saved_dues_amount:,.2f}"
                            )
                            lines.append("")
                            lines.append(separator)
                            lines.append("Sold By:")
                            lines.append("VERMA MEDICAL STORE")
                            lines.append(separator)

                            bill_text = "\n".join(lines)

                            st.code(
                                bill_text,
                                language="text"
                            )

                            st.download_button(
                                label="⬇️ Download Bill",
                                data=bill_text,
                                file_name=f"{st.session_state.last_saved_order_id}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )

                    except Exception as e:

                        st.error(
                            f"Unable to save bill: {e}"
                        )

    # -----------------------------
    # BILL SUMMARY
    # -----------------------------

    with bill_col:

        st.markdown(
            "<div style='font-size:16px;font-weight:700;"
            "margin-bottom:5px;'>💰 Bill Summary</div>",
            unsafe_allow_html=True
        )



        # =====================================================
        # BILL SUMMARY VALUES
        # =====================================================

        cart_total = sum(
            item["Amount"]
            for item in st.session_state.get("sale_cart", [])
        )

        st.metric(
            "Order Amount",
            f"₹ {cart_total:,.2f}"
        )

        paid_col, due_col = st.columns(2)

        with paid_col:
            if "sales_paid" not in st.session_state:
                st.session_state.sales_paid = 0.0

            paid_amount = st.number_input(
                "Paid",
                min_value=0.0,
                max_value=float(cart_total),
                step=100.0,
                key=f"sales_paid_{st.session_state.get('sale_reset_counter', 0)}"
            )

        with due_col:
            due_amount = max(
                cart_total - paid_amount,
                0
            )

            st.metric(
                "Due",
                f"₹ {due_amount:,.2f}"
            )



    # =====================================================
    # BOTTOM TABLE
    # =====================================================

    st.markdown("---")

    st.markdown(
        "<div style='font-size:17px;font-weight:700;"
        "margin-bottom:5px;'>📋 Today's Sales</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # SALES TABLE
    # =====================================================

    sales_table_query = text("""
        SELECT
            Order_Id,
            Name AS Shop_Name,
            Order_Amount,
            Paid_Amount,
            Dues_Amount,
            Date AS Due_Date,
            Payment_Status
        FROM Sales
        WHERE CAST(Date AS DATE)
              BETWEEN :from_date AND :to_date
        ORDER BY Date DESC
    """)

    with engine.connect() as connection:

        sales_rows = connection.execute(
            sales_table_query,
            {
                "from_date": from_date,
                "to_date": to_date
            }
        ).fetchall()

    if sales_rows:

        sales_df = pd.DataFrame(
            sales_rows,
            columns=[
                "Order ID",
                "Shop Name",
                "Order Amount",
                "Paid Amount",
                "Dues Amount",
                "Due Date",
                "Payment Status"
            ]
        )

        # =====================================
        # SALES TABLE STYLING
        # =====================================

        sales_table_style = (
            sales_df.style
            .set_properties(
            ** {
            "background-color": "#FFFFFF",
            "color": "black",
            "font-weight": "600",
            "border": "1px solid white"
            }
        )

        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#80DEEA !important"),
                        ("color", "#000000 !important"),
                        ("font-weight", "900 !important"),
                        ("border", "2px solid black"),
                        ("text-align", "center")
                    ]
                },
                {
                    "selector": "td",
                    "props": [
                        ("background-color", "#00BCD4 !important"),
                        ("color", "#000000 !important"),
                        ("border", "1px solid white")
                    ]
                }
            ]
        )
    )

        # =====================================
        # BLACK ROUNDED TABLE CONTAINER
        # =====================================

        st.markdown(
            """
            <style>
            div[data-testid="stDataFrame"] {
                border: 4px solid #000000;
                border-radius: 12px;
                overflow: hidden;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            sales_table_style,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            f"No sales found from "
            f"{from_date.strftime('%d-%b-%Y')} to "
            f"{to_date.strftime('%d-%b-%Y')}."
        )
# =========================================================
# MEDICINE
# =========================================================

elif page == "💊 Medicine":

    # =====================================================
    # MEDICINE KPIs
    # =====================================================

    # Total Medicines
    total_medicines_query = text("""
        SELECT COUNT(*) 
        FROM Medicine
    """)

    total_stock_query = text("""
        SELECT COALESCE(SUM(Quantity), 0)
        FROM Medicine
    """)

    out_of_stock_query = text("""
        SELECT COUNT(*)
        FROM Medicine
        WHERE Quantity = 0
    """)

    low_stock_query = text("""
        SELECT COUNT(*)
        FROM Medicine
        WHERE Quantity BETWEEN 1 AND 10
    """)

    with engine.connect() as connection:

        total_medicines = connection.execute(
            total_medicines_query
        ).scalar() or 0

        total_stock = connection.execute(
            total_stock_query
        ).scalar() or 0

        out_of_stock = connection.execute(
            out_of_stock_query
        ).scalar() or 0

        low_stock = connection.execute(
            low_stock_query
        ).scalar() or 0

    # =====================================================
    # KPI CARDS
    # =====================================================

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">💊 Total Medicines</div>
                <div class="kpi-value">{total_medicines:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">📦 Total Stock Units</div>
                <div class="kpi-value">{total_stock:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">❌ Out of Stock Medicines</div>
                <div class="kpi-value">{out_of_stock:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with kpi4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">⚠️ Low Stock Medicines</div>
                <div class="kpi-value">{low_stock:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =====================================================
    # MEDICINE ENTRY / STOCK UPDATE
    # =====================================================

    st.markdown(
        """
        <style>

        .medicine-panel {
            background-color: #00BCD4;
            border: 4px solid #000000;
            border-radius: 12px;
            padding: 10px;
        }

        .medicine-entry-title {
            font-size: 17px;
            font-weight: 800;
            color: #000000;
            margin-bottom: 6px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container(border=True):

        st.markdown(
            """
            <div class="medicine-entry-title">
                ➕ Medicine Entry / Stock Update
            </div>
            """,
            unsafe_allow_html=True
        )

        entry_cols = st.columns(
            [
                1.8,  # Medicine Name
                1.6,  # Manufacturer
                1.0,  # Cost Price
                1.0,  # Price
                1.0,  # Selling Price
                0.9,  # Discount
                1.1,  # Pack Size
                0.9,  # Type
                1.1,  # Man Date
                1.1,  # Expiry Date
                0.8,  # Quantity
                0.8  # Save
            ]
        )

        with entry_cols[0]:
            medicine_name = st.text_input(
                "Medicine Name",
                key="medicine_entry_name"
            )

        with entry_cols[1]:
            manufacturer_name = st.text_input(
                "Manufacturer",
                key="medicine_entry_manufacturer"
            )

        with entry_cols[2]:
            cost_price = st.number_input(
                "Cost Price",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="medicine_entry_cost"
            )

        with entry_cols[3]:
            price = st.number_input(
                "Price",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="medicine_entry_price"
            )

        with entry_cols[4]:
            selling_price = st.number_input(
                "Selling Price",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                key="medicine_entry_selling"
            )

        with entry_cols[5]:

            if price > 0:
                discount_percent = (
                                           (price - selling_price) / price
                                   ) * 100
            else:
                discount_percent = 0.0

            st.number_input(
                "Discount %",
                value=float(discount_percent),
                disabled=True,
                format="%.2f",
                key="medicine_entry_discount"
            )

        with entry_cols[6]:
            pack_size_label = st.text_input(
                "Pack Size",
                key="medicine_entry_pack"
            )

        with entry_cols[7]:
            medicine_type = st.text_input(
                "Type",
                key="medicine_entry_type"
            )

        with entry_cols[8]:
            man_date = st.date_input(
                "Man. Date",
                key="medicine_entry_man_date"
            )

        with entry_cols[9]:
            expiry_date = st.date_input(
                "Expiry Date",
                key="medicine_entry_expiry_date"
            )

        with entry_cols[10]:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                step=1,
                key="medicine_entry_quantity"
            )

        with entry_cols[11]:
            save_medicine = st.button(
                "💾 SAVE",
                use_container_width=True,
                key="save_medicine"
            )
    # =====================================================
    # SAVE MEDICINE
    # =====================================================

    if save_medicine:

        # -------------------------------------------------
        # BASIC VALIDATION
        # -------------------------------------------------

        if not medicine_name.strip():

            st.warning("Please enter Medicine Name.")

        elif price <= 0:

            st.warning("Price must be greater than 0.")

        elif selling_price <= 0:

            st.warning("Selling Price must be greater than 0.")

        elif selling_price > price:

            st.warning(
                "Selling Price cannot be greater than Price."
            )

        elif quantity <= 0:

            st.warning("Quantity must be greater than 0.")

        else:

            # -------------------------------------------------
            # SAVE TO SQL
            # -------------------------------------------------

            from datetime import datetime

            now = datetime.now()

            medicine_name_clean = medicine_name.strip()

            manufacturer_clean = (
                manufacturer_name.strip()
                if manufacturer_name
                else None
            )

            pack_clean = (
                pack_size_label.strip()
                if pack_size_label
                else None
            )

            type_clean = (
                medicine_type.strip()
                if medicine_type
                else None
            )

            # -------------------------------------------------
            # CHECK EXISTING MEDICINE / LOT
            # -------------------------------------------------

            existing_query = text("""
                SELECT
                    Medicine_Id,
                    Quantity
                FROM Medicine
                WHERE Medicine_Name = :medicine_name
                  AND ISNULL(Manufacturer_Name, '') =
                      ISNULL(:manufacturer_name, '')
                  AND Price = :price
                  AND Selling_Price = :selling_price
                  AND ISNULL(Pack_Size_Label, '') =
                      ISNULL(:pack_size_label, '')
                  AND (
                        Expiry_Date = :expiry_date
                        OR (
                            Expiry_Date IS NULL
                            AND :expiry_date IS NULL
                        )
                      )
            """)

            with engine.begin() as connection:

                existing = connection.execute(
                    existing_query,
                    {
                        "medicine_name": medicine_name_clean,
                        "manufacturer_name": manufacturer_clean,
                        "price": price,
                        "selling_price": selling_price,
                        "pack_size_label": pack_clean,
                        "expiry_date": expiry_date
                    }
                ).fetchone()

                # -------------------------------------------------
                # EXISTING LOT → ADD QUANTITY
                # -------------------------------------------------

                if existing:

                    update_query = text("""
                        UPDATE Medicine
                        SET
                            Quantity = Quantity + :quantity,
                            Updated_Date = :updated_date
                        WHERE Medicine_Id = :medicine_id
                    """)

                    connection.execute(
                        update_query,
                        {
                            "quantity": quantity,
                            "updated_date": now,
                            "medicine_id": existing.Medicine_Id
                        }
                    )

                    st.success(
                        f"Stock updated successfully. "
                        f"{quantity} units added to "
                        f"{medicine_name_clean}."
                    )

                # -------------------------------------------------
                # NEW MEDICINE / NEW LOT
                # -------------------------------------------------

                else:

                    # Generate unique MED###### ID
                    while True:

                        import random

                        medicine_id = (
                                "MED"
                                + f"{random.randint(0, 999999):06d}"
                        )

                        id_check = connection.execute(
                            text("""
                                SELECT 1
                                FROM Medicine
                                WHERE Medicine_Id = :medicine_id
                            """),
                            {
                                "medicine_id": medicine_id
                            }
                        ).fetchone()

                        if not id_check:
                            break

                    # -------------------------------------------------
                    # INSERT NEW MEDICINE
                    # -------------------------------------------------

                    insert_query = text("""
                        INSERT INTO Medicine (
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
                            Quantity,
                            Created_Date,
                            Updated_Date
                        )
                        VALUES (
                            :medicine_id,
                            :medicine_name,
                            :manufacturer_name,
                            :cost_price,
                            :price,
                            :discount_percent,
                            :selling_price,
                            :pack_size_label,
                            :medicine_type,
                            :man_date,
                            :expiry_date,
                            :quantity,
                            :created_date,
                            :updated_date
                        )
                    """)

                    connection.execute(
                        insert_query,
                        {
                            "medicine_id": medicine_id,
                            "medicine_name": medicine_name_clean,
                            "manufacturer_name": manufacturer_clean,
                            "cost_price": cost_price,
                            "price": price,
                            "discount_percent": discount_percent,
                            "selling_price": selling_price,
                            "pack_size_label": pack_clean,
                            "medicine_type": type_clean,
                            "man_date": man_date,
                            "expiry_date": expiry_date,
                            "quantity": quantity,
                            "created_date": now,
                            "updated_date": now
                        }
                    )

                    st.success(
                        f"Medicine added successfully. "
                        f"Medicine ID: {medicine_id}"
                    )
    # =====================================================
    # DUPLICATE MEDICINES + NEAR EXPIRY
    # =====================================================

    duplicate_col, expiry_col = st.columns(2)

    # =====================================================
    # LEFT — DUPLICATE MEDICINES
    # =====================================================

    with duplicate_col:

        st.markdown(
            "<div style='font-size:17px;font-weight:700;"
            "margin-top:10px;margin-bottom:5px;'>"
            "🔄 Duplicate Medicines"
            "</div>",
            unsafe_allow_html=True
        )

        duplicate_query = text("""
            SELECT
                Medicine_Name,
                Manufacturer_Name,
                Price,
                Discount_Percent,
                Quantity
            FROM Medicine
            WHERE Medicine_Name IN (
                SELECT Medicine_Name
                FROM Medicine
                GROUP BY Medicine_Name
                HAVING COUNT(*) > 1
            )
            ORDER BY
                Medicine_Name,
                Created_Date ASC
        """)

        with engine.connect() as connection:

            duplicate_rows = connection.execute(
                duplicate_query
            ).fetchall()

        if duplicate_rows:

            duplicate_df = pd.DataFrame(
                duplicate_rows,
                columns=[
                    "Medicine Name",
                    "Manufacturer",
                    "Price",
                    "Discount %",
                    "Quantity"
                ]
            )

            st.dataframe(
                duplicate_df,
                use_container_width=True,
                hide_index=True,
                height=180
            )

        else:

            st.info(
                "No duplicate medicines found."
            )

    # =====================================================
    # RIGHT — NEAR EXPIRY
    # =====================================================

    with expiry_col:

        st.markdown(
            "<div style='font-size:17px;font-weight:700;"
            "margin-top:10px;margin-bottom:5px;'>"
            "⚠️ Near Expiry"
            "</div>",
            unsafe_allow_html=True
        )

        near_expiry_query = text("""
            SELECT
                Medicine_Name,
                Manufacturer_Name,
                Type,
                Quantity,
                Expiry_Date
            FROM Medicine
            WHERE Expiry_Date IS NOT NULL
              AND Expiry_Date >= CAST(GETDATE() AS DATE)
              AND Expiry_Date <= DATEADD(
                    DAY,
                    90,
                    CAST(GETDATE() AS DATE)
              )
            ORDER BY Expiry_Date ASC
        """)

        with engine.connect() as connection:

            near_expiry_rows = connection.execute(
                near_expiry_query
            ).fetchall()

        if near_expiry_rows:

            near_expiry_df = pd.DataFrame(
                near_expiry_rows,
                columns=[
                    "Medicine Name",
                    "Manufacturer",
                    "Type",
                    "Quantity",
                    "Expiry Date"
                ]
            )

            st.dataframe(
                near_expiry_df,
                use_container_width=True,
                hide_index=True,
                height=180
            )

        else:

            st.info(
                "No medicines are near expiry."
            )
    # =====================================================
    # MOST SOLD + MOST EXPENSIVE MEDICINES
    # =====================================================

    most_sold_col, most_expensive_col = st.columns(2)

    # =====================================================
    # LEFT — MOST SOLD MEDICINES
    # =====================================================

    with most_sold_col:

        st.markdown(
            "<div style='font-size:17px;font-weight:700;"
            "margin-bottom:5px;'>"
            "📊 Most Sold Medicines"
            "</div>",
            unsafe_allow_html=True
        )

        most_sold_query = text("""
            SELECT TOP 10
                Medicine_Name,
                SUM(Quantity) AS Total_Sold
            FROM Sales_Details
            GROUP BY Medicine_Name
            ORDER BY Total_Sold DESC
        """)

        with engine.connect() as connection:

            most_sold_rows = connection.execute(
                most_sold_query
            ).fetchall()

        if most_sold_rows:

            most_sold_df = pd.DataFrame(
                most_sold_rows,
                columns=[
                    "Medicine Name",
                    "Quantity Sold"
                ]
            )

            fig = px.bar(
                most_sold_df,
                x="Medicine Name",
                y="Quantity Sold",
                text="Quantity Sold",
                title="Top 10 Most Sold Medicines"
            )

            fig.update_layout(
                height=300,
                margin=dict(
                    l=15,
                    r=15,
                    t=45,
                    b=80
                ),
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=9)
                )
            )

            fig.update_traces(
                marker_color="#00BCD4",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        else:

            st.info(
                "No medicine sales data available."
            )

    # =====================================================
    # RIGHT — MOST EXPENSIVE MEDICINES
    # =====================================================

    with most_expensive_col:

        st.markdown(
            "<div style='font-size:17px;font-weight:700;"
            "margin-bottom:5px;'>"
            "💰 Most Expensive Medicines"
            "</div>",
            unsafe_allow_html=True
        )

        most_expensive_query = text("""
            SELECT TOP 10
                Medicine_Name,
                Price
            FROM Medicine
            ORDER BY Price DESC
        """)

        with engine.connect() as connection:

            most_expensive_rows = connection.execute(
                most_expensive_query
            ).fetchall()

        if most_expensive_rows:

            most_expensive_df = pd.DataFrame(
                most_expensive_rows,
                columns=[
                    "Medicine Name",
                    "Price"
                ]
            )

            fig = px.bar(
                most_expensive_df,
                x="Medicine Name",
                y="Price",
                text="Price",
                title="Top 10 Most Expensive Medicines"
            )

            fig.update_layout(
                height=300,
                margin=dict(
                    l=15,
                    r=15,
                    t=45,
                    b=80
                ),
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=9)
                )
            )

            fig.update_traces(
                marker_color="#00BCD4",
                texttemplate="₹ %{text:,.2f}",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False
                }
            )

        else:

            st.info(
                "No medicine data available."
            )
    # =====================================================
    # ALL MEDICINES TABLE
    # =====================================================

    st.markdown("---")

    st.markdown(
        "<div style='font-size:17px;font-weight:700;"
        "margin-top:5px;margin-bottom:8px;'>"
        "💊 All Medicines"
        "</div>",
        unsafe_allow_html=True
    )

    # =====================================================
    # MEDICINE FILTERS
    # =====================================================

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        manufacturer_query = text("""
            SELECT DISTINCT Manufacturer_Name
            FROM Medicine
            WHERE Manufacturer_Name IS NOT NULL
              AND LTRIM(RTRIM(Manufacturer_Name)) <> ''
            ORDER BY Manufacturer_Name
        """)

        with engine.connect() as connection:
            manufacturer_rows = connection.execute(
                manufacturer_query
            ).fetchall()

        manufacturers = [
            row[0]
            for row in manufacturer_rows
        ]

        selected_manufacturer = st.selectbox(
            "Manufacturer",
            ["All"] + manufacturers,
            key="medicine_manufacturer_filter"
        )

    with filter_col2:

        type_query = text("""
            SELECT DISTINCT Type
            FROM Medicine
            WHERE Type IS NOT NULL
              AND LTRIM(RTRIM(Type)) <> ''
            ORDER BY Type
        """)

        with engine.connect() as connection:
            type_rows = connection.execute(
                type_query
            ).fetchall()

        medicine_types = [
            row[0]
            for row in type_rows
        ]

        selected_type = st.selectbox(
            "Medicine Type",
            ["All"] + medicine_types,
            key="medicine_type_filter"
        )

    # =====================================================
    # MEDICINE TABLE QUERY
    # =====================================================

    medicine_table_query = text("""
        SELECT TOP 6
            Medicine_Name,
            Manufacturer_Name,
            Price,
            Discount_Percent,
            Selling_Price,
            Type,
            Expiry_Date,
            Quantity
        FROM Medicine
        WHERE
            (
                :manufacturer = 'All'
                OR Manufacturer_Name = :manufacturer
            )
            AND
            (
                :medicine_type = 'All'
                OR Type = :medicine_type
            )
        ORDER BY Medicine_Name
    """)

    with engine.connect() as connection:

        medicine_rows = connection.execute(
            medicine_table_query,
            {
                "manufacturer": selected_manufacturer,
                "medicine_type": selected_type
            }
        ).fetchall()

    if medicine_rows:

        medicine_df = pd.DataFrame(
            medicine_rows,
            columns=[
                "Medicine Name",
                "Manufacturer Name",
                "Price",
                "Discount %",
                "Selling Price",
                "Type",
                "Expiry Date",
                "Quantity"
            ]
        )

        st.dataframe(
            medicine_df,
            use_container_width=True,
            hide_index=True,
            height=260
        )

    else:

        st.info(
            "No medicines found for the selected filters."
        )
# =========================================================
# RETAILERS & PAYMENTS
# =========================================================

elif page == "🏪 Retailers & Payments":

    # =====================================================
    # RETAILER PAGE — DATE FILTER + KPI SECTION
    # =====================================================

    retailer_kpi_query = text("""
        SELECT
            ISNULL(SUM(Order_Amount), 0) AS Total_Selling,
            ISNULL(SUM(Dues_Amount), 0) AS Total_Dues,
            COUNT(DISTINCT CAST(Date AS DATE)) AS Sale_Days
        FROM Sales
        WHERE CAST(Date AS DATE)
              BETWEEN :from_date AND :to_date
    """)

    total_retailers_query = text("""
        SELECT COUNT(*)
        FROM Retailer
        WHERE Status = 'Active'
    """)

    # -----------------------------------------------------
    # DATE VALUES
    # -----------------------------------------------------

    from_date = st.session_state.get(
        "sales_from_date",
        date.today()
    )

    to_date = st.session_state.get(
        "sales_to_date",
        date.today()
    )

    # -----------------------------------------------------
    # DATABASE VALUES
    # -----------------------------------------------------

    with engine.connect() as connection:

        kpi_result = connection.execute(
            retailer_kpi_query,
            {
                "from_date": from_date,
                "to_date": to_date
            }
        ).fetchone()

        total_retailers = connection.execute(
            total_retailers_query
        ).scalar() or 0

    # -----------------------------------------------------
    # KPI CALCULATIONS
    # -----------------------------------------------------

    total_selling = float(
        kpi_result.Total_Selling or 0
    )

    total_dues = float(
        kpi_result.Total_Dues or 0
    )

    sale_days = int(
        kpi_result.Sale_Days or 0
    )

    average_sale = (
        total_selling / sale_days
        if sale_days > 0
        else 0
    )

    # =====================================================
    # SIX COLUMNS — SAME ROW
    # =====================================================

    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

    # -----------------------------------------------------
    # 1. TOTAL SELLING
    # -----------------------------------------------------

    with kpi1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Total Selling Amount
                </div>
                <div class="kpi-value">
                    ₹ {total_selling:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # 2. TOTAL DUES
    # -----------------------------------------------------

    with kpi2:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Total Dues Amount
                </div>
                <div class="kpi-value">
                    ₹ {total_dues:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # 3. AVERAGE SALE PER DAY
    # -----------------------------------------------------

    with kpi3:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Average Sale Per Day
                </div>
                <div class="kpi-value">
                    ₹ {average_sale:,.2f}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # 4. TOTAL RETAILERS
    # -----------------------------------------------------

    with kpi4:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-title">
                    Total Retailers
                </div>
                <div class="kpi-value">
                    {total_retailers:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # 5. FROM DATE
    # -----------------------------------------------------

    with kpi5:

        from_date = st.date_input(
            "From Date",
            value=from_date,
            key="retailer_from_date"
        )

    # -----------------------------------------------------
    # 6. TO DATE
    # -----------------------------------------------------

    with kpi6:

        to_date = st.date_input(
            "To Date",
            value=to_date,
            key="retailer_to_date"
        )
    # =====================================================
    # NEW RETAILER ENTRY
    # =====================================================
    # Reset retailer entry panel after successful save
    if st.session_state.get("retailer_entry_reset", False):
        st.session_state["new_retailer_shop_name"] = ""
        st.session_state["new_retailer_proprietor_name"] = ""
        st.session_state["new_retailer_address"] = ""
        st.session_state["new_retailer_city"] = "Hazaribagh"
        st.session_state["new_retailer_state"] = "Jharkhand"
        st.session_state["new_retailer_pin"] = "825301"
        st.session_state["new_retailer_phone"] = ""
        st.session_state["new_retailer_status"] = "Active"

        st.session_state["retailer_entry_reset"] = False

    with st.container(border=True):

        retailer_entry_col1, retailer_entry_col2, retailer_entry_col3, \
            retailer_entry_col4, retailer_entry_col5, retailer_entry_col6, \
            retailer_entry_col7, retailer_entry_col8, retailer_entry_col9 = st.columns(9)

        with retailer_entry_col1:
            shop_name = st.text_input(
                "Shop Name",
                key="new_retailer_shop_name"
            )

        with retailer_entry_col2:
            proprietor_name = st.text_input(
                "Proprietor",
                key="new_retailer_proprietor_name"
            )

        with retailer_entry_col3:
            address = st.text_input(
                "Address",
                key="new_retailer_address"
            )

        with retailer_entry_col4:
            city = st.text_input(
                "City",
                value="Hazaribagh",
                key="new_retailer_city"
            )

        with retailer_entry_col5:
            state = st.selectbox(
                "State",
                ["Jharkhand"],
                key="new_retailer_state"
            )

        with retailer_entry_col6:
            pin_code = st.text_input(
                "PIN Code",
                value="825301",
                key="new_retailer_pin"
            )

        with retailer_entry_col7:
            phone_no = st.text_input(
                "Phone No",
                key="new_retailer_phone"
            )

        with retailer_entry_col8:
            status = st.selectbox(
                "Status",
                ["Active", "Inactive"],
                index=0,
                key="new_retailer_status"
            )

        with retailer_entry_col9:
            save_retailer = st.button(
                "💾 Save",
                use_container_width=True,
                key="save_new_retailer"
            )

    # =====================================================
    # SAVE RETAILER
    # =====================================================

    if save_retailer:

        if not shop_name.strip():

            st.warning("Please enter the Shop Name.")

        elif not proprietor_name.strip():

            st.warning("Please enter the Proprietor Name.")

        else:

            retailer_insert_query = text("""
                INSERT INTO Retailer (
                    Shop_Name,
                    Proprietor_Name,
                    Address,
                    City,
                    State,
                    Pin_Code,
                    Phone_No,
                    Created_Date,
                    Status
                )
                VALUES (
                    :shop_name,
                    :proprietor_name,
                    :address,
                    :city,
                    :state,
                    :pin_code,
                    :phone_no,
                    GETDATE(),
                    :status
                )
            """)

            try:

                with engine.begin() as connection:

                    connection.execute(
                        retailer_insert_query,
                        {
                            "shop_name": shop_name.strip(),
                            "proprietor_name": proprietor_name.strip(),
                            "address": address.strip(),
                            "city": city.strip(),
                            "state": state,
                            "pin_code": pin_code.strip(),
                            "phone_no": phone_no.strip(),
                            "status": status
                        }
                    )

                # Set reset flag
                st.session_state["retailer_entry_reset"] = True

                st.success(
                    f"Retailer '{shop_name}' added successfully."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Unable to save retailer: {e}"
                )
    # =====================================================
    # RETAILER CHARTS
    # =====================================================

    top_retailers_sales_query = text("""
        SELECT TOP 10
            r.Shop_Name,
            SUM(s.Order_Amount) AS Total_Selling
        FROM Sales s
        INNER JOIN Retailer r
            ON s.Retailer_Id = r.Retailer_Id
        WHERE CAST(s.Date AS DATE)
              BETWEEN :from_date AND :to_date
        GROUP BY r.Shop_Name
        ORDER BY Total_Selling DESC
    """)

    top_retailers_dues_query = text("""
        SELECT TOP 10
            r.Shop_Name,
            SUM(s.Dues_Amount) AS Total_Dues
        FROM Sales s
        INNER JOIN Retailer r
            ON s.Retailer_Id = r.Retailer_Id
        WHERE CAST(s.Date AS DATE)
              BETWEEN :from_date AND :to_date
        GROUP BY r.Shop_Name
        ORDER BY Total_Dues DESC
    """)

    with engine.connect() as connection:

        top_sales_rows = connection.execute(
            top_retailers_sales_query,
            {
                "from_date": from_date,
                "to_date": to_date
            }
        ).fetchall()

        top_dues_rows = connection.execute(
            top_retailers_dues_query,
            {
                "from_date": from_date,
                "to_date": to_date
            }
        ).fetchall()

    # =====================================================
    # CHARTS — SIDE BY SIDE
    # =====================================================

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.markdown(
            """
            <h4 style="
                color:#008B8F;
                margin-bottom:5px;
                font-weight:700;
            ">
            💰 Top Retailers — Selling Amount
            </h4>
            """,
            unsafe_allow_html=True
        )

        if top_sales_rows:

            sales_chart_df = pd.DataFrame(
                top_sales_rows,
                columns=[
                    "Shop_Name",
                    "Total_Selling"
                ]
            )

            fig_sales = px.bar(
                sales_chart_df,
                x="Shop_Name",
                y="Total_Selling",
                text="Total_Selling"
            )

            fig_sales.update_traces(
                marker_color="#00BCD4",
                texttemplate="₹ %{text:,.0f}",
                textposition="outside"
            )

            fig_sales.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=80
                ),
                xaxis_title="",
                yaxis_title="Selling Amount",
                showlegend=False
            )

            st.plotly_chart(
                fig_sales,
                use_container_width=True
            )

        else:

            st.info(
                "No retailer sales data available for the selected date range."
            )

    with chart_col2:

        st.markdown(
            """
            <h4 style="
                color:#008B8F;
                margin-bottom:5px;
                font-weight:700;
            ">
            💳 Top Retailers — Dues Amount
            </h4>
            """,
            unsafe_allow_html=True
        )

        if top_dues_rows:

            dues_chart_df = pd.DataFrame(
                top_dues_rows,
                columns=[
                    "Shop_Name",
                    "Total_Dues"
                ]
            )

            fig_dues = px.bar(
                dues_chart_df,
                x="Shop_Name",
                y="Total_Dues",
                text="Total_Dues"
            )

            fig_dues.update_traces(
                marker_color="#00BCD4",
                texttemplate="₹ %{text:,.0f}",
                textposition="outside"
            )

            fig_dues.update_layout(
                height=350,
                margin=dict(
                    l=20,
                    r=20,
                    t=20,
                    b=80
                ),
                xaxis_title="",
                yaxis_title="Dues Amount",
                showlegend=False
            )

            st.plotly_chart(
                fig_dues,
                use_container_width=True
            )

        else:

            st.info(
                "No retailer dues data available for the selected date range."
            )
    # =====================================================
    # RETAILER TABLES
    # =====================================================

    dues_table_query = text("""
        SELECT
            Shop_Name,
            Order_Id,
            Order_Amount,
            Paid_Amount,
            Dues_Amount,
            Due_Date,
            Payment_Status
        FROM Dues
        WHERE Dues_Amount > 0
        ORDER BY Due_Date ASC
    """)

    retailers_table_query = text("""
        SELECT
            Shop_Name,
            Proprietor_Name,
            Address,
            City,
            Phone_No,
            Status
        FROM Retailer
        ORDER BY Shop_Name
    """)

    with engine.connect() as connection:

        dues_rows = connection.execute(
            dues_table_query
        ).fetchall()

        retailer_rows = connection.execute(
            retailers_table_query
        ).fetchall()

    # =====================================================
    # TABLES — SIDE BY SIDE
    # =====================================================

    table_col1, table_col2 = st.columns(2)

    # -----------------------------------------------------
    # LEFT — DUES WITH RETAILERS
    # -----------------------------------------------------

    with table_col1:

        st.markdown(
            """
            <h4 style="
                color:#008B8F;
                margin-bottom:5px;
                font-weight:700;
            ">
            💳 Dues with Retailers
            </h4>
            """,
            unsafe_allow_html=True
        )

        if dues_rows:

            dues_df = pd.DataFrame(
                dues_rows,
                columns=[
                    "Shop_Name",
                    "Order_Id",
                    "Order_Amount",
                    "Paid_Amount",
                    "Dues_Amount",
                    "Due_Date",
                    "Payment_Status"
                ]
            )

            dues_df["Order_Amount"] = dues_df[
                "Order_Amount"
            ].apply(
                lambda x: f"₹ {float(x):,.2f}"
            )

            dues_df["Paid_Amount"] = dues_df[
                "Paid_Amount"
            ].apply(
                lambda x: f"₹ {float(x):,.2f}"
            )

            dues_df["Dues_Amount"] = dues_df[
                "Dues_Amount"
            ].apply(
                lambda x: f"₹ {float(x):,.2f}"
            )

            dues_df["Due_Date"] = pd.to_datetime(
                dues_df["Due_Date"]
            ).dt.strftime("%d-%m-%Y")

            st.dataframe(
                dues_df,
                use_container_width=True,
                hide_index=True,
                height=300
            )

        else:

            st.info(
                "No outstanding dues found."
            )

    # -----------------------------------------------------
    # RIGHT — TOTAL RETAILERS
    # -----------------------------------------------------

    with table_col2:

        st.markdown(
            """
            <h4 style="
                color:#008B8F;
                margin-bottom:5px;
                font-weight:700;
            ">
            🏪 Total Retailers
            </h4>
            """,
            unsafe_allow_html=True
        )

        if retailer_rows:

            retailers_df = pd.DataFrame(
                retailer_rows,
                columns=[
                    "Shop_Name",
                    "Proprietor_Name",
                    "Address",
                    "City",
                    "Phone_No",
                    "Status"
                ]
            )

            st.dataframe(
                retailers_df,
                use_container_width=True,
                hide_index=True,
                height=300
            )

        else:

            st.info(
                "No retailers found."
            )