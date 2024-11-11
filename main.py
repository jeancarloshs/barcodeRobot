import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

categoria = "bebidas"
categoriaObjResult = categoria.replace("-", " ")
categoriaObjResult = categoriaObjResult.title()
# categoriaObjResult = categoriaObjResult.replace("E", "e")
targetUrl = f"https://cosmos.bluesoft.com.br/categorias/{categoria}/produtos"
urlComosBlueSoft = targetUrl + "?page=1"

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
browser = uc.Chrome(use_subprocess=True, options=options)
browser.get(urlComosBlueSoft)

wait = WebDriverWait(browser, 10)

all_results = []
total_products = 0

while True:
    try:
        # Pega a lista de produtos na página atual
        products_list = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-list-item")))
        
        for product in products_list:
            try:
                # time.sleep(1)

                # Pegar título, imagem, NCM e GTIN
                title_element = product.find_element(By.CSS_SELECTOR, "div.col-md-12.infos > h5.description > a")
                img_element = product.find_element(By.CSS_SELECTOR, "div.col-md-3.picture a img.list-item-thumbnail")
                ncm_element = product.find_elements(By.CSS_SELECTOR, "div.col-md-12.infos > p.text > span.ncm a")
                gtin_element = product.find_element(By.CSS_SELECTOR, "div.col-md-12.infos > p.text > span.barcode a")

                # time.sleep(1)
                # Extrair dados
                title = title_element.text
                img_url = img_element.get_attribute("src")
                ncm = ncm_element[0].text if ncm_element else ""
                gtin = gtin_element.text

                # time.sleep(1)
                # Criar dicionário para armazenar as informações do produto
                obj_result = {
                    'title': title,
                    'image': img_url,
                    'categoria': categoriaObjResult,
                    'ncm': ncm,
                    'gtin': gtin,
                }

                all_results.append(obj_result)
                total_products += 1
                print(f"{obj_result}")

            except Exception as e:
                print(f"Erro ao Extrair Dados: {e}")

        # Role a página antes de tentar clicar no botão "Próxima"
        browser.execute_script("window.scrollBy(0, 3500);")  # Rola 3500 pixels para baixo
        time.sleep(2)  # Espera 2 segundos para o carregamento dos elementos

        try:
          # Localiza o link da "Próxima"
          li_next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.next a[rel='next']")))
          # next_page_element = li_next_page.find_element(By.XPATH, "..")  # Acessa o <li> que contém o <a>


          # Verifica se o link "Próxima" está desabilitado
          # if 'disabled' in li_next_page.find_element(By.XPATH, "..").get_attribute('class'):
          #     print("Última página alcançada.")
          #     break  # Sai do loop se for a última página
          
          # if "disabled" in next_page_element.get_attribute("class"):
          #     print("Última página alcançada.")
          #     break  # Sai do loop se for a última página
          # else:
          #     # Se o link "Próxima" estiver habilitado, clica nele
          #     li_next_page.click()
          #     time.sleep(random.uniform(5, 7))

          # Se o link "Próxima" estiver habilitado, clica nele
          li_next_page.click()

          # Aguarda um tempo para carregar a próxima página
          time.sleep(random.uniform(3, 5))  # Atraso aleatório para não sobrecarregar o site
        except Exception as e:
          print(f"Erro ao tentar navegar para a próxima página: {e}")
          break

    except Exception as e:
        print(f"Erro ao processar a navegação ou carregar produtos: {e}")
        break

json_file_path = f"produtos-{categoria}.json"
try:
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(all_results, json_file, ensure_ascii=False, indent=2)
    print(f"Total de produtos coletados: {total_products}")
except Exception as e:
    print(f"Erro ao salvar os dados no arquivo JSON: {e}")


browser.quit()
