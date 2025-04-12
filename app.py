import streamlit as st
import pandas as pd
import json
from datetime import datetime

FILENAME = "expenses.json"
def load_expenses():
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
            return pd.DataFrame(data)
    except FileNotFoundError:
        return pd.DataFrame(columns=["amount", "category", "note", "date"])

def save_expenses(df):
    df.to_json(FILENAME, orient="records", indent=4)

def main():
    st.set_page_config(page_title="Expense Tracker", layout="centered")
    st.title("Expense Tracker App")

    menu = ["Add Expense", "View Expenses", "Delete Expense"]
    choice = st.sidebar.selectbox("Select Action", menu)

    df = load_expenses()

    if choice == "Add Expense":
        st.subheader("Add a New Expense")
        amount = st.number_input("Enter amount (₹)")
        category = st.text_input("Category", placeholder="E.g. Food, Transport")
        note = st.text_input("Note (optional)", placeholder="Description")
        if st.button("Add Expense"):
            if amount == 0.0:
                st.warning("Please enter a valid amount greater than ₹0.")
            elif category.strip() == "":
                st.warning("Please enter a category.")
            else:
                new_expense = {
                    "amount": amount,
                    "category": category,
                    "note": note,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
                save_expenses(df)
                st.success("✅ Expense added!")
        
    elif choice == "View Expenses":
        st.subheader("All Expenses")
        if df.empty:
            st.info("No expenses recorded yet.")
        else:
            df['amount'] = df['amount'].astype(float)
            st.dataframe(df)
            total = df['amount'].sum()
            st.markdown(f"### Total Spent: ₹{total:.2f}")

    elif choice == "Delete Expense":
        st.subheader("Delete an Expense")
        if df.empty:
           st.info("No expenses to delete.")
        else:
           df_display = df.copy()
           df_display.index = df_display.index + 1  
           selected = st.selectbox("Select expense to delete (by index)", df_display.index)
           
           st.write(df_display.loc[selected]) 

           if st.button("Delete"):
               df = df.drop(index=selected - 1).reset_index(drop=True)
               save_expenses(df)
               st.success("✅ Expense deleted.")


if __name__ == "__main__":
    main()
