
import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from statsmodels.tsa.holtwinters import ExponentialSmoothing

import warnings
from statsmodels.tools.sm_exceptions import ConvergenceWarning

warnings.filterwarnings(
    "ignore",
    category=ConvergenceWarning
)

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Dashboard")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("retail_order_dataset1.csv")

    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    return df


df = load_data()

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(

    "Select Region",

    options=sorted(df["Region"].unique()),

    default=sorted(df["Region"].unique())

)

categories = st.sidebar.multiselect(

    "Select Category",

    options=sorted(df["Category"].unique()),

    default=sorted(df["Category"].unique())

)

date_range = st.sidebar.date_input(

    "Select Date Range",

    value=(

        df["OrderDate"].min(),

        df["OrderDate"].max()

    )

)

# ---------------------------------------------------
# Filter Data
# ---------------------------------------------------

filtered = df[

    (df["Region"].isin(regions))

    &

    (df["Category"].isin(categories))

]

if len(date_range) == 2:

    start_date = pd.to_datetime(date_range[0])

    end_date = pd.to_datetime(date_range[1])

    filtered = filtered[

        (filtered["OrderDate"] >= start_date)

        &

        (filtered["OrderDate"] <= end_date)

    ]

# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------

total_revenue = filtered["Revenue"].sum()

total_orders = filtered["OrderID"].nunique()

avg_order_value = filtered["Revenue"].mean()

top_region = (

    filtered

    .groupby("Region")["Revenue"]

    .sum()

    .idxmax()

)

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(

    "Total Revenue",

    f"${total_revenue:,.0f}"

)

col2.metric(

    "Total Orders",

    total_orders

)

col3.metric(

    "Average Order Value",

    f"${avg_order_value:,.2f}"

)

col4.metric(

    "Top Region",

    top_region

)

st.divider()

# ---------------------------------------------------
# Download Button
# ---------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Filtered Data",

    data=csv,

    file_name="filtered_sales.csv",

    mime="text/csv"

)

st.divider()

# ---------------------------------------------------
# Tabs
# ---------------------------------------------------

tab1, tab2, tab3, tab4, tab5 = st.tabs(

    [

        "Monthly Revenue Trend",

        "Top 10 Products",

        "EDA",

        "Customer Segments",

        "Forecast"

    ]

)
# ---------------------------------------------------
# Tab 1 : Monthly Revenue Trend
# ---------------------------------------------------

