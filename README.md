# Sales_Dashboard

An interactive business intelligence dashboard developed using Streamlit to analyze retail sales data. The dashboard provides real-time insights through dynamic filters, KPI cards, interactive visualizations, customer segmentation, exploratory data analysis (EDA), and sales forecasting.

# Project Overview:

- Retail sales analytics dashboard built using Streamlit.
- Interactive visualizations.
- Customer segmentation using RFM and K-Means.
- Time-series forecasting using Holt–Winters.
- Data filtering and CSV export.

# Features:

- Sidebar filters (Region, Category, Date Range)
- KPI Cards
- Monthly Revenue Trend
- Top 10 Products
- EDA
- Interactive Plotly Charts
- Customer Segmentation
- Forecasting
- Download CSV
- Built with Streamlit and Pandas

# Tech Stack:

- Python
- Streamlit
- Pandas
- Plotly

# Data Dictionary:

| Column       | Description             |
| ------------ | ----------------------- |
| OrderID      | Unique order identifier |
| OrderDate    | Order date              |
| CustomerID   | Customer identifier     |
| CustomerName | Customer name           |
| Region       | Sales region            |
| Category     | Product category        |
| Product      | Product name            |
| Qty          | Quantity sold           |
| UnitPrice    | Price per unit          |
| Revenue      | Qty × UnitPrice         |
| Discount     | Discount (%)            |
| Cluster      | K-Means cluster         |
| Segment      | Customer segment        ||

# Architecture Diagram:

                            Retail Sales Dataset
                         (merged_master.csv)
                                   │
                                   ▼
                      Data Loading (Pandas)
                                   │
                                   ▼
                Data Preprocessing & Cleaning
        (Date Conversion, Missing Values, Filtering)
                                   │
                                   ▼
                   Interactive Sidebar Filters
           (Region, Category, Date Range Selection)
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
      KPI Calculations      Exploratory Data      Customer Analytics
 (Revenue, Orders, AOV,     Analysis (EDA)       (RFM + K-Means)
    Top Region)             Histogram, Box Plot,
                             Outlier Detection
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   │
                                   ▼
                    Time Series Forecasting
             (Monthly Revenue + Holt-Winters Model)
                                   │
                                   ▼
                     Interactive Plotly Charts
      (Line Chart, Bar Chart, Scatter Plot, Pie Chart)
                                   │
                                   ▼
                      CSV Download & Data Preview
                                   │
                                   ▼
                    Streamlit Web Dashboard

# Key Findings:

1. Overall Sales Performance

* The retail dataset contains **50,000 customer orders** recorded between **01 January 2021 and 31 December 2023**.
* The business generated a **total revenue of $718,119,957** during the analysis period.
* The **average order value** was **$14,362.40**, indicating a relatively high-value transaction dataset.

---

# 2. Regional Performance

* The **East region** generated the highest overall revenue among all sales regions.
* This suggests that the East region contributed the largest share of the company's total sales and represents the strongest performing market.

---

# 3. Monthly Revenue Trend

* Revenue fluctuated throughout the three-year period, indicating seasonal and business-cycle variations.
* The **highest monthly revenue** was recorded in **May 2021**.
* The **lowest monthly revenue** occurred in **February 2022**.
* Despite month-to-month fluctuations, the business maintained consistently high monthly revenue throughout the analysis period.

---

# 4. Product Performance

* Sports equipment products such as **Cricket Bat**, **Basketball**, **Football**, **Volleyball**, and **Tennis Racket** generated the highest revenue.
* The **Cricket Bat** was the highest revenue-generating product.
* These products represent the company's strongest revenue contributors and could be prioritized for inventory planning and marketing campaigns.

---

# 5. Revenue Distribution

* The revenue distribution is **positively (right) skewed**.
* Most customer orders generated relatively low to moderate revenue, while a smaller number of orders contributed exceptionally high revenue.
* This indicates the presence of a few high-value transactions that significantly influence total revenue.

---

# 6. Outlier Analysis

* The box plot identified **332 revenue outliers** using the Interquartile Range (IQR) method.
* These outliers likely correspond to bulk purchases or premium-value orders rather than data quality issues.
* Such transactions should be reviewed separately before making business decisions based on average revenue.

---

# 7. Customer Segmentation

Using **RFM Analysis** and **K-Means Clustering**, customers were divided into four meaningful segments:

-> Loyal Customers - Largest customer group with consistent purchasing behaviour.                     
-> Regular Customers - Stable customers with moderate purchase frequency and revenue contribution.      
-> Champions - High-value customers with excellent purchase frequency and the highest spending.  
-> At-Risk Customers - Customers with low recent activity who may require retention strategies.       

**Observation:**

* Loyal Customers constitute the largest customer segment.
* Champions contribute significantly despite representing a smaller percentage of customers.
* At-Risk Customers should be targeted with promotional campaigns to improve retention.

---

# 8. Sales Forecast

The Holt–Winters forecasting model predicts the following revenue for the next three months:

| Month         |   Forecast Revenue |
| ------------- | -----------------: |
| January 2024  | **$20.24 Million** |
| February 2024 | **$18.26 Million** |
| March 2024    | **$19.91 Million** |

The forecast indicates:

* A slight decline in February 2024.
* Revenue recovery during March 2024.
* Overall revenue is expected to remain around **$18–20 million per month**, suggesting stable future sales performance.

---

# Overall Conclusion

The dashboard demonstrates that the business maintained **strong and consistent sales performance** over the three-year period, generating more than **$718 million** in revenue. The **East region** emerged as the top-performing market, while sports-related products contributed the highest sales. Customer segmentation revealed a large base of **Loyal Customers** alongside a valuable **Champions** segment, highlighting opportunities for customer retention and targeted marketing. Revenue forecasting suggests that sales are expected to remain stable during the first quarter of 2024, providing confidence for future planning and inventory management.


# 🚀 Live Demo:

Streamlit App: https://sales-dashboard-keerthana-bharath.streamlit.app
