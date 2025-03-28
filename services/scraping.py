import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver(download_dir: str):
    try:
        options = Options()
        options.add_argument("--headless=new") 
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        service = Service(executable_path="/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)
        
        logging.info("Driver do Selenium configurado com sucesso.")
        return driver
    except Exception as e:
        logging.error(f"Erro ao configurar o driver do Selenium: {e}")
        raise

def download_xml(driver, url: str, chave_acesso: str, download_dir: str) -> str:
    try:
        driver.get(url)
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Digite a CHAVE DE ACESSO']"))
        )
        input_field.send_keys(chave_acesso)
    
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, "//img[@alt='Permitir pop-ups']"))
            )
        except Exception:
            logging.info("Popup 'Permitir pop-ups' não detectado ou já removido.")
   
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Buscar DANFE/XML')]"))
        )
        driver.execute_script("arguments[0].click();", search_button)
        
        try:
            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.XPATH, "//img[@alt='Permitir pop-ups']"))
            )
        except Exception:
            logging.info("Popup 'Permitir pop-ups' não detectado ou já removido.")
        
        download_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-contrast-blue') and contains(text(), 'Baixar XML')]"))
        )
        driver.execute_script("arguments[0].click();", download_button)
        
        time.sleep(10)
        
        file_path = os.path.join(download_dir, f"{chave_acesso}.xml")
        if os.path.exists(file_path):
            logging.info(f"XML baixado com sucesso: {file_path}")
            return file_path
        else:
            logging.error("Arquivo XML não encontrado após o download.")
            raise FileNotFoundError("Arquivo XML não encontrado.")
    except Exception as e:
        logging.error(f"Erro ao baixar XML: {e}")
        raise