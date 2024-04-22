import streamlit as st
import pandas as pd
import os
from db import Database  # Make sure to adjust import path as needed
from dotenv import load_dotenv

load_dotenv()

# Function to establish a connection to the database
def connect_db():
    return Database(os.getenv("DATABASE_URL"))

# Function to fetch books data from the database with optional filters and sorting
def fetch_books(search_query='', sort_by='title', order='asc'):
    db = connect_db()
    try:
        books = db.search_books(search_query, search_query, sort_by, order)
        df = pd.DataFrame(books, columns=['Title', 'Price', 'Rating', 'Description'])
        return df
    finally:
        db.__exit__(None, None, None)

# Streamlit webpage setup
st.title('Book Display, Filter, and Search Portal')

# Search and filter options
search_query = st.text_input('Search for books (title, description)')
sort_options = ['title', 'price', 'rating', 'description']
sort_by = st.selectbox('Sort by', sort_options, index=0)
order_options = ['asc', 'desc']
order = st.selectbox('Order', order_options, index=0)

# Fetch and display books
books_df = fetch_books(search_query=search_query, sort_by=sort_by, order=order)
if not books_df.empty:
    st.write("Books found:", books_df.shape[0])
    st.dataframe(books_df)
else:
    st.write("No books found.")
