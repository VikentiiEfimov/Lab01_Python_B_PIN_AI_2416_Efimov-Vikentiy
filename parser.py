import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.makedirs("dataset/good", exist_ok=True)
os.makedirs("dataset/bad", exist_ok=True)
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

films = [
    (535341, "1+1"),
    (435, "Зеленая миля"),
    (448, "Форрест Гамп"),
    (329, "Список Шиндлера"),
    (1143242, "Джентльмены"),
    (462682, "Волк с Уолл-Стрит")
]

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

for film_id, film_name in films:
    if good_counter >= MAX_REVIEWS and bad_counter >= MAX_REVIEWS:
        print("Достигнут лимит в 1000 отзывов для каждого типа.")
        break

    for status in ("good", "bad"):
        if (status == "good" and good_counter >= MAX_REVIEWS) or (status == "bad" and bad_counter >= MAX_REVIEWS):
            continue

        page = 1
        while True:
            url = f"https://www.kinopoisk.ru/film/{film_id}/reviews/ord/date/status/{status}/perpage/10/page/{page}/"
            driver.get(url)
            time.sleep(2) 

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "reviewItem"))
                )
            except:
                break

            reviews = driver.find_elements(By.CLASS_NAME, "reviewItem")
            if not reviews:
                break

            for review in reviews:
                if (status == "good" and good_counter >= MAX_REVIEWS) or (status == "bad" and bad_counter >= MAX_REVIEWS):
                    break

                try:
                    read_more = review.find_element(By.CLASS_NAME, "reviewItem_readmore")
                    read_more.click()
                    time.sleep(1)
                except:
                    pass
                try:
                    text_element = review.find_element(By.CLASS_NAME, "brand_words")
                    text = text_element.text.strip()
                except:
                    continue

                if not text:
                    continue

                if status == "good":
                    save_review(text, film_name, status, good_counter)
                    good_counter += 1
                else:
                    save_review(text, film_name, status, bad_counter)
                    bad_counter += 1

            if (status == "good" and good_counter >= MAX_REVIEWS) or (status == "bad" and bad_counter >= MAX_REVIEWS):
                break

            try:
                next_btn = driver.find_element(By.CLASS_NAME, "paginator__page-next")
                if not next_btn.is_enabled():
                    break
                page += 1
            except:
                break

            time.sleep(2) 

driver.quit()
print(f"Готово! Положительных отзывов: {good_counter}, отрицательных: {bad_counter}.")