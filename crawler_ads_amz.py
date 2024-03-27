import configparser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import re
from PIL import Image
import easyocr
import time
import queue
import csv
import threading


def image_to_text_easyocr(image_path):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_path)
    text = ' '.join([entry[1] for entry in result])
    return text


def form_captcha(driver, image_captcha, count):
    if image_captcha:
        div_image = [image.find("img") for image in image_captcha]
        url_image = div_image[0].get("src")
        response = requests.get(url_image, stream=True)
        folder_ing_captcha = "image captcha"
        if not os.path.exists(folder_ing_captcha):
            os.mkdir(folder_ing_captcha)
        file_name = f"{count}.jpg"
        path_file_name = os.path.join(folder_ing_captcha, file_name)
        with open(path_file_name, "wb") as f:
            f.write(response.content)
        if path_file_name:
            image = Image.open(path_file_name)
            result_text = image_to_text_easyocr(image)
        input_element = driver.find_element(By.XPATH, '//*[@id="captchacharacters"]')
        input_element.send_keys(result_text)
        button = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
        button.click()


def get_link(link_img, count):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    ChromeDriverManager().install()
    driver = webdriver.Chrome(options=chrome_options)
    screen_width = driver.execute_script("return window.screen.availWidth;")
    screen_height = driver.execute_script("return window.screen.availHeight;")
    driver.set_window_size(screen_width, screen_height)
    driver.get(link_img)
    while True:
        soup_captcha = BeautifulSoup(driver.page_source, "lxml")
        if soup_captcha.find_all("div", class_="a-row a-text-center"):
            image_captcha = soup_captcha.find_all("div", class_="a-row a-text-center")
            form_captcha(driver, image_captcha, count)
        else:
            break
    return driver


def get_link_product_related(driver):
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
        time.sleep(2)  # Đợi một chút để trang tải
    main = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="dp-container"]'))
    )
    total_page = main.find_elements(By.XPATH, '//*[@id="sp_detail"]/div[1]/div[2]/span/span[1]/span[2]')
    _list_products = []
    for _ in range(1):
        list_products = driver.find_element(By.XPATH, '//*[@id="sp_detail"]/div[2]/div/div/div[2]/div/ol')
        products = list_products.find_elements(By.XPATH, './li')
        for product in products:
            url_product = product.find_element(By.XPATH, './div/a')
            _list_products.append(url_product.get_attribute("href"))
        button_previous = main.find_element(By.XPATH, '//*[@id="sp_detail"]/div[2]/div/div/div[3]/a')
        button_previous.click()
        time.sleep(5)
    driver.quit()
    return _list_products


datas = []


def process_image(items):
    global datas
    link_search = items["product"]
    count = items["count"]
    while True:
        if not (By.XPATH, '//*[@id="dp-container"]'):
            time.sleep(10)
        else:
            break
    print(count, ":", link_search)
    driver = get_link(link_search, count)
    soup = BeautifulSoup(driver.page_source, "lxml")
    main = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="dp-container"]'))
    )

    product_title = main.find_elements(By.XPATH, '//*[@id="productTitle"]')
    title = product_title[0].text
    print("title : ", product_title[0].text)

    if main.find_elements(By.XPATH, '//*[@id="acrCustomerReviewText"]'):
        product_ratings = main.find_elements(By.XPATH, '//*[@id="acrCustomerReviewText"]')
        rating = product_ratings[0].text
        print("rate : ", product_ratings[0].text)
    else:
        rating = "0 rating"
        print("rate : ", "No rating")
    product_prices = soup.find_all("span", class_="a-size-base a-color-price a-color-price")
    for product_price in product_prices:
        price = product_price.get_text(strip=True)

    description = []
    div_descriptions = soup.find_all("div", class_="a-expander-content a-expander-partial-collapse-content")
    for p_element in div_descriptions[1]:
        description.append(p_element.get_text(strip=True))
    print("description : ", description)

    large_image = main.find_element(By.XPATH, '//*[@id="main-image-container"]/ul')
    large_image.click()
    parent_div = large_image.find_element(By.XPATH, '//*[@id="ivThumbs"]/div[3]')
    child_divs = parent_div.find_elements(By.XPATH, './div')
    list_image = []
    if len(child_divs) == 1:
        time.sleep(1)
        image_x_paths = main.find_elements(By.XPATH, '//*[@id="ivLargeImage"]/img')
        for image_x_path in image_x_paths:
            list_image.append(image_x_path.get_attribute("src"))
    else:
        for child_div in range(len(child_divs)):
            image_child = main.find_element(By.XPATH, f'//*[@id="ivThumbs"]/div[3]/div[{child_div + 1}]')
            image_child.click()
            time.sleep(1)
            image_x_paths = main.find_elements(By.XPATH, '//*[@id="ivLargeImage"]/img')
            for image_x_path in image_x_paths:
                list_image.append(image_x_path.get_attribute("src"))
    match = re.search(r'%2Fdp%2F([A-Z0-9]+)', link_search)
    asin = match.group(1)
    print("asin : ", asin)
    link_amazon = f"https://www.amazon.com/dp/{asin}"

    row = [title, list_image, description, price, rating, asin]
    datas.append(row)
    driver.quit()


def worker(main_queue):
    while not main_queue.empty():
        items = main_queue.get()
        if items is None:
            break
        process_image(items)
        main_queue.task_done()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    link_search = config['setting']['link_search']
    driver = get_link(link_search, "0")

    list_product = get_link_product_related(driver)
    print("total link:", len(list_product))
    print(list_product)
    fifo_queue = queue.Queue()
    count = 0
    for product in list_product:
        count += 1
        items = {
            "product": product,
            "count": count
        }
        fifo_queue.put(items)
    threads = []

    for _ in range(5):
        thread = threading.Thread(target=worker, args=(fifo_queue,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    header = ['TITLE', 'IMAGE', 'DESCRIPTION', 'PRICING', 'RATING', 'ASIN']
    # Ghi dữ liệu vào tệp CSV
    with open('export_csv.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # Viết header
        writer.writerow(header)
        # Viết dữ liệu
        writer.writerows(datas)
