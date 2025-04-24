import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import re

st.set_page_config(page_title="Simple Finance App", page_icon="💰", layout="wide")

category_file = "categories.json"

# Initialize session state for categories
if "categories" not in st.session_state:
    st.session_state.categories = {"Uncategorized": []}
if os.path.exists(category_file):
    with open(category_file, "r") as f:
        st.session_state.categories = json.load(f)

def save_categories():
    """Save categories to JSON file."""
    with open(category_file, "w") as f:
        json.dump(st.session_state.categories, f)

def categorize_transactions(df):
    """Categorize transactions based on keywords using substring matching."""
    df["Category"] = "Uncategorized"
    for category, keywords in st.session_state.categories.items():
        if category == "Uncategorized" or not keywords:
            continue
        pattern = "|".join(re.escape(keyword.lower()) for keyword in keywords)
        mask = df["Details"].str.lower().str.contains(pattern, na=False)
        df.loc[mask & (df["Category"] == "Uncategorized"), "Category"] = category
    return df

def add_keyword_to_category(category, keyword):
    """Add a keyword to a category with a warning if it exists elsewhere."""
    keyword = keyword.lower().strip()
    for cat, keywords in st.session_state.categories.items():
        if keyword in keywords and cat != category:
            st.warning(f"Keyword '{keyword}' already exists in category '{cat}'. It will be assigned to '{cat}' first.")
            break
    if keyword and keyword not in st.session_state.categories[category]:
        st.session_state.categories[category].append(keyword)
        save_categories()
        return True
    return False

def load_transactions(file):
    """Load and process transaction data from CSV."""
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns]
        df["Amount"] = df["Amount"].str.replace(",", "").astype(float)
        df["Date"] = pd.to_datetime(df["Date"], format="%d %b %Y")
        return categorize_transactions(df)
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def main():
    st.title("Simple Finance Dashboard")

    uploaded_file = st.file_uploader("Upload your transaction CSV file", type=["csv"])

    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        if df is not None:
            debits_df = df[df["Debit/Credit"] == "Debit"].copy()
            credits_df = df[df["Debit/Credit"] == "Credit"].copy()
            st.session_state.debits_df = debits_df.copy()

            tab1, tab2, tab3 = st.tabs(["Expenses (Debits)", "Payments (Credits)", "Category Management"])

            with tab1:
                st.subheader("Filter Transactions")
                col1, col2 = st.columns(2)
                with col1:
                    start_date = st.date_input("Start Date", value=st.session_state.debits_df["Date"].min())
                with col2:
                    end_date = st.date_input("End Date", value=st.session_state.debits_df["Date"].max())

                selected_categories = st.multiselect(
                    "Select Categories",
                    options=list(st.session_state.categories.keys()),
                    default=list(st.session_state.categories.keys())
                )

                filtered_df = st.session_state.debits_df[
                    (st.session_state.debits_df["Date"] >= pd.to_datetime(start_date)) &
                    (st.session_state.debits_df["Date"] <= pd.to_datetime(end_date)) &
                    (st.session_state.debits_df["Category"].isin(selected_categories))
                ]

                st.subheader("Your Expenses")
                edited_df = st.data_editor(
                    filtered_df[["Date", "Details", "Amount", "Category"]],
                    column_config={
                        "Date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
                        "Amount": st.column_config.NumberColumn("Amount", format="%.2f AED"),
                        "Category": st.column_config.SelectboxColumn(
                            "Category",
                            options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index=True,
                    use_container_width=True,
                    key="category_editor"
                )

                save_button = st.button("Apply Changes", type="primary")
                if save_button:
                    for idx in edited_df.index:
                        new_category = edited_df.at[idx, "Category"]
                        if new_category != st.session_state.debits_df.at[idx, "Category"]:
                            st.session_state.debits_df.at[idx, "Category"] = new_category

                if st.button("Recategorize Transactions"):
                    st.session_state.debits_df = categorize_transactions(st.session_state.debits_df)
                    st.rerun()

                st.subheader("Expense Summary")
                total_expenses = filtered_df["Amount"].sum()
                st.metric("Total Expenses", f"{total_expenses:,.2f} AED")

                category_totals = filtered_df.groupby("Category")["Amount"].sum().reset_index()
                category_totals = category_totals.sort_values("Amount", ascending=False)

                st.dataframe(
                    category_totals,
                    column_config={"Amount": st.column_config.NumberColumn("Amount", format="%.2f AED")},
                    use_container_width=True,
                    hide_index=True
                )

                fig = px.pie(category_totals, values="Amount", names="Category", title="Expenses by Category")
                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.subheader("Payments Summary")
                total_payments = credits_df["Amount"].sum()
                st.metric("Total Payments", f"{total_payments:,.2f} AED")
                st.write(credits_df)

            with tab3:
                st.subheader("Manage Categories")

                new_category = st.text_input("New Category Name", key="new_category")
                if st.button("Add Category", key="add_category"):
                    if new_category and new_category not in st.session_state.categories:
                        st.session_state.categories[new_category] = []
                        save_categories()
                        st.rerun()
                    elif new_category in st.session_state.categories:
                        st.error("Category already exists.")

                for category in list(st.session_state.categories.keys()):
                    if category == "Uncategorized":
                        continue
                    with st.expander(category):
                        st.write("Keywords:")
                        for keyword in st.session_state.categories[category]:
                            col1, col2 = st.columns([3, 1])
                            col1.write(keyword)
                            if col2.button("Remove", key=f"remove_{category}_{keyword}"):
                                st.session_state.categories[category].remove(keyword)
                                save_categories()
                                st.rerun()

                        new_keyword = st.text_input("Add new keyword", key=f"new_keyword_{category}")
                        if st.button("Add Keyword", key=f"add_keyword_{category}"):
                            if new_keyword:
                                add_keyword_to_category(category, new_keyword)
                                st.rerun()

                        if st.button("Delete Category", key=f"delete_{category}"):
                            st.session_state[f"confirm_delete_{category}"] = True

                        if st.session_state.get(f"confirm_delete_{category}", False):
                            st.write(f"Are you sure you want to delete '{category}'? Transactions will be set to 'Uncategorized'.")
                            col1, col2 = st.columns(2)
                            if col1.button("Confirm Delete", key=f"confirm_delete_{category}"):
                                del st.session_state.categories[category]
                                if "debits_df" in st.session_state:
                                    st.session_state.debits_df.loc[
                                        st.session_state.debits_df["Category"] == category, "Category"
                                    ] = "Uncategorized"
                                save_categories()
                                st.rerun()
                            if col2.button("Cancel", key=f"cancel_delete_{category}"):
                                st.session_state[f"confirm_delete_{category}"] = False
                                st.rerun()

if __name__ == "__main__":
    main()