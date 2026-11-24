from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Iniciar el navegador
driver = webdriver.Chrome()

# 2. Navegar a una página
driver.get("https://www.google.com")

# 3. Esperar y localizar un elemento
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "q"))
)

# 4. Interactuar: escribir y enviar
search_box.send_keys("Selenium WebDriver")
search_box.send_keys("\n")  # Enter

# 5. Verificar el resultado
assert "selenium" in driver.title
print("Test OK:", driver.title)

# 6. Cerrar la sesión
driver.quit()   
