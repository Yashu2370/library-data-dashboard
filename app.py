import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Layout Configurations
st.set_page_config(page_title="Library Analytics Dashboard", layout="wide", page_icon="📊")

# Custom Title Block matching an IT Profile
st.title("📊 Library Information & Resource Management Analytics")
st.markdown("""
*Developed by **Yashwanth K S** | Transitioning Library Professional to IT Systems Analytics*
***
This dashboard simulates transactional query logs from a Library Management System (LMS) database to visualize operational trends and resource utilization.
""")

# --- STEP A: SIMULATE THE DATABASE DATA ---
# In a real environment, this represents the output dataset from an optimized SQL query execution.
@st.cache_data
def load_library_transaction_data():
    categories = ['Computer Science', 'Data Analytics', 'Electronics', 'Mathematics', 'Management', 'Fiction']
    statuses = ['Returned', 'Issued', 'Overdue']
    
    np.random.seed(42)
    records = 250
    
    data = {
        'Transaction_ID': range(1001, 1001 + records),
        'Book_Category': np.random.choice(categories, size=records, p=[0.30, 0.25, 0.15, 0.10, 0.12, 0.08]),
        'Status': np.random.choice(statuses, size=records, p=[0.70, 0.20, 0.10]),
        'Days_Borrowed': np.random.randint(1, 30, size=records)
    }
    return pd.DataFrame(data)

df = load_library_transaction_data()

# --- STEP B: THE KPIS OVERVIEW ROW ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Database Records", value=len(df))
with col2:
    st.metric(label="Active Issued Books", value=len(df[df['Status'] == 'Issued']))
with col3:
    st.metric(label="Critical Overdue Flags", value=len(df[df['Status'] == 'Overdue']), delta="-2 this week", delta_color="inverse")
with col4:
    st.metric(label="Avg Loan Period (Days)", value=f"{df['Days_Borrowed'].mean():.1f} Days")

st.markdown("***")

# --- STEP C: DATA VISUALIZATIONS ---
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("📚 Resource Utilization by Category")
    # Aggregate data to show backend analytical capabilities
    cat_counts = df['Book_Category'].value_counts().reset_index()
    cat_counts.columns = ['Book Category', 'Total Checkouts']
    
    fig_bar = px.bar(
        cat_counts, 
        x='Total Checkouts', 
        y='Book Category', 
        orientation='h',
        color='Total Checkouts',
        color_continuous_scale='Blues',
        template='plotly_white'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with right_chart:
    st.subheader("⚠️ Inventory Distribution Status")
    status_counts = df['Status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    
    fig_pie = px.pie(
        status_counts, 
        values='Count', 
        names='Status', 
        hole=0.4,
        color_discrete_sequence=['#2ecc71', '#3498db', '#e74c3c']
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- STEP D: SIMULATED SQL INTERACTION VIEW ---
st.markdown("***")
st.subheader("🔍 Backend Database Query Filter")
st.caption("Filter records dynamically to simulate the parsing of raw SQL execution sets.")

category_filter = st.multiselect(
    "Select Book Categories to Drill Down:", 
    options=list(df['Book_Category'].unique()), 
    default=list(df['Book_Category'].unique())
)

filtered_df = df[df['Book_Category'].isin(category_filter)]
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
