import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

@st.cache_data
def load_data(nrows):
    data = pd.read_csv('/Users/lilykuo/Desktop/MSBA/trendmarketplace/OnlineSalesData.csv', nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    data['Date'] = pd.to_datetime(data['Date'])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# Take a look at raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# show the revenues of each categories
st.subheader('Revenues of Each Category')
total_revenue_by_category = data.groupby('Product Category')['Total Revenue'].sum().sort_values(ascending=False)
# st.bar_chart(total_revenue_by_category)

fig = px.bar(
    total_revenue_by_category,
    x=total_revenue_by_category.index,
    y=total_revenue_by_category.values,
    labels={'x': 'Product Category', 'y': 'Total Revenue'}
)

# Rotate x-axis labels for better readability
fig.update_layout(xaxis_tickangle=-45)

# Display the plot in Streamlit
st.plotly_chart(fig)



# show the products sales of a specific category 
st.subheader('products sales of a specific category')

# add a widget to make user select category by themselves
category_option = st.selectbox(
    "Select a Category",
    (data['Product Category'].unique()),
)

# add a widget to make user select topX by themselves
top_option = st.slider("Top Sales of Product", 1, 20, 10)

# show the products sales of a specific category 
st.subheader(f'top {top_option} products sales of {category_option} category')
product_revenue_by_category = data[data['Product Category'] == category_option].groupby('Product Name')['Total Revenue'].sum().sort_values(ascending=False)
top_product_revenue_by_category = product_revenue_by_category[0:top_option]
# st.bar_chart(top_product_revenue_by_category)

# Create a bar plot using plotly.express
fig = px.bar(
    top_product_revenue_by_category,
    x=top_product_revenue_by_category.index,
    y=top_product_revenue_by_category.values,
    labels={'x': 'Product Name', 'y': 'Total Revenue'}
)

# Rotate x-axis labels for better readability
fig.update_layout(xaxis_tickangle=-45)

# Display the plot in Streamlit
st.plotly_chart(fig)


# show the sales with each payment method of a specific category
st.subheader(f'Payment method(s) of {category_option} category ')
payment_revenue_by_category = data[data['Product Category'] == category_option].groupby('Payment Method')['Total Revenue'].sum().sort_values(ascending=False)
# top_product_revenue_by_category = product_revenue_by_category[0:11]
# # st.bar_chart(top_product_revenue_by_category)

# Create a bar plot using plotly.express
fig = px.bar(
    payment_revenue_by_category,
    x=payment_revenue_by_category.index,
    y=payment_revenue_by_category.values,
    labels={'x': 'Payment Method', 'y': 'Total Revenue'}
)

# Rotate x-axis labels for better readability
fig.update_layout(xaxis_tickangle=-45)

# Display the plot in Streamlit
st.plotly_chart(fig)