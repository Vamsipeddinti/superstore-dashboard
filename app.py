# ============================================
# 🛒 SUPERSTORE SALES DASHBOARD - STREAMLIT
# ============================================

import pandas as pd
import plotly.express as px
import streamlit as st

# Page config
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 Superstore Sales Dashboard")
st.markdown("---")

# Data Load
@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv", encoding='latin1')
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['ship_date'] = pd.to_datetime(df['ship_date'])
    df['year'] = df['order_date'].dt.year
    df['month'] = df['order_date'].dt.month
    df['profit_margin'] = (df['profit'] / df['sales']) * 100
    return df

df = load_data()
st.success("✅ Data Loaded Successfully!")

# Sidebar Filters
st.sidebar.title("🔍 Filters")

# Year filter
years = sorted(df['year'].unique())
selected_years = st.sidebar.multiselect(
    "📅 Select Year",
    options=years,
    default=years
)

# Region filter
regions = sorted(df['region'].unique())
selected_regions = st.sidebar.multiselect(
    "🗺️ Select Region",
    options=regions,
    default=regions
)

# Category filter
categories = sorted(df['category'].unique())
selected_categories = st.sidebar.multiselect(
    "🏷️ Select Category",
    options=categories,
    default=categories
)

# Filter data
df_filtered = df[
    (df['year'].isin(selected_years)) &
    (df['region'].isin(selected_regions)) &
    (df['category'].isin(selected_categories))
]

# KPI Cards
st.subheader("📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Sales",
        value=f"${df_filtered['sales'].sum():,.0f}"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${df_filtered['profit'].sum():,.0f}"
    )

with col3:
    st.metric(
        label="🛒 Total Orders",
        value=f"{df_filtered['order_id'].nunique():,}"
    )

with col4:
    st.metric(
        label="📊 Avg Profit Margin",
        value=f"{df_filtered['profit_margin'].mean():.2f}%"
    )

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    # Sales by Region
    region_sales = df_filtered.groupby('region')['sales'].sum().reset_index()
    region_sales = region_sales.sort_values('sales', ascending=False)
    
    fig1 = px.bar(
        region_sales,
        x='region',
        y='sales',
        color='region',
        title='🗺️ Sales by Region',
        labels={'sales': 'Total Sales ($)', 'region': 'Region'},
        template='plotly_dark',
        text_auto='.2s'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Category wise Profit
    category_profit = df_filtered.groupby('category')['profit'].sum().reset_index()
    
    fig2 = px.pie(
        category_profit,
        values='profit',
        names='category',
        title='🏷️ Category wise Profit',
        template='plotly_dark',
        hole=0.4,
        color_discrete_map={
            'Technology': '#2E4057',
            'Office Supplies': '#C1666B',
            'Furniture': '#8B6914'
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Monthly Sales Trend
monthly_sales = df_filtered.groupby(
    df_filtered['order_date'].dt.to_period('M')
)['sales'].sum().reset_index()
monthly_sales['order_date'] = monthly_sales['order_date'].dt.to_timestamp()

fig3 = px.line(
    monthly_sales,
    x='order_date',
    y='sales',
    title='📈 Monthly Sales Trend',
    labels={'sales': 'Total Sales ($)', 'order_date': 'Month'},
    template='plotly_dark',
    markers=True
)
st.plotly_chart(fig3, use_container_width=True)
st.markdown("---")

# Top 10 Products
top10 = df_filtered.groupby('product_name')['sales'].sum().reset_index()
top10 = top10.nlargest(10, 'sales')

fig4 = px.bar(
    top10,
    x='sales',
    y='product_name',
    orientation='h',
    color='sales',
    title='🏆 Top 10 Products by Sales',
    labels={'sales': 'Total Sales ($)', 'product_name': 'Product'},
    template='plotly_dark',
    text_auto='.2s',
    color_continuous_scale='Blues'
)
fig4.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig4, use_container_width=True)
st.markdown("---")

# Raw Data Table
st.subheader("📋 Raw Data")

if st.checkbox("Show Raw Data"):
    st.dataframe(
        df_filtered,
        use_container_width=True
    )