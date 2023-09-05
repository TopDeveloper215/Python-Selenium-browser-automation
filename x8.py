import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_random_link_with_js(driver, target_url):
    try:
        script = """
            var links = document.querySelectorAll("a[href^='%s'][href*='https://']");
            if (links.length > 0) {
                links[Math.floor(Math.random() * links.length)].click();
            }
        """ % target_url
        driver.execute_script(script)
        print('1')
    except Exception as e:
        print("12", str(e))
        
with open("keyword.txt", "r") as keyword_file:
    keywords = [keyword.strip() for keyword in keyword_file.readlines()]
print("11")

with open("url.txt", "r") as url_file:
    target_url = url_file.readline().strip()

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')  
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(20)

with driver: 
    for keyword in keywords:
        search_query = f"https://www.google.com/search?q={keyword}"
        driver.get(search_query)
        try:
            consent_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#L2AGLb > div"))
            )
            consent_button.click()
            driver.refresh()
        except:
            pass
        print("111")
        WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.tF2Cxc")))
        
        search_results = driver.find_elements(By.TAG_NAME, 'a')
        print(search_results[0].get_attribute("href"))
        matching_url = ""
        found_target_url = False
        for result in search_results:
            href = result.get_attribute("href")
            if href and target_url in href:
                found_target_url = True
                matching_url = href
                break
       
        if found_target_url:
            driver.get(matching_url)
            try:
                scrollable_element = driver.find_element(By.TAG_NAME, "body")
                scroll_height = scrollable_element.size["height"]
                driver.execute_script(f"arguments[0].scrollTop = {scroll_height};", scrollable_element)
                print("100")
            except Exception as e:
                print("200", str(e))
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            click_random_link_with_js(driver, target_url)
            
            time.sleep(20) 
