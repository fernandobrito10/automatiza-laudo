from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import os

load_dotenv()

atd_id = input("Digite o atendimento: ")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://grendene.agidesk.com/login")
    
    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(os.getenv("agidesk_login"))
    wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(os.getenv("agidesk_senha") + Keys.ENTER)
    
    wait.until(EC.url_contains("/painel"))
    
    driver.get(f"https://grendene.agidesk.com/br/painel/atendimento/{atd_id}")
    
    elemento_contato = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h4[id^='app-taskcontact-']"))
    )
    id_pessoa_agidesk = elemento_contato.get_attribute('data-id')
    print(f"ID Agidesk: {id_pessoa_agidesk}")
    

    driver.get(f"https://grendene.agidesk.com/br/configuracoes/contato/{id_pessoa_agidesk}")
    time.sleep(2)
    wait.until(EC.url_contains(f"/br/configuracoes/contato/{id_pessoa_agidesk}"))
    time.sleep(2)
    id_ad = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
    ).get_attribute("value")
    time.sleep(2)
    nome = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="contacts-title"]/div'))
    ).text
    time.sleep(2)
    centro_de_custo = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="contacts-main-form-fields-8-field-1"]/div/div[1]'))
    ).text
    
    print(f"""
    Username: {id_ad}
    Nome: {nome}
    Centro de Custo: {centro_de_custo}
    """)

except Exception as e:
    print(f"Erro: {str(e)}")