with tab1:

    monthly = (

        filtered

        .groupby(

            filtered["OrderDate"].dt.to_period("M")

        )["Revenue"]

        .sum()

        .reset_index()

    )

    monthly["OrderDate"] = monthly["OrderDate"].astype(str)

    fig = px.line(

        monthly,

        x="OrderDate",

        y="Revenue",

        markers=True,

        title="Monthly Revenue Trend"

    )

    fig.update_layout(

        xaxis_title="Month",

        yaxis_title="Revenue"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

# ---------------------------------------------------
# Tab 2 : Top 10 Products
# ---------------------------------------------------

with tab2:

    top_products = (

        filtered

        .groupby("Product")["Revenue"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )

    fig2 = px.bar(

        top_products,

        x="Product",

        y="Revenue",

        color="Revenue",

        text_auto=".2s",

        title="Top 10 Products by Revenue"

    )

    fig2.update_layout(

        xaxis_title="Product",

        yaxis_title="Revenue"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )

# ---------------------------------------------------
# Tab 3 : EDA
# ---------------------------------------------------

with tab3:

    st.subheader("Exploratory Data Analysis")

    metric = st.selectbox(

        "Select Metric",

        [

            "Revenue",

            "Qty",

            "UnitPrice",

            "Discount"

        ]

    )

    st.write("### Distribution")

    fig3 = px.histogram(
    
        filtered,
        
        x=metric,
        
        nbins=30,
        
        color_discrete_sequence=["skyblue"],
        
        title=f"{metric} Distribution"
        )

    fig3.update_traces(
        marker_line_color="black",
        marker_line_width=1
        )

    st.plotly_chart(

        fig3,

        use_container_width=True

    )

    st.write("### Box Plot")

    fig4 = px.box(

        filtered,

        y=metric,

        color_discrete_sequence=["royalblue"]

    )

    st.plotly_chart(

        fig4,

        use_container_width=True

    )

    # -----------------------------
    # Outlier Detection
    # -----------------------------

    Q1 = filtered[metric].quantile(0.25)

    Q3 = filtered[metric].quantile(0.75)

    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR

    upper = Q3 + 1.5 * IQR

    outliers = filtered[

        (filtered[metric] < lower)

        |

        (filtered[metric] > upper)

    ]

    st.write("### Outlier Summary")

    st.metric(

        "Number of Outliers",

        len(outliers)

    )

    st.dataframe(

        outliers.head(20),

        use_container_width=True

    )

# ---------------------------------------------------
# Tab 4 : Customer Segments
# ---------------------------------------------------

with tab4:

    st.subheader("Customer Segments (RFM Analysis)")

    # -----------------------------
    # Customer-level RFM Summary
    # -----------------------------

    rfm = (

        filtered

        .groupby("CustomerID")

        .agg(

            Recency=("OrderDate",
                     lambda x: (
                         filtered["OrderDate"].max()
                         + pd.Timedelta(days=1)
                         - x.max()
                     ).days),

            Frequency=("OrderID","count"),

            Monetary=("Revenue","sum"),

            Segment=("Segment","first")

        )

        .reset_index()

    )

    # -----------------------------
    # RFM Scatter
    # -----------------------------

    fig = px.scatter(

        rfm,

        x="Frequency",

        y="Monetary",

        color="Segment",

        size="Monetary",

        hover_data=["CustomerID","Recency"],

        title="Customer Segments"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )
    st.subheader("Segment Summary")
    
    #-----------------------
    #Add Segment Summary
    #-----------------------
    
    segment_summary = (

        rfm

        .groupby("Segment")

        .agg(

            Customers=("CustomerID","count"),

            AvgRecency=("Recency","mean"),

            AvgFrequency=("Frequency","mean"),

            AvgRevenue=("Monetary","mean")

        )

        .sort_values(

            "AvgRevenue",

            ascending=False

        )

        .reset_index()

    )

    st.dataframe(

        segment_summary,

        use_container_width=True

    )
    #-----------------------
    #Add Customer Count Bar Chart
    #-----------------------
    st.subheader("Customer Count by Segment")

    count = (

        rfm["Segment"]

        .value_counts()

        .reset_index()

    )

    count.columns = [

        "Segment",

        "Customers"

    ]

    fig2 = px.bar(

        count,

        x="Segment",

        y="Customers",

        color="Segment",

        text="Customers"

    )

    st.plotly_chart(

        fig2,

        use_container_width=True

    )
    #-----------------------
    #Segment Distribution Pie Chart
    #-----------------------
    
    fig3 = px.pie(
    count,
    names="Segment",
    values="Customers",
    title="Customer Segment Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
        )
# ---------------------------------------------------
# Tab 5 : Forecast
# ---------------------------------------------------

with tab5:

    st.subheader("3-Month Revenue Forecast")

    # -----------------------------
    # Monthly Revenue
    # -----------------------------

    monthly = (

        filtered

        .groupby(

            filtered["OrderDate"].dt.to_period("M")

        )["Revenue"]

        .sum()

    )

    monthly.index = monthly.index.to_timestamp()

    # -----------------------------
    # Holt-Winters Model
    # -----------------------------

    model = ExponentialSmoothing(

        monthly,

        trend="add",

        seasonal="add",

        seasonal_periods=12

    ).fit()

    forecast = model.forecast(3)

    # -----------------------------
    # Confidence Band (Approximate)
    # -----------------------------

    lower = forecast * 0.90

    upper = forecast * 1.10

    # -----------------------------
    # Plot Forecast
    # -----------------------------

    fig6 = go.Figure()

    # Actual Revenue

    fig6.add_trace(

        go.Scatter(

            x=monthly.index,

            y=monthly.values,

            mode="lines+markers",

            name="Actual Revenue"

        )

    )

    # Forecast

    fig6.add_trace(

        go.Scatter(

            x=forecast.index,

            y=forecast.values,

            mode="lines+markers",

            name="Forecast"

        )

    )

    # Upper Confidence

    fig6.add_trace(

        go.Scatter(

            x=forecast.index,

            y=upper.values,

            mode="lines",

            line=dict(width=0),

            showlegend=False

        )

    )

    # Lower Confidence

    fig6.add_trace(

        go.Scatter(

            x=forecast.index,

            y=lower.values,

            mode="lines",

            fill="tonexty",

            line=dict(width=0),

            name="Confidence Band"

        )

    )

    fig6.update_layout(

        title="Holt-Winters Forecast (Next 3 Months)",

        xaxis_title="Month",

        yaxis_title="Revenue"

    )

    st.plotly_chart(

        fig6,

        use_container_width=True

    )

    # -----------------------------
    # Forecast Table
    # -----------------------------

    forecast_df = pd.DataFrame({

        "Month": forecast.index,

        "Forecast Revenue": forecast.values,

        "Lower Bound": lower.values,

        "Upper Bound": upper.values

    })

    st.write("### Forecast Values")

    st.dataframe(

        forecast_df,

        use_container_width=True

    )

# ---------------------------------------------------
# Data Preview
# ---------------------------------------------------

st.divider()

st.subheader("Filtered Dataset")

st.dataframe(

    filtered,

    use_container_width=True

)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.divider()

st.caption("Sales Dashboard | Streamlit | Retail Analytics Project")
