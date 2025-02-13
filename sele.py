from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import time
import os

load_dotenv()

atd_id = input("Digite o atendimento: ")

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get(f"https://grendene.agidesk.com/br/painel/atendimento/{atd_id}")

input_element = driver.find_element(By.ID, "username")
input_element.send_keys(os.getenv("agidesk_login"))

time.sleep(1000)

driver.quit()