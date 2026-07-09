
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Dashboard1")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("merged_master.csv")
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df

df = load_data()

# ---------------------------------------------------
# Sidebar Filters
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
    (df["Region"].isin(regions)) &
    (df["Category"].isin(categories))
]

if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    filtered = filtered[
        (filtered["OrderDate"] >= start_date) &
        (filtered["OrderDate"] <= end_date)
    ]

# ---------------------------------------------------
# KPI Calculations
# ---------------------------------------------------

total_revenue = filtered["Revenue"].sum()

total_orders = filtered["OrderID"].nunique()

avg_order = filtered["Revenue"].mean()

top_region = (
    filtered.groupby("Region")["Revenue"]
    .sum()
    .idxmax()
)

# ---------------------------------------------------
# KPI Row
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
    f"${avg_order:,.2f}"
)

col4.metric(
    "Top Region",
    top_region
)

st.divider()

# ---------------------------------------------------
# Tabs
# ---------------------------------------------------

tab1, tab2 = st.tabs([
    "Monthly Revenue Trend",
    "Top 10 Products"
])

# ---------------------------------------------------
# Tab 1
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
# Tab 2
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
        title="Top 10 Products by Revenue",
        text_auto=".2s"
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
# Data Preview
# ---------------------------------------------------

st.divider()

st.subheader("Filtered Dataset")

st.dataframe(
    filtered,
    use_container_width=True
)
