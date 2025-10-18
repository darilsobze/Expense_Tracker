import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px

BACKEND_URL = "http://127.0.0.1:5000"
st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
st.title("My Personal Expense Tracker")

st.write("Track your daily spending and get insights into your expenses.")

# Add a new Expense
st.subheader("➕ Add a New Expense")

with st.form("Expense_form"):
    description = st.text_input("Description")
    category = st.selectbox("Select a category", ["Food", "Transport", "Bills", "Shopping", "Other"])
    amount = st.number_input("Amount", 0.0)
    date = st.date_input("Date")
    submitted = st.form_submit_button("Add Expense")

if submitted:
    data = {
        "description": description,
        "category": category,
        "amount": amount,
        "date": str(date)
    }

    result = requests.post(f"{BACKEND_URL}/add_expense", json=data)

    if result.status_code == 200:
        st.success("Expenses added successfully!")
    else:
        st.error("Failed to add expense")

# load Expenses
st.subheader("📋 All Expenses")
result = requests.get(f"{BACKEND_URL}/get_expenses")

if result.status_code == 200:
    expenses = result.json()
    if len(expenses) == 0:
        st.info("No expenses yet. Add one above 👆")
    else:
        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date", ascending=False)

        st.dataframe(df, use_container_width=True)

        # Summary Section
        total_spent = df["amount"].sum()
        st.markdown(f"### 💵 Total Spent: **${total_spent:.2f}**")

        category_summary = df.groupby("category")["amount"].sum().reset_index()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Spending by Category")
            st.dataframe(category_summary, use_container_width=True)

        with col2:
            fig = px.pie(category_summary, values="amount", names="category", title="Category Breakdown")
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### 📆 Spending Over Time")
        trend = df.groupby("date")["amount"].sum().reset_index()
        fig2 = px.line(trend, x="date", y="amount", markers=True, title="Spending Trend")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("Failed to load expenses from backend.")
