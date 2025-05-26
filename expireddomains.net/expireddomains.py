from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# === Переменные ===
пер_логин = "kingsss"
пер_пароль = "Koko2006"

# === Настройка браузера ===
print("🚀 Запускаем браузер...")
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # окно браузера открывается на весь экран
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# === Шаг 1: Переход на страницу логина ===
print("🌐 Переход на страницу входа...")
driver.get("https://www.expireddomains.net/login/")
time.sleep(2)

# === Шаг 2: Вводим логин ===
print("📝 Ввод логина...")
username_input = driver.find_element(By.ID, "inputLogin")
username_input.clear()
username_input.send_keys(пер_логин)

# === Шаг 3: Вводим пароль ===
print("🔒 Ввод пароля...")
password_input = driver.find_element(By.ID, "inputPassword")
password_input.clear()
password_input.send_keys(пер_пароль)

# === Шаг 4: Нажимаем кнопку входа ===
print("➡️ Нажимаем кнопку входа...")
login_button = driver.find_element(By.XPATH, "//form//button[@type='submit']")
login_button.click()

# === Шаг 5: Ожидаем 2FA ===
print("\n⏳ Жду, пока ты пройдёшь 2FA вручную.")
print("👉 После прохождения нажми Enter в консоли, чтобы продолжить.")
input("⌨️  Введи 2FA в браузере и нажми Enter здесь: ")

# === Шаг 6: Проверка входа и переход к данным ===
print("✅ Авторизация завершена.")
print("📂 Переход к списку удалённых доменов...")

driver.get("https://www.expireddomains.net/domain-name-database/")  # пример раздела
time.sleep(3)