import streamlit as st
import pandas as pd
import plotly.express as px

st.title("SmartStock Inventory Optimization Dashboard")
file_path = "../original_files/updated_dataset.csv"
df = pd.read_csv(file_path)
st.sidebar.header("Filter Options")

selected_products = st.sidebar.multiselect( "Select Product(s)", df["Product_Name"].unique(),
                                           default=df["Product_Name"].unique())
df = df[df["Product_Name"].isin(selected_products)]
col1, col2, col3 = st.columns(3)
col1.metric("Total Products", df["Product_Name"].nunique())
col2.metric("Total Sales", int(df["Total_Sales_Value"].sum()))
col3.metric("Average Units Sold", int(df["Units_Sold"].mean()))

st.subheader("Top 5 Best Selling Products")

category_sales = df.groupby("Product_Name")["Total_Sales_Value"].sum().reset_index()
top_products = category_sales.sort_values(
    by="Total_Sales_Value", ascending=False).head(5)

fig1 = px.bar(top_products,x="Product_Name",y="Total_Sales_Value",
    color="Total_Sales_Value",title="Top 5 Products")
st.plotly_chart(fig1)

st.subheader("Sales Trend by Products")
fig2 = px.line(category_sales,x="Product_Name",
    y="Total_Sales_Value",markers=True,title="Sales Trend by Products")
st.plotly_chart(fig2)

st.subheader("Price vs Units Sold")
fig3 = px.scatter(df,x="Price",y="Units_Sold",
    size="Opening_Stock",color="Product_Name",title="Price vs Units Sold")
st.plotly_chart(fig3)
# re-order and stock-out
latest_month = df["Month_Num"].max()
latest_df = df[df["Month_Num"] == latest_month].copy()
st.subheader("Stock-out Risk Products (Latest Month)")

latest_df["Sales_to_Stock_Ratio"] = latest_df["Units_Sold"] / latest_df["Opening_Stock"]
latest_df["Stockout_Risk"] = latest_df["Sales_to_Stock_Ratio"] > 0.7

if latest_df["Stockout_Risk"].any():
    st.warning(
        f" Some products are selling fast and may face stock-out risk in Month {latest_month}"
    )
    st.dataframe(
        latest_df[latest_df["Stockout_Risk"]][
            ["Product_Name", "Opening_Stock", "Units_Sold", "Sales_to_Stock_Ratio"]
        ]
    )
else:
    st.success("No stock-out risk detected in the latest month")

st.subheader("Reorder Stock Recommendations")
latest_df["Optimal_Stock"] = latest_df["Units_Sold"] * 1.2

latest_df["Reorder_Quantity"] = latest_df["Optimal_Stock"] - latest_df["Opening_Stock"]
latest_df["Reorder_Quantity"] = latest_df["Reorder_Quantity"].apply(
    lambda x: max(int(x), 0))
latest_df["Reorder_Required"] = latest_df["Reorder_Quantity"] > 0

if latest_df["Reorder_Required"].any():
    reorder_count = latest_df["Reorder_Required"].sum()
    st.error(f" Reorder Required for {reorder_count} product(s)!")
    st.dataframe(
        latest_df[latest_df["Reorder_Required"]][
            ["Product_Name", "Opening_Stock", "Optimal_Stock", "Reorder_Quantity"]
        ]
    )
else:
    st.success(" No immediate reorder required. Stock levels are sufficient.")
show_all = st.checkbox("Show Full Data (All Months)")

if show_all:
    st.dataframe(df)
