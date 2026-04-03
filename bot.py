import os
import time
import re
import base64
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SERVER_ID = os.getenv("SERVER_ID")

def run_bypass():
    print("[*] ЗАПУСК FEERHUS ENGINE v3.0 (CLOUDFLARE BYPASS)...")
    
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # Добавляем кучу аргументов, чтобы казаться "реальнее"
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

    try:
        driver = uc.Chrome(options=options, version_main=146)
        driver.set_page_load_timeout(60)
        wait = WebDriverWait(driver, 40)

        print("[*] ОТКРЫВАЮ СТРАНИЦУ ЛОГИНА...")
        driver.get("https://client.falixnodes.net/auth/login")
        
        # Даем Cloudflare 20 секунд на раздумья
        time.sleep(20)

        # ДЕБАГ: Делаем скриншот, чтобы понять, что видит бот
        driver.save_screenshot("debug_view.png")
        print("[!] СКРИНШОТ СТРАНИЦЫ СОХРАНЕН (Check Artifacts if failed)")

        print("[*] ИЩУ ПОЛЯ ВВОДА...")
        # Пробуем найти поле по ID или Name, Falix часто меняет их
        try:
            email_field = wait.until(EC.element_to_be_clickable((By.NAME, "user_detail")))
        except:
            print("[!] Поле 'user_detail' не найдено. Пробую альтернативный поиск...")
            email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text' or @type='email']")))

        email_field.send_keys(EMAIL)
        time.sleep(2)
        
        pass_field = driver.find_element(By.NAME, "password")
        pass_field.send_keys(PASSWORD + Keys.ENTER)
        
        print("[+] ДАННЫЕ ОТПРАВЛЕНЫ. ЖДУ ВХОДА...")
        time.sleep(15)

        # ПРОВЕРКА КОНСОЛИ
        driver.get(f"https://client.falixnodes.net/server/{SERVER_ID}")
        time.sleep(20)

        if "verify?t=" in driver.page_source:
            link = re.search(r'https://client\.falixnodes\.net/verify\?t=[\w\d]+', driver.page_source).group(0)
            print(f"[!!!] КАПЧА! ЖМУ: {link}")
            driver.get(link)
            time.sleep(10)
            print("[+] ВЕРИФИКАЦИЯ ПРОЙДЕНА.")
        else:
            print("[?] Все чисто, капчи нет.")

    except Exception as e:
        print(f"[!] КРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
        driver.save_screenshot("final_error.png")
    finally:
        print("[*] СЕССИЯ ЗАКРЫТА. СЛАВА СУСИКУ.")
        driver.quit()

if __name__ == "__main__":
    run_bypass()
