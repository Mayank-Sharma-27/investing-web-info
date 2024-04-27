from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from datetime import datetime


def scrape_and_save_economic_data(csv_file_prefix='economic_calendar_data'):
    """
    Scrapes economic data for each filter in 'economicCalendarFilters', updates the 'IMP' column based on the number of 'grayFullBullishIcon',
    and saves it to CSV files in a folder named with today's date, except for the filter named 'Filters'.
    """
    # Setup Chrome options for headless execution
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1200")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Setup Selenium WebDriver with the correct path to the chromedriver
    service = Service(
        executable_path='/Users/mayank/workspace/investing-web-info/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://www.investing.com/economic-calendar/')

    # Wait for the filters to load
    filters = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "#economicCalendarFilters a"))
    )

    # Create a folder named with today's date
    today_date = datetime.now().strftime('%Y-%m-%d')
    folder_path = os.path.join(os.getcwd(), today_date)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Iterate over each filter
    for filter_element in filters:
        filter_name = filter_element.text.strip()
        if filter_name != "Filters":  # Check if the filter name is not "Filters"
            print(f"Scraping data for filter: {filter_name}")

            # Click the filter element
            driver.execute_script("arguments[0].click();", filter_element)

            # Wait for the table to update and scroll to load dynamic data
            time.sleep(5)  # Initial wait for some data to load
            last_height = driver.execute_script(
                "return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(3)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # Extract the table data
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "economicCalendarData"))
            )
            html_content = table.get_attribute('outerHTML')
            soup = BeautifulSoup(html_content, 'html.parser')
            df = pd.read_html(str(soup))[0]

            # Update the 'IMP' column based on the number of 'grayFullBullishIcon'
            imp_column_index = 2
            for row in df.itertuples():
                cell_html = soup.select_one(
                    f'tr:nth-of-type({row.Index + 1}) td:nth-of-type({imp_column_index + 1})')
                if cell_html:
                    count = len(cell_html.select('.grayFullBullishIcon'))
                    df.at[row.Index, df.columns[imp_column_index]] = count

            # Save the DataFrame to a CSV file in the created folder
            csv_file_name = f"{csv_file_prefix}_{filter_name.replace(' ', '_')}.csv"
            csv_file_path = os.path.join(folder_path, csv_file_name)
            df.to_csv(csv_file_path, index=False)
            print(f"Data successfully saved to {csv_file_path}")

    # Close the browser
    driver.quit()


# Call the function
scrape_and_save_economic_data()
