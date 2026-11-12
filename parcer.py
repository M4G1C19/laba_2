from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

browser = webdriver.Chrome()
browser.get("https://catalog.onliner.by/mobile")

def get_all_links_on_page():
    product_elements = browser.find_elements(By.CLASS_NAME, value='catalog-form__link')

    links_array = []
    for element in product_elements:
        links_array.append(element.get_attribute('href'))
    
    return links_array

all_links = get_all_links_on_page()

def click_next_page():
    next_page_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[4]/div/div/div/div/div[3]/div[3]/a')))
    next_page_button.click()

click_next_page()
first_filtered_links = []

for link in all_links:
    if link == None or 'forum.' in link or 'tech.' in link:
        pass
    else:
        first_filtered_links.append(link)

len(first_filtered_links)
second_filtered_links = []

for link in first_filtered_links:
    if 'prices' in link or 'reviews' in link or 'used' in link:
        pass
    else:
        second_filtered_links.append(link)

len(second_filtered_links)

def initial_driver():
    chrome_executable_path = 'chrome-win/chrome.exe'
    chromedriver_executable_path = 'chromedriver_win32/chromedriver.exe'

    browser_options = webdriver.ChromeOptions()
    browser_options.binary_location = chrome_executable_path
    
    driver_service = Service(chromedriver_executable_path)
    new_browser = webdriver.Chrome(service=driver_service, options=browser_options)
    
    return new_browser

def anonymous_driver(version):
    anonymous_browser = initial_driver()

    user_agent_start = "Object.defineProperty(navigator, 'userAgent', {value: 'Mozilla/"
    user_agent_end = ".0 (Windows NT 40.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'});"
    
    anonymous_browser.execute_script(user_agent_start + str(version) + user_agent_end)

    return anonymous_browser

def clean_links(links: list):
    print(f'Start size of links list: {len(links)}')
    
    temp_filtered_links = []
    final_filtered_links = []

    for link in links:
        if link == None or 'forum.' in link or 'tech.' in link:
            pass
        else:
            temp_filtered_links.append(link)
            
    print(f'Current size of links list: {len(temp_filtered_links)}')

    for link in temp_filtered_links:
        if 'prices' in link or 'reviews' in link or 'used' in link:
            pass
        else:
            final_filtered_links.append(link)
            
    print(f'Finish size of links list: {len(final_filtered_links)}')

    return final_filtered_links

collected_links = []

try:
    for iteration in range(0, 5, 1):
        collected_links += get_all_links_on_page()
        click_next_page()
except:
    print("All done (catch block)")
    cleaned_links_list = clean_links(collected_links)
finally:
    print("All done (finally block)")
    cleaned_links_list = clean_links(collected_links)

with open('links.txt', 'a', encoding='utf-8') as output_file:
    for single_link in cleaned_links_list:
        output_file.write(f'{single_link}\n')

for first_link in cleaned_links_list:
    browser.get(first_link)
    break

def get_characteristics():
    characteristics_data = []
    characteristics_data.append({'Название модели': browser.find_element(By.CLASS_NAME, value='catalog-masthead__title').text})
    
    table_rows = browser.find_elements(By.CSS_SELECTOR, value='.product-specs__table tr')
    
    for row in table_rows:
        table_cells = row.find_elements(By.TAG_NAME, value='td')
        
        if len(table_cells) == 2:
            if not table_cells[1].text:
                if table_cells[1].find_elements(By.CLASS_NAME, value="i-x"):
                    characteristics_data.append({table_cells[0].text:'NO'})
                else:
                    characteristics_data.append({table_cells[0].text:'Yes'})
                                          
                characteristics_data.append({table_cells[0].text:table_cells[1].text})
            else:
                characteristics_data.append({table_cells[0].text:table_cells[1].text})
                
    return characteristics_data

result_table = pd.DataFrame()

for product_url in cleaned_links_list[0:3]:
    browser.get(product_url)

    new_row_data = pd.DataFrame([get_characteristics()])
    result_table = pd.concat([result_table, new_row_data], ignore_index=True)
    
print(result_table)