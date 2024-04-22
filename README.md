### Book Scraper and Viewer
This project contains a Python scraper that collects book data from "http://books.toscrape.com" and a Streamlit application that allows users to view and interact with the scraped data.

## Getting Started
First Time Setup
Follow these steps to set up the project on your local machine for the first time:

## Create a Virtual Environment (Optional but recommended):
python -m venv venv
# Activate the Virtual Environment:
Linux/macOS:
source venv/bin/activate
Windows:
.\venv\Scripts\activate
## Install Dependencies:
pip install -r requirements.txt
## Future Runs
# Run the Streamlit App:
streamlit run app.py
# Functionality
Scraper: The scraper script (scraper_script.py) visits "http://books.toscrape.com", extracts data about books, and stores it in a database.
Streamlit App: The app.py is a Streamlit application that reads the scraped data from the database and provides a user-friendly interface to filter and view the book data.
# Configuration
Make sure to update the DATABASE_URL in the .env file or set this environment variable appropriately to point to your PostgreSQL database.
Adjust the cron job in the GitHub Actions workflow (/.github/workflows/scraper.yml) if you wish to change the scraping frequency.

## License
This project is open source and available under the MIT License.