import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from bs4 import BeautifulSoup
from time import sleep

# Update the CHROME_DRIVER_PATH with the path where Selenium Chrome Driver is installed for you.
CHROME_DRIVER_PATH = "path_to_chrome_driver"
LINK_TO_FORM = "https://forms.gle/HVGpZRkLvWP3rq4y9"
LINK_TO_HOUSING_SITE = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.53941573095703%2C%22east%22%3A-122.32724226904297%2C%22south%22%3A37.64913317663461%2C%22north%22%3A37.90123481692657%7D%2C%22mapZoom%22%3A12%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"


class RentalHouseFinder:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.price_list = []
        self.address_list = []
        self.link_list = []

    def fill_form(self):
        self.driver.get(LINK_TO_FORM)
        for index, price in enumerate(self.price_list):
            sleep(2)
            address_field = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price_field = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link_field = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            submit_button = self.driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
            address_field.send_keys(self.address_list[index])
            price_field.send_keys(self.price_list[index])
            link_field.send_keys(f"https://www.zillow.com/{self.link_list[index]}")
            submit_button.click()
            sleep(2)
            submit_new_response_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            submit_new_response_button.click()

    def collect_data(self):
        # Get the header information from http://myhttpheader.com/. Fill  in the values for the keys already posted
        headers = {
                "Accept-Language": "",
                "User-Agent": "",
            }
        response = requests.get(url=LINK_TO_HOUSING_SITE, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser", on_duplicate_attribute="replace")
        price_list = soup.find_all(class_="list-card-price")
        for price in price_list:
            self.price_list.append(price.text[:6])
        print(self.price_list)

        address_list = soup.find_all(class_="list-card-addr")
        for address in address_list:
            self.address_list.append(address.text)
        print(self.address_list)

        links_list = soup.find_all(class_="list-card-img")
        for link in links_list:
            self.link_list.append(link.get("href"))
        print(self.link_list)



scanner = RentalHouseFinder()

scanner.collect_data()
sleep(2)
scanner.fill_form()