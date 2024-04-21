# investing-web-info
# Economic Data Scraper

This Python script scrapes economic data from the Investing.com economic calendar, updates the 'IMP' column based on the number of 'grayFullBullishIcon' icons, and saves the data to CSV files in a folder named with today's date.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Chrome Browser
- ChromeDriver compatible with the version of your Chrome browser

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>


2. pip install -r requirements.txt

Download ChromeDriver:


Go to the ChromeDriver Downloads page.


Download the version of ChromeDriver that matches your Google Chrome version.
Extract the downloaded file and note the path to the chromedriver executable.
Update the script with your ChromeDriver path:
Open the script and replace the executable_path in the Service object with the path to your chromedriver.


python scrape_and_save_economic_data.py