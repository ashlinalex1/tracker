import pandas as pd
import streamlit as st
import plotly.express as px

# Load the expense data
FILENAME = 'expenses.csv'

@st.cache
def load_data():
    try:
        data = pd.read_csv(FILENAME, names=['Date', 'Category', 'Description', 'Amount'])
        data['Date'] = pd.to_datetime(data['Date'])
        data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')
        return data.dropna()
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Category', 'Description', 'Amount'])

# Streamlit App
st.title("Expense Tracker Dashboard")

# Load data
data = load_data()

if data.empty:
    st.warning("No data found. Please add expenses first!")
else:
    # Sidebar Filters
    st.sidebar.header("Filter Options")
    categories = data['Category'].unique()
    selected_category = st.sidebar.multiselect("Select Categories", categories, default=categories)

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [data['Date'].min(), data['Date'].max()],
        min_value=data['Date'].min(),
        max_value=data['Date'].max(),
    )

    # Filter data
    filtered_data = data[
        (data['Category'].isin(selected_category)) &
        (data['Date'] >= pd.Timestamp(date_range[0])) &
        (data['Date'] <= pd.Timestamp(date_range[1]))
    ]

    # Display filtered data
    st.subheader("Filtered Expenses")
    st.write(filtered_data)

    # Visualization: Expense Distribution
    st.subheader("Expense Distribution by Category")
    if not filtered_data.empty:
        fig = px.pie(filtered_data, values='Amount', names='Category', title='Expense Distribution')
        st.plotly_chart(fig)

    # Visualization: Expense Trends
    st.subheader("Expense Trends Over Time")
    if not filtered_data.empty:
        trend_fig = px.line(filtered_data, x='Date', y='Amount', color='Category', title='Expense Trends')
        st.plotly_chart(trend_fig)

    # Download Filtered Data
    st.subheader("Download Filtered Data")
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "filtered_expenses.csv", "text/csv", key='download-csv')
