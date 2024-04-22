import psycopg2

class Database:
    def __init__(self, database_url):
        self.con = psycopg2.connect(database_url)
        self.cur = self.con.cursor()
        self.setup_database()

    def setup_database(self):
        self.create_books_table()
        self.update_books_table()

    def create_books_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            price NUMERIC(5,2) NOT NULL,
            rating TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(q)
        self.con.commit()

    def update_books_table(self):
        # This method can be used to add new columns if needed
        q = """
        ALTER TABLE books
        ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '';
        """
        try:
            self.cur.execute(q)
            self.con.commit()
        except Exception as e:
            print(f"Error updating table: {e}")

    def insert_book(self, book):
        q = """
        INSERT INTO books (title, price, rating, description) VALUES (%s, %s, %s, %s)
        """
        self.cur.execute(q, (book['title'], book['price'], book['rating'], book['description']))
        self.con.commit()

    def search_books(self, name_query, description_query, sort_by, order):
        q = f"""
        SELECT title, price, rating, description FROM books
        WHERE title ILIKE %s AND description ILIKE %s
        ORDER BY {sort_by} {'ASC' if order == 'ascending' else 'DESC'}
        """
        search_term = f"%{name_query}%"
        description_term = f"%{description_query}%"
        self.cur.execute(q, (search_term, description_term))
        return self.cur.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()
