import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stschyot import get_films

os.makedirs("dataset/good", exist_ok=True)
os.makedirs("dataset/bad", exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

films = get_films()

good_counter = 0
bad_counter = 0
MAX_REVIEWS = 1000

def save_review(text, film_name, status, counter):
    filename = f"{counter:04d}.txt"
    folder = "good" if status == "good" else "bad"
    path = os.path.join("dataset", folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(film_name + "\n\n")
        f.write(text)
    print(f"Сохранён {status} отзыв: {filename}")

for film_id, film_name, pos_rew, neg_rew in films:
    for status in ("good", "bad"):
        page = 1 
        counter = 0
        while True:
            url = f"https://www.kinopoisk.ru/film/{film_id}/reviews/ord/date/status/{status}/perpage/10/page/{page}/"
            driver.get(url)           

            reviews = driver.find_elements(By.CLASS_NAME, "reviewItem")
            for review in reviews:
                #if (((status == "good" and good_counter >= MAX_REVIEWS) or (status == "good" and counter >= int(int(pos_rew) * 0.084) + 1)) or ((status == "bad" and bad_counter >= MAX_REVIEWS) or(status == "bad" and counter >= int(neg_rew)))):
                if ((status == "good" and counter >= int(int(pos_rew) * 0.084) + 1) or (status == "bad" and counter >= int(neg_rew))):
                    break
                text_element = review.find_element(By.CLASS_NAME, "brand_words")
                text = text_element.text.strip()
                if status == "good":
                    save_review(text, film_name, status, good_counter)
                    good_counter += 1
                else:
                    save_review(text, film_name, status, bad_counter)
                    bad_counter += 1
                counter +=1
            
            if ((status == "good" and counter >= int(int(pos_rew) * 0.084) + 1) or (status == "bad" and counter >= int(neg_rew))):
                    break
            page += 1
 