from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import re

# --- Конфигурация ---
USERNAME = ""
PASSWORD = ""
DOMAIN_GROUP_NAME = ""
LOGIN_URL = ""

# --- Генерация безопасного имени файла ---
safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', DOMAIN_GROUP_NAME)
filename = f"fail_{safe_name}.txt"

# --- Вспомогательная задержка ---
def wait_real(short=False):
    time.sleep(random.uniform(0.9, 1.4 if short else 2.2))

# --- Настройка драйвера ---
def setup_driver():
    options = Options()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver = setup_driver()

try:
    # --- Авторизация ---
    driver.get(LOGIN_URL)
    wait_real()
    driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(USERNAME)
    wait_real()
    driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(PASSWORD)
    wait_real()
    driver.find_element(By.XPATH, '//button[contains(@class, "ant-btn") and .//span[text()="Login"]]').click()
    time.sleep(5)

    # --- Открыть раздел Domains ---
    driver.find_element(By.XPATH, '//span[contains(@class, "ant-menu-title-content") and text()="Domains"]').click()
    wait_real()

    # --- Перейти в нужную группу ---
    driver.find_element(By.XPATH, f'//a[contains(text(), "{DOMAIN_GROUP_NAME}")]').click()
    time.sleep(5)

    with open(filename, "w", encoding="utf-8") as fail_file:
        while True:
            time.sleep(3)

            # --- Сбор данных ---
            rows = driver.find_elements(By.CSS_SELECTOR, "tr.ant-table-row")
            for row in rows:
                try:
                    health = row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
                    if "Attention" in health:
                        domain = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a").text.strip()
                        print(f"⚠️ Attention: {domain}")
                        fail_file.write(domain + "\n")
                except:
                    continue

            # --- Проверка текущей страницы ---
            current_page = int(driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-item-active").get_attribute("title"))

            # --- Проверка: есть ли "Next Page" ---
            next_li = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next")
            disabled = next_li.get_attribute("aria-disabled")
            if disabled == "true":
                print("✅ Последняя страница достигнута.")
                break

            try:
                # --- Убрать мешающее окно опроса PostHog ---
                driver.execute_script("""
                    let el = document.querySelector('div[class^="PostHogSurvey-"]');
                    if (el) {
                        el.style.display = "none";
                    }
                """)

                # --- Клик по кнопке следующей страницы ---
                next_btn = next_li.find_element(By.TAG_NAME, "button")
                next_btn.click()
                print(f"➡️ Переход на страницу {current_page + 1}")

                # --- Ожидание обновления страницы ---
                for _ in range(20):  # максимум 5 секунд
                    time.sleep(0.25)
                    new_page = int(driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-item-active").get_attribute("title"))
                    if new_page != current_page:
                        break
                else:
                    raise Exception("⚠️ Страница не обновилась после клика")

                wait_real()

            except Exception as e:
                print("❌ Ошибка при переходе:", e)
                break

except Exception as e:
    print("❌ Общая ошибка:", e)

finally:
    print("🔚 Скрипт завершён.")
    driver.quit()
