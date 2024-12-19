from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import json
import csv

service = Service()
options = webdriver.ChromeOptions()

data = []

# This will automatically install Chromedriver
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(120)

for i in range(1,6):

    driver.get("https://nhasachmienphi.com/category/?/page/"+str(i))

    # Chờ tất cả các phần tử với class name được tải
    books = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".col-xs-6.col-sm-3.col-md-3.col-lg-3.mg-b-30.item_sach"))
    )

    # In ra tất cả các liên kết
    for book in books:
        url = book.find_element(By.TAG_NAME, "a").get_attribute("href")  # Lấy href từ thẻ <a>
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        result = soup.find('div', class_='content_page pd-20')
        head = result.find('div', class_='col-xs-12 col-sm-8 col-md-8 col-lg-8')
        content = result.find('div', class_='content_p content_p_al')
        link_element = head.find_all('div', class_='mg-t-10')[0].find('div', class_='fb-like')["data-href"]
        title_element = head.find('h1', class_='tblue fs-20').text.strip()
        author_element = head.find_all('div', class_='mg-t-10')[1].text.replace('Tác giả: ', '').strip()
        category_element = head.find('div', class_='mg-tb-10').find('a', class_='tblue').text.strip()
        description_element = content.text.strip().replace('\n', ' ')

        data.append({
            "link": link_element,
            "title": title_element,
            "author": author_element,
            "category": category_element,
            "description": description_element
        })

print(json.dumps(data, ensure_ascii=False, indent=2))

# Xuất dữ liệu ra file CSV
with open("books.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["link", "title", "author", "category", "description"])
    writer.writeheader()
    writer.writerows(data)

print("Dữ liệu đã được lưu vào books.csv")

input("Nhấn Enter để đóng trình duyệt...")

driver.quit()
