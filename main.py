# import time
# import configparser
# import queue
# import csv
# import threading
# import os
# import requests
# from PIL import Image
# import easyocr
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# def image_to_text_easyocr(image_path):
#     reader = easyocr.Reader(['en'])
#     result = reader.readtext(image_path)
#     text = ' '.join([entry[1] for entry in result])
#     return text
#
#
# def get_driver():
#     chrome_options = Options()
#     chrome_options.add_experimental_option("detach", True)
#     ChromeDriverManager().install()
#     driver = webdriver.Chrome(options=chrome_options)
#     screen_width = driver.execute_script("return window.screen.availWidth;")
#     screen_height = driver.execute_script("return window.screen.availHeight;")
#     driver.set_window_size(screen_width, screen_height)
#     driver.get(link_search)
#
#
# def get_link_product_related(link_search):
#     chrome_options = Options()
#     chrome_options.add_experimental_option("detach", True)
#     ChromeDriverManager().install()
#     driver = webdriver.Chrome(options=chrome_options)
#     screen_width = driver.execute_script("return window.screen.availWidth;")
#     screen_height = driver.execute_script("return window.screen.availHeight;")
#     driver.set_window_size(screen_width, screen_height)
#     driver.get(link_search)
#     image_captcha = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
#     get_link_image = image_captcha.get_attribute("src")
#     response = requests.get(get_link_image, stream=True)
#     folder_ing_captcha = "image captcha"
#     if not os.path.exists(folder_ing_captcha):
#         os.mkdir(folder_ing_captcha)
#     file_name = f"1.jpg"
#     path_file_name = os.path.join(folder_ing_captcha, file_name)
#     with open(path_file_name, "wb") as f:
#         f.write(response.content)
#     if path_file_name:
#         image = Image.open(path_file_name)
#         result_text = image_to_text_easyocr(image)
#     input_element = driver.find_element(By.XPATH, '//*[@id="captchacharacters"]')
#     input_element.send_keys(result_text)
#     button_continute = driver.find_element(By.XPATH,
#                                            '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
#     button_continute.click()
#     for _ in range(3):
#         driver.execute_script("window.scrollBy(0, document.body.scrollHeight/5);")
#         time.sleep(2)  # Đợi một chút để trang tải
#
#     main = WebDriverWait(driver, 300).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="dp-container"]'))
#     )
#     total_page = main.find_elements(By.XPATH, '//*[@id="sp_detail"]/div[1]/div[2]/span/span[1]/span[2]')
#     _list_products = []
#     for page in range(int(total_page[0].text)):
#         list_products = driver.find_element(By.XPATH, '//*[@id="sp_detail"]/div[2]/div/div/div[2]/div/ol')
#         products = list_products.find_elements(By.XPATH, './li')
#         for product in products:
#             url_product = product.find_element(By.XPATH, './div/a')
#             _list_products.append(url_product.get_attribute("href"))
#         button_previous = main.find_element(By.XPATH, '//*[@id="sp_detail"]/div[2]/div/div/div[3]/a')
#         button_previous.click()
#         time.sleep(2)
#     driver.quit()
#     return _list_products
#
#
# def process_image(items):
#     chrome_options = Options()
#     chrome_options.add_experimental_option("detach", True)
#     ChromeDriverManager().install()
#     driver = webdriver.Chrome(options=chrome_options)
#     screen_width = driver.execute_script("return window.screen.availWidth;")
#     screen_height = driver.execute_script("return window.screen.availHeight;")
#     driver.set_window_size(screen_width, screen_height)
#     driver.get(items)
#     image_captcha = driver.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
#     get_link_image = image_captcha.get_attribute("src")
#     response = requests.get(get_link_image, stream=True)
#     folder_ing_captcha = "image captcha"
#     if not os.path.exists(folder_ing_captcha):
#         os.mkdir(folder_ing_captcha)
#     file_name = f"1.jpg"
#     path_file_name = os.path.join(folder_ing_captcha, file_name)
#     with open(path_file_name, "wb") as f:
#         f.write(response.content)
#     if path_file_name:
#         image = Image.open(path_file_name)
#         result_text = image_to_text_easyocr(image)
#     input_element = driver.find_element(By.XPATH, '//*[@id="captchacharacters"]')
#     input_element.send_keys(result_text)
#     button_continute = driver.find_element(By.XPATH,
#                                            '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
#     button_continute.click()
#
#     main = WebDriverWait(driver, 300).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="dp-container"]'))
#     )
#     product_title = main.find_elements(By.XPATH, '//*[@id="productTitle"]')
#     title = product_title[0].text
#     print("title : ", product_title[0].text)
#
#     try:
#         product_ratings = main.find_elements(By.XPATH, '//*[@id="acrCustomerReviewText"]')
#         rating = product_ratings[0].text
#         print("rate : ", product_ratings[0].text)
#     except:
#         print("No rating")
#     if not product_ratings[0].text:
#         rating = "0 rating"
#
#     product_price = main.find_elements(By.XPATH, '//*[@id="price"]')
#     price = product_price[0].text
#     print("price : ", product_price[0].text)
#
#     try:
#         read_more = main.find_element(By.XPATH, '//*[@id="bookDescription_feature_div"]/div/div[2]/a/span')
#         read_more.click()
#     except:
#         print("No read more")
#     product_description = main.find_elements(By.XPATH, '//*[@id="bookDescription_feature_div"]/div/div[1]')
#     description = product_description[0].text
#     print("description : ", product_description[0].text)
#
#     large_image = main.find_element(By.XPATH, '//*[@id="main-image-container"]/ul')
#     large_image.click()
#     parent_div = large_image.find_element(By.XPATH, '//*[@id="ivThumbs"]/div[3]')
#     child_divs = parent_div.find_elements(By.XPATH, './div')
#     list_image = []
#     if len(child_divs) == 1:
#         time.sleep(1)
#         image_x_paths = main.find_elements(By.XPATH, '//*[@id="ivLargeImage"]/img')
#         for image_x_path in image_x_paths:
#             list_image.append(image_x_path.get_attribute("src"))
#     else:
#         for child_div in range(len(child_divs)):
#             image_child = main.find_element(By.XPATH, f'//*[@id="ivThumbs"]/div[3]/div[{child_div + 1}]')
#             image_child.click()
#             time.sleep(1)
#             image_x_paths = main.find_elements(By.XPATH, '//*[@id="ivLargeImage"]/img')
#             for image_x_path in image_x_paths:
#                 list_image.append(image_x_path.get_attribute("src"))
#     row = [title, list_image, description, price, rating]
#     driver.quit()
#
#
# def worker(main_queue):
#     while not main_queue.empty():
#         items = main_queue.get()
#         if items is None:
#             break
#         process_image(items)
#         main_queue.task_done()
#
#
# if __name__ == '__main__':
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#
#     link_search = config['setting']['link_search']
#     list_product = get_link_product_related(link_search)
#     # fifo_queue = queue.Queue()
#     # for product in list_product:
#     #     fifo_queue.put(product)
#     # threads = []
#     # for _ in range(4):
#     #     thread = threading.Thread(target=worker, args=(fifo_queue,))
#     #     threads.append(thread)
#     # for thread in threads:
#     #     thread.start()
#     # for thread in threads:
#     #     thread.join()
#     # data = []
#     # header = ['TITLE', 'IMAGE', 'DESCRIPTION', 'PRICING', 'RATING']
#     # data.append(row)
#     # # Ghi dữ liệu vào tệp CSV
#     # with open('export_csv.csv', 'w', encoding='utf-8-sig', newline='') as f:
#     #     writer = csv.writer(f)
#     #     # Viết header
#     #     writer.writerow(header)
#     #     # Viết dữ liệu
#     #     writer.writerows(data)
#     while True:
#         if input("Enter q to exit") == "q":
#             break
