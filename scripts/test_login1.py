from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
EMAIL = "cliente@carmel.com"
PASSWORD_CORRECTA = "cliente123"
PASSWORD_INCORRECTA = "cliente999"


def test_login_exitoso_credenciales_validas():
    """TC-01: Login con credenciales válidas → redirección al dashboard."""
    driver = webdriver.Chrome()
    try:
        driver.get(f"{BASE_URL}/login")

        # Completar formulario
        email_box = driver.find_element(By.ID, "email")
        pass_box = driver.find_element(By.ID, "password")
        email_box.send_keys(EMAIL)
        pass_box.send_keys(PASSWORD_CORRECTA)

        # Enviar
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

        # Esperar a que el dashboard cargue
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dashboard-header"))
        )
        
        # Asegurar que el dashboard está visible
        assert driver.find_element(By.ID, "dashboard-header").is_displayed()

    finally:
        driver.quit()


def test_login_fallido_contrasena_incorrecta():
    """TC-02: Login con contraseña incorrecta → mensaje de error."""
    driver = webdriver.Chrome()
    try:
        driver.get(f"{BASE_URL}/login")

        # Completar formulario con contraseña errónea
        email_box = driver.find_element(By.ID, "email")
        pass_box = driver.find_element(By.ID, "password")
        email_box.send_keys(EMAIL)
        pass_box.send_keys(PASSWORD_INCORRECTA)

        # Enviar
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

        # Esperar a que aparezca el mensaje de error
        error_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".error-message"))
        )
        
        # Verificar que el mensaje contiene "inválid" (cubre "inválido"/"inválidas")
        assert "inválid" in error_msg.text.lower()

        # Verificar que NO se redirigió al dashboard
        try:
            driver.find_element(By.ID, "dashboard-header")
            assert False, "No debería estar en el dashboard"
        except Exception:
            pass

    finally:
        driver.quit()   
