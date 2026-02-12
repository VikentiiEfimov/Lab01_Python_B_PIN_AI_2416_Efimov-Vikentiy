import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from stschyot import get_films

os.makedirs("dataset/good", exist_ok=True)
os.makedirs("dataset/bad", exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)

films = get_films()

good_counter = 0
bad_counter = 0
MAX_REVIEWS = 999
per_options = [10, 25, 50, 75, 100, 200]
wait = WebDriverWait(driver, 5)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('parser.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def save_review(title, text, film_name, status, pn_counter, counter):
    filename = f"{pn_counter:04d}.txt"
    folder = "good" if status == "good" else "bad"
    path = os.path.join("dataset", folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(film_name + "\n\n")
        if title != "": f.write(title + "\n\n")
        f.write(text)
    logging.info(f"Сохранён {counter+1}-й {status} отзыв: {filename} по {film_name}")

for film_id, film_name, pos_rew, neg_rew in films:
    for status in ("good", "bad"):
        target = int(int(pos_rew) * 0.084) + 1 if status == "good" else int(neg_rew)
        perpage = next((x for x in per_options if x >= target), 200)
        counter = 0

        while counter < target:
            url = f"https://www.kinopoisk.ru/film/{film_id}/reviews/ord/rating/status/{status}/perpage/{perpage}/page/1/"
            driver.get(url)

            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "reviewItem"))
                )
            except:
                break

            reviews = driver.find_elements(By.CLASS_NAME, "reviewItem")

            for review in reviews:
                if counter >= target:
                    break

                title = review.find_element(By.CLASS_NAME, "sub_title").text.strip()
                text_element = review.find_element(By.CLASS_NAME, "brand_words")
                text = text_element.text.strip()

                if status == "good":
                    save_review(title, text, film_name, status, good_counter, counter)
                    if good_counter == MAX_REVIEWS:
                        counter = target +1
                        break
                    else: good_counter += 1

                else:
                    save_review(title, text, film_name, status, bad_counter, counter)
                    if bad_counter == MAX_REVIEWS:
                        counter = target +1
                        break
                    else: bad_counter += 1

                counter += 1

driver.quit()
logging.info(f"Готово! Положительных: {good_counter+1}, отрицательных: {bad_counter+1}.")