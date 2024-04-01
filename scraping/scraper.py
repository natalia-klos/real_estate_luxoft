from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

class ScrapeWithDriver:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def scrape(self, home_page='https://www.sreality.cz/hledani/prodej/byty', max_elements=500, max_pages=100, max_pictures=1):
        property_data = {}
        page_num = 1
        for i in range(1, max_pages):
        #while len(property_data) < max_elements:
            self.driver.get(home_page + '?strana=' + str(page_num))
            sleep(1)

            soup=BeautifulSoup(self.driver.page_source, 'html.parser')
            property_elements = soup.find_all(class_="property ng-scope")
            page_num += 1

            for element in property_elements:
                if len(property_data) < max_elements:
                    title = element.find(class_="name ng-binding").text.strip()
                    image_links = [img['src'] for img in element.find_all('img') if (img['src'].startswith('https') & ~(img['src'].endswith('ffffff')) )]
                    property_data[title] = image_links
                else:
                    break
            
            data_for_db = []
            for title, img_address in property_data.items():
                dictionary = {'title': title, 'img_address': img_address}
                data_for_db.append(dictionary)

            for dct in data_for_db:
                dct['img_address'] = ' '.join(dct['img_address'][:max_pictures])

            return data_for_db
    


