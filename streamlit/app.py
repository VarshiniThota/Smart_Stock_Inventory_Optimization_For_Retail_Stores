import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SmartStore Inventory Optimization Dashboard")

file_path="../original_files/updated_dataset.csv"
df=pd.read_csv(file_path)

st.subheader("Total Sales by Product")
fig1 = px.bar(df, x="Product_Name", y="Total_Sales_Value",
              color="Total_Sales_Value")
st.plotly_chart(fig1)

st.subheader("Sales Trend by Products")
category_sales = df.groupby("Product_Name")["Total_Sales_Value"].sum().reset_index()
fig2 = px.line(category_sales, x="Product_Name", y="Total_Sales_Value", markers=True,
              title="Sales Trend by products")
st.plotly_chart(fig2)



st.subheader("Price vs Units Sold")
fig3 = px.scatter(df, x="Price", y="Units_Sold",
                  size="Opening_Stock", color="Product_Name")
st.plotly_chart(fig3)

st.subheader("Stock-out Risk Products")
df["Sales_to_Stock_Ratio"] = df["Units_Sold"] / df["Opening_Stock"]
df["Stockout_Risk"] = df["Sales_to_Stock_Ratio"] > 0.7
st.dataframe(df[df["Stockout_Risk"] == True])
