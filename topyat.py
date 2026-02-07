import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
#options_chrome.add_argument('--headless')
driver = webdriver.Chrome(options=options)

filename = "topyat.txt"
path = os.path.join("dataset", filename)
with open(path, "w", encoding="utf-8") as f:

    for page in range(1, 11):
        url = f"https://www.kinopoisk.ru/lists/movies/top500/?page={page}/"
        driver.get(url)
        time.sleep(2) 

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "styles_root__dtojy"))
            )
        except:
            break
        
        films = driver.find_elements(By.CLASS_NAME, "styles_root__dtojy")
        if not films:
            break

        for film in films:
            a = film.find_element(By.TAG_NAME, 'a')
            f.write(a.get_attribute('href') + " ")
            print(a.get_attribute('href'))
            url_f = a.get_attribute('href') + "reviews/"

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url_f)
            time.sleep(3)

            f.write(driver.find_elements(By.CLASS_NAME, "breadcrumbs__item")[2].find_element(By.TAG_NAME, 'a').text + " ")
            for stat in ("all", "pos", "neg"):
                    f.write(driver.find_element(By.CLASS_NAME, "resp_type").find_element(By.CLASS_NAME, stat).find_element(By.TAG_NAME, 'b').text + " ")
            f.write("\n")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

driver.quit()