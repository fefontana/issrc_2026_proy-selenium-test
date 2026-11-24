from selenium import webdriver
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://localhost:5173"
EMAIL = "cliente@carmel.com"

# --- Caso 1: Login exitoso ---
print("=" * 60)
print("CASO 1: LOGIN EXITOSO")
print("=" * 60)

driver = webdriver.Chrome()
driver.get(f"{BASE_URL}/login")
driver.find_element(By.ID, "email").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys("cliente123")
driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
time.sleep(5)

print(f"URL: {driver.current_url}")
print(f"Título: {driver.title}")
print(f"\n--- HTML del <body> (primeros 3000 chars) ---")
print(driver.find_element(By.TAG_NAME, "body").text[:3000])

# Buscar elementos que podrían indicar "logueado"
print("\n--- Búsqueda de elementos clave ---")
for sel, desc in [
    ("header", "header"),
    ("nav", "nav"),
    ("[class*='dashboard']", "class*='dashboard'"),
    ("[class*='welcome']", "class*='welcome'"),
    ("[class*='user']", "class*='user'"),
    ("[class*='logout']", "class*='logout'"),
    ("[class*='salir']", "class*='salir'"),
]:
    try:
        el = driver.find_element(By.CSS_SELECTOR, sel)
        print(f"  ✅ {desc}: {el.text[:100]}")
    except:
        print(f"  ❌ {desc}: no encontrado")

driver.quit()

# --- Caso 2: Login fallido ---
print("\n" + "=" * 60)
print("CASO 2: LOGIN FALLIDO (contraseña incorrecta)")
print("=" * 60)

driver = webdriver.Chrome()
driver.get(f"{BASE_URL}/login")
driver.find_element(By.ID, "email").send_keys(EMAIL)
driver.find_element(By.ID, "password").send_keys("cliente999")
driver.find_element(By.CSS_SELECTOR, "button.btn-primary").click()
time.sleep(5)

print(f"URL: {driver.current_url}")
print(f"Título: {driver.title}")
print(f"\n--- Texto visible en la página ---")
print(driver.find_element(By.TAG_NAME, "body").text[:2000])

# Buscar elementos de error
print("\n--- Búsqueda de elementos de error ---")
for sel, desc in [
    ("[class*='error']", "class*='error'"),
    ("[class*='alert']", "class*='alert'"),
    ("[class*='toast']", "class*='toast'"),
    ("[class*='invalid']", "class*='invalid'"),
    ("[class*='danger']", "class*='danger'"),
    ("[role='alert']", "role='alert'"),
    ("p", "p (todos)"),
]:
    try:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        for el in els[:3]:
            if el.text.strip():
                print(f"  ✅ {desc}: \"{el.text[:100]}\"")
    except:
        pass

driver.quit()   
