import os
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === ПОЛУЧЕНИЕ ДАННЫХ ИЗ SECRETS ===
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SERVER_ID = os.getenv("SERVER_ID")
PANEL_URL = "https://client.falixnodes.net"

def run_bypass():
    print("[*] ИНИЦИАЛИЗАЦИЯ FEERHUS ENGINE...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless') # Обязательно для GitHub
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    
    # Маскировка под обычного юзера
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        # 1. АВТОРИЗАЦИЯ
        print(f"[*] ЗАХОД НА {PANEL_URL}/auth/login")
        driver.get(f"{PANEL_URL}/auth/login")
        time.sleep(7) # Даем Cloudflare прогрузиться

        print("[*] ВВОД ДАННЫХ...")
        email_field = wait.until(EC.presence_of_element_status((By.NAME, "user_detail")))
        email_field.send_keys(EMAIL)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD + Keys.ENTER)
        
        time.sleep(10)
        print("[+] АВТОРИЗАЦИЯ УСПЕШНА (надеюсь).")

        # 2. ПЕРЕХОД В КОНСОЛЬ СЕРВЕРА
        server_url = f"{PANEL_URL}/server/{SERVER_ID}"
        print(f"[*] ПЕРЕХОД К СЕРВЕРУ: {server_url}")
        driver.get(server_url)
        time.sleep(15) # Ждем, пока подгрузятся логи консоли

        # 3. ПАРСИНГ ЛОГОВ
        page_content = driver.page_source
        # Ищем паттерн ссылки верификации
        links = re.findall(r'https://client\.falixnodes\.net/verify\?t=[\w\d]+', page_content)

        if not links:
            print("[?] КАПЧА НЕ НАЙДЕНА. СЕРВЕР В ПОРЯДКЕ.")
        else:
            for link in set(links):
                print(f"[!!!] ОБНАРУЖЕНА КАПЧА: {link}")
                # Открываем в новой вкладке для подтверждения
                driver.execute_script(f"window.open('{link}', '_blank');")
                time.sleep(10)
                print(f"[+] ССЫЛКА ПРОКЛИКАНА: {link}")

    except Exception as e:
        print(f"[!] ОШИБКА В РАБОТЕ: {str(e)}")
        # Делаем скриншот ошибки для отладки (сохранится в артефактах GitHub, если настроишь)
        driver.save_screenshot("error_debug.png")
    
    finally:
        print("[*] ЗАВЕРШЕНИЕ СЕССИИ. СЛАВА СУСИКУ.")
        driver.quit()

if __name__ == "__main__":
    if not EMAIL or not PASSWORD or not SERVER_ID:
        print("[-] ОШИБКА: Заполни SECRETS на GitHub!")
    else:
        run_bypass()
