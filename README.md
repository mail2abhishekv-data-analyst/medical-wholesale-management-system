# Medical Wholesale Management System

A Python and Streamlit-based Medical Wholesale Management System designed to manage medicine inventory, sales, retailers, dues, and business performance through an interactive dashboard.

## Project Overview

This project demonstrates the development of a database-driven business application using Python, Streamlit, SQL Server, SQLAlchemy, and Plotly.

The system provides a centralized interface for managing medicines, recording sales, maintaining retailer information, tracking outstanding dues, and monitoring business performance through interactive dashboards.

## Key Features

* Business performance dashboard
* Sales management and billing
* Medicine inventory management
* Retailer management
* Retailer dues tracking
* Medicine search and filtering
* Automatic discount calculation
* Selling price calculation
* Stock quantity management
* Expiry and near-expiry monitoring
* Duplicate medicine detection
* Sales trend analysis
* Top-selling medicine analysis
* Retailer sales analysis
* Retailer dues analysis
* SQL Server database integration
* Interactive Plotly charts
* Streamlit-based user interface

## Application Pages

### Dashboard

Provides an overall view of business performance, including:

* Total sales
* Total orders
* Total dues
* Active retailers
* Sales trends
* Top-selling medicines
* Retailer performance
* Sales and dues analysis

### Sales

The Sales page allows users to:

* Create new sales
* Select retailers
* Search medicines
* Add medicines to a sale
* Calculate discounts
* Calculate selling amounts
* Record paid amounts
* Track outstanding dues
* View sales history
* Analyze sales trends

### Medicine

The Medicine page provides:

* Medicine master data
* Inventory information
* Manufacturer filtering
* Medicine type filtering
* Stock monitoring
* Low-stock identification
* Out-of-stock identification
* Duplicate medicine detection
* Near-expiry medicine monitoring
* Top-selling medicine analysis

### Retailers & Payments

The Retailer section provides:

* New retailer registration
* Retailer information management
* Retailer sales analysis
* Retailer dues analysis
* Outstanding dues tracking
* Payment status monitoring

## Technology Stack

| Technology    | Purpose                    |
| ------------- | -------------------------- |
| Python        | Application development    |
| Streamlit     | Web application interface  |
| SQL Server    | Database management        |
| SQLAlchemy    | Database connectivity      |
| PyODBC        | SQL Server connection      |
| Pandas        | Data processing            |
| Plotly        | Interactive visualizations |
| python-dotenv | Environment configuration  |

## Database

The application uses Microsoft SQL Server as its backend database.

The database contains business entities for:

* Medicines
* Sales
* Sales details
* Retailers
* Dues

The application communicates with SQL Server through SQLAlchemy and PyODBC.

## Project Structure

```text
Medical_Wholesale_App/
│
├── app.py
├── database.py
├── sales.py
├── medicine.py
├── retailer.py
├── dues.py
├── launcher.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Configuration

Database configuration is stored locally using environment variables.

The `.env` file is intentionally excluded from the repository and should never be committed to GitHub.

Example configuration:

```text
MEDICAL_DB_SERVER=your_server
MEDICAL_DB_NAME=Medical_Wholesale_DB
MEDICAL_DB_DRIVER=ODBC Driver 17 for SQL Server
```

## Running the Application

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Configure the local SQL Server connection using the `.env` file.

Then start the application:

```bash
streamlit run app.py
```

## Important Note

This repository is intended as a portfolio and demonstration project.

The application currently uses a local SQL Server environment and therefore requires appropriate SQL Server configuration and database setup before deployment on another computer.

Production deployment would require additional hardening such as database backup and recovery procedures, user authentication and authorization, audit logging, enhanced transaction controls, and deployment-specific configuration.

## Project Purpose

This project demonstrates practical skills in:

* Python application development
* SQL Server database design
* Database connectivity
* Data processing
* Business application development
* Inventory management
* Sales management
* Dashboard development
* Data visualization
* Streamlit application development

## Author

**Abhishek Verma**

Data Analyst | Excel | SQL | Power BI | Python | Data Cleaning & Dashboards
