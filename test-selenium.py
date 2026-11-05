from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome()

try:
    driver.get("http://127.0.0.1:8000")

    campo = driver.find_element(By.ID, "nombre")
    campo.send_keys("Abdiel")

    boton = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    boton.click()

    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element(
            (By.ID, "resultado"),
            "Hola, Abdiel!",
        )
    )

    resultado = driver.find_element(By.ID, "resultado").text
    assert resultado == "Hola, Abdiel!", resultado

    print("Prueba correcta: el saludo funciona.")

finally:
    driver.quit()
