import random
import time
import undetected_chromedriver as uc
# from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


targetUrl = "https://cosmos.bluesoft.com.br/categorias/saude/produtos"
urlComosBlueSoft = targetUrl + "?page=1"

options = uc.ChromeOptions()
browser = uc.Chrome(use_subprocess=True, options=options)
browser.get(urlComosBlueSoft)

time.sleep(10)

wait = WebDriverWait(browser, 10)
products_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-list-item")))

paginate_count = browser.find_element(By.CSS_SELECTOR, "div.pagination > ul.pagination > li.active > a").text
pagination_items = browser.find_elements(By.CSS_SELECTOR, "div.pagination > ul.pagination > li")
total_pages = len(pagination_items) - 2

all_results = []

for product in products_list:
  try:
    # Pegar título, imagem, NCM e GTIN
    title_element = product.find_element(By.CSS_SELECTOR, "h5.description > a")
    img_element = product.find_element(By.CSS_SELECTOR, "div.col-md-3.picture a img")
    ncm_element = product.find_element(By.CSS_SELECTOR, "span.ncm a")
    gtin_element = product.find_element(By.CSS_SELECTOR, "span.barcode a")


    # Extrair dados
    title = title_element.text
    img_url = img_element.get_attribute("src")
    ncm = ncm_element.text
    gtin = gtin_element.text

    # Criar dicionário para armazenar as informações do produto
    obj_result = {
        'title': title,
        'image': img_url,
        'ncm': ncm,
        'gtin': gtin,
    }

    all_results.append(obj_result)

    # print(all_results)
  except Exception as e:
    print(f"Erro ao pegar as informações: {e}")

json_file_path = "produtos.json"
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(all_results, json_file, ensure_ascii=False, indent=2)

browser.quit()