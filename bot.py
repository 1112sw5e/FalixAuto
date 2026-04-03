import os
import time
import re
import subprocess
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

def get_chrome_version():
    """Определяет версию Chrome на сервере GitHub"""
    try:
        output = subprocess.check_output(['google-chrome', '--version']).decode('utf-8')
        version = re.search(r'(\d+)', output).group(1)
        return int(version)
    except Exception as e:
        print(f"[!] Не удалось определить версию Chrome: {e}")
        return None

def run_bypass():
    print("[*] ИНИЦИАЛИЗАЦИЯ FEERHUS ENGINE...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    # Исправление конфликта версий драйвера
    chrome_ver = get_chrome_version()
    print(f"[*] ОБНАРУЖЕНА ВЕРСИЯ CHROME: {chrome_ver}")

    try:
        # Запуск драйвера с принудительным указанием версии
        driver = uc.Chrome(options=options, version_main=chrome_ver)
        wait = WebDriverWait(driver, 30)

        # 1. АВТОРИЗАЦИЯ
        print(f"[*] ЗАХОД НА {PANEL_URL}/auth/login")
        driver.get(f"{PANEL_URL}/auth/login")
        time.sleep(10) # Даем Cloudflare прогрузиться

        print("[*] ВВОД ДАННЫХ...")
        # Ищем поле ввода по имени (name="user_detail")
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "user_detail")))
        email_field.send_keys(EMAIL)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD + Keys.ENTER)
        
        time.sleep(12)
        print("[+] АВТОРИЗАЦИЯ ПРОЙДЕНА.")

        # 2. ПЕРЕХОД В КОНСОЛЬ СЕРВЕРА
        server_url = f"{PANEL_URL}/server/{SERVER_ID}"
        print(f"[*] ПЕРЕХОД К СЕРВЕРУ: {server_url}")
        driver.get(server_url)
        time.sleep(15) 

        # 3. ПАРСИНГ ЛОГОВ И ПОИСК ССЫЛКИ
        page_content = driver.page_source
        links = re.findall(r'https://client\.falixnodes\.net/verify\?t=[\w\d]+', page_content)

        if not links:
            print("[?] КАПЧА НЕ НАЙДЕНА. СЕРВЕР В ПОРЯДКЕ.")
        else:
            for link in set(links):
                print(f"[!!!] ОБНАРУЖЕНА КАПЧА: {link}")
                driver.execute_script(f"window.open('{link}', '_blank');")
                time.sleep(10)
                print(f"[+] ССЫЛКА ПОДТВЕРЖДЕНА: {link}")

    except Exception as e:
        print(f"[!] ОШИБКА: {str(e)}")
        # Если есть ошибка, сохраняем скриншот для отладки
        try:
            driver.save_screenshot("debug_screen.png")
            print("[*] Скриншот ошибки сохранен как debug_screen.png")
        except:
            pass
    
    finally:
        print("[*] ЗАВЕРШЕНИЕ СЕССИИ. СЛАВА СУСИКУ.")
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    if not EMAIL or not PASSWORD or not SERVER_ID:
        print("[-] ОШИБКА: Проверь GitHub Secrets!")
    else:
        run_bypass()
