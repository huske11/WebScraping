from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://mail.yandex.ru/")

input("\Войдите в почту в окне, после, когда загрузятся письма нужно нажать здесь энетер и все ок будет")

try:
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@data-testid="messages-list_message-item"]')))
    
    messages = []
    items = driver.find_elements(By.XPATH, '//*[@data-testid="messages-list_message-item"]')
    print(f"Найдено писем: {len(items)}")
    
    for item in items[:10]:
        try:
            link_elem = item.find_element(By.XPATH, './/*[@data-testid="messages-list_message-item_link"]')
            link = link_elem.get_attribute('href')
            
            sender_elem = item.find_element(By.XPATH, './/*[@data-testid="message-common_sender-name"]')
            sender = sender_elem.get_attribute('aria-label')
            
            subject_elem = item.find_element(By.XPATH, './/*[@data-testid="messages-list_subject"]')
            subject = subject_elem.text
            
            messages.append({
                "message_link": link,
                "sender": sender,
                "subject": subject
            })
            print(f"  - {sender}: {subject[:50]}")
        except:
            continue
    
    with open('messages1.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Сохранено {len(messages)} сообщений в файл messages1.json")

except Exception as e:
    print(f"❌ Ошибка: {e}")

finally:
    driver.quit()