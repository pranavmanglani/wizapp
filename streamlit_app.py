import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load and preprocess data
@st.cache
def load_data():
    data = pd.read_csv("sales_data.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    return data

data = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")
selected_product = st.sidebar.selectbox("Select Product", data['Product'].unique())
start_date = st.sidebar.date_input("Start Date", data['Date'].min())
end_date = st.sidebar.date_input("End Date", data['Date'].max())

# Filter data based on user input
filtered_data = data[(data['Product'] == selected_product) &
                     (data['Date'] >= pd.to_datetime(start_date)) &
                     (data['Date'] <= pd.to_datetime(end_date))]

# Display filtered data
st.write(f"### Sales Data for {selected_product}")
st.dataframe(filtered_data)

# Revenue trend chart
st.write("### Revenue Trend")
fig, ax = plt.subplots()
ax.plot(filtered_data['Date'], filtered_data['Revenue'], marker='o')
ax.set_xlabel('Date')
ax.set_ylabel('Revenue')
ax.set_title(f'Revenue Trend for {selected_product}')
plt.xticks(rotation=45)
st.pyplot(fig)

# Sales distribution by category
st.write("### Sales Distribution by Category")
category_sales = filtered_data.groupby('Category').agg({'Revenue': 'sum'}).reset_index()
fig = px.pie(category_sales, names='Category', values='Revenue', title='Sales Distribution by Category')
st.plotly_chart(fig)
