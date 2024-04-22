import os
import requests
from bs4 import BeautifulSoup
import psycopg2
from dotenv import load_dotenv

# Define the Database class
class Database:
    def __init__(self, url):
        self.con = psycopg2.connect(url)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                price NUMERIC,
                rating VARCHAR(50)
            );
        """)
        self.con.commit()

    def insert_book(self, book):
        self.cur.execute("INSERT INTO books (title, price, rating) VALUES (%s, %s, %s)", 
                         (book['title'], book['price'], book['rating']))
        self.con.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

# Function to scrape books
def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    books = []
    for book in soup.find_all("article", class_="product_pod"):
        title = book.find("h3").find("a")["title"]
        price = book.find('p', class_='price_color').text
        rating = book.p['class'][1]
        books.append({
            'title': title,
            'price': float(price[1:]),  # Assuming the price is like '£51.77'
            'rating': rating
        })
    return books

# Load environment variables
load_dotenv()
database_url = os.getenv('DATABASE_URL')

# Main execution
if __name__ == "__main__":
    url = "http://books.toscrape.com"
    books = scrape_books(url)
    
    with Database(database_url) as db:
        db.create_table()
        for book in books:
            db.insert_book(book)
