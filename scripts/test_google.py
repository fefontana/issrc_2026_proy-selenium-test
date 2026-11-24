# test_google.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_search():
    driver = webdriver.Chrome()
    try:
        driver.get("https://www.google.com")
        box = driver.find_element(By.NAME, "q")
        box.send_keys("Selenium")
        box.send_keys("\n")

        # Esperar a que el título contenga "Selenium"
        WebDriverWait(driver, 10).until(EC.title_contains("Selenium"))

        assert "Selenium" in driver.title
    finally:
        driver.quit()   

# Fallo de ejecucion por problema de timing: el assert se ejecuta antes de que la página de 
# resultados termine de cargar. Google aún muestra el título "Google Search" porque la 
# navegación a los resultados no terminó.
#
# test_google.py (primer intento)
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#
#def test_search():
#    driver = webdriver.Chrome()
#    try:
#        driver.get("https://www.google.com")
#        box = driver.find_element(By.NAME, "q")
#        box.send_keys("Selenium")
#        box.send_keys("\n")
#        assert "Selenium" in driver.title
#    finally:
#        driver.quit()   
