from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
EMAIL = "cliente@carmel.com"
PASSWORD_CORRECTA = "cliente123"
PASSWORD_INCORRECTA = "cliente999"


def test_login_exitoso_credenciales_validas():
    """TC-01: Login con credenciales válidas → redirección a home con 'Hola, Cliente'."""
    driver = webdriver.Chrome()
    try:
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "email").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD_CORRECTA)
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

        # Esperar a que aparezca el link "Salir" (indica sesión activa)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Salir')]"))
        )

        # Verificar que el saludo muestra el nombre
        nav = driver.find_element(By.TAG_NAME, "nav")
        assert "Hola, Cliente" in nav.text

        # Verificar que la URL cambió a home
        assert driver.current_url == f"{BASE_URL}/"

    finally:
        driver.quit()


def test_login_fallido_contrasena_incorrecta():
    """TC-02: Login con contraseña incorrecta → mensaje 'Credenciales incorrectas'."""
    driver = webdriver.Chrome()
    try:
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "email").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD_INCORRECTA)
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

        # Esperar a que aparezca el texto de error
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Credenciales incorrectas')]")
            )
        )

        # Verificar que el mensaje es visible
        error_el = driver.find_element(
            By.XPATH, "//*[contains(text(),'Credenciales incorrectas')]"
        )
        assert error_el.is_displayed()

        # Verificar que NO se redirigió (sigue en /login)
        assert "/login" in driver.current_url

    finally:
        driver.quit()   
