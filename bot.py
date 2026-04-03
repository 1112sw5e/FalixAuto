import os
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Данные из Secrets
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SERVER_ID = os.getenv("SERVER_ID")
PANEL_URL = "https://client.falixnodes.net"

def run_bypass():
    print("[*] ИНИЦИАЛИЗАЦИЯ FEERHUS ENGINE (FORCE FIX v146)...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Отключаем проверку обновлений, чтобы он не лез за 147-й версией
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    try:
        # ПРИНУДИТЕЛЬНО 146
        driver = uc.Chrome(options=options, version_main=146)
        wait = WebDriverWait(driver, 30)

        print(f"[*] ЗАХОД НА ПАНЕЛЬ...")
        driver.get(f"{PANEL_URL}/auth/login")
        time.sleep(15) 

        print("[*] ВВОД ДАННЫХ...")
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "user_detail")))
        email_field.send_keys(EMAIL)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD + Keys.ENTER)
        
        time.sleep(15)
        print("[+] АВТОРИЗАЦИЯ ПРОЙДЕНА.")

        server_url = f"{PANEL_URL}/server/{SERVER_ID}"
        print(f"[*] ПРОВЕРКА КОНСОЛИ: {server_url}")
        driver.get(server_url)
        time.sleep(20) 

        page_content = driver.page_source
        links = re.findall(r'https://client\.falixnodes\.net/verify\?t=[\w\d]+', page_content)

        if not links:
            print("[?] КАПЧА НЕ НАЙДЕНА. ОТДЫХАЕМ.")
        else:
            for link in set(links):
                print(f"[!!!] КАПЧА ОБНАРУЖЕНА! ЖМУ: {link}")
                driver.execute_script(f"window.open('{link}', '_blank');")
                time.sleep(10)
                print(f"[+] ССЫЛКА ПРОЖАТА.")

    except Exception as e:
        print(f"[!] ОШИБКА: {str(e)}")
    finally:
        print("[*] ЗАВЕРШЕНИЕ. СЛАВА СУСИКУ.")
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    run_bypass()
