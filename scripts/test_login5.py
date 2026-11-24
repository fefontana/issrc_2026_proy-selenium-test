from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://localhost:5173"
EMAIL = "cliente@carmel.com"
PASSWORD_CORRECTA = "cliente123"
PASSWORD_INCORRECTA = "cliente999"


def get_driver():
    options = Options()

    # --- Banner de automatización ---
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    # --- Password Manager: 3 capas ---
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,  # ← el culpable del "cambiá tu contraseña"
        "reduce-security-for-testing": True,
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-features=PasswordLeakDetection")

    # --- Otros ---
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-notifications")

    return webdriver.Chrome(options=options)
    
    
    


def test_login_exitoso_credenciales_validas():
    """TC-01: Login con credenciales válidas → redirección a home con 'Hola, Cliente'."""
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "email").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD_CORRECTA)
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Salir')]"))
        )

        nav = driver.find_element(By.TAG_NAME, "nav")
        assert "Hola, Cliente" in nav.text
        assert driver.current_url == f"{BASE_URL}/"

    finally:
        driver.quit()


def test_login_fallido_contrasena_incorrecta():
    """TC-02: Login con contraseña incorrecta → mensaje 'Credenciales incorrectas'."""
    driver = get_driver()
    try:
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "email").send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD_INCORRECTA)
        driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(),'Credenciales incorrectas')]")
            )
        )

        error_el = driver.find_element(
            By.XPATH, "//*[contains(text(),'Credenciales incorrectas')]"
        )
        assert error_el.is_displayed()
        assert "/login" in driver.current_url

    finally:
        driver.quit()   
