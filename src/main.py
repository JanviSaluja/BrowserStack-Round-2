from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os
import requests
from googletrans import Translator
import re
from collections import Counter

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Could not download image {url}. Reason: {e}")

def translate_and_analyze_titles(titles):
    translator = Translator()
    translated_titles = []

    print("\nTranslating titles to English...")
    for title in titles:
        try:
            translated = translator.translate(title, src='es', dest='en')
            translated_titles.append(translated.text)
            print(f"Original: {title}")
            print(f"Translated: {translated.text}\n")
        except Exception as e:
            print(f"Translation failed for '{title}': {e}")
            translated_titles.append(title)

    # Analyze repeated words in translated titles
    print("Analyzing repeated words in translated titles...")
    all_words = []
    for t in translated_titles:
        words = re.findall(r'\b\w+\b', t.lower())
        all_words.extend(words)

    word_counts = Counter(all_words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    if repeated_words:
        print("Words repeated more than twice:")
        for word, count in repeated_words.items():
            print(f"'{word}': {count} times")
    else:
        print("No words repeated more than twice.")

    return translated_titles

def scrape_opinion_articles():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://elpais.com/")
        time.sleep(3)

        # Accept cookies if present
        try:
            accept_cookies = driver.find_element(By.XPATH, "//button[contains(., 'Aceptar')]")
            accept_cookies.click()
            print("Accepted cookies")
            time.sleep(2)
        except:
            print("No cookies banner found")

        # Navigate directly to the Opinion section
        driver.get("https://elpais.com/opinion/")
        print("Navigated directly to 'Opinión' section")
        time.sleep(3)

        # Collect first 5 unique article URLs
        article_links = driver.find_elements(By.CSS_SELECTOR, "article a")
        article_urls = []
        for link in article_links:
            href = link.get_attribute("href")
            if href and href not in article_urls:
                article_urls.append(href)
            if len(article_urls) >= 5:
                break
        print(f"Collected {len(article_urls)} article URLs")

        collected_titles = []

        for idx, href in enumerate(article_urls):
            print(f"\nVisiting article {idx+1}: {href}")
            driver.get(href)
            time.sleep(2)

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
                collected_titles.append(title)
                print(f"Title (Spanish): {title}")
            except:
                title = "No title found"
                collected_titles.append(title)
                print("No title found")

            try:
                paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
                snippet = " ".join([p.text for p in paragraphs[:3]])
                print(f"Snippet: {snippet[:200]}...")
            except:
                snippet = "No content found"
                print("No content snippet found")

            try:
                img = driver.find_element(By.CSS_SELECTOR, "figure img")
                img_url = img.get_attribute("src")
                if img_url:
                    if not os.path.exists("images"):
                        os.makedirs("images")
                    img_filename = os.path.join("images", f"article_{idx+1}.jpg")
                    download_image(img_url, img_filename)
                else:
                    print("No cover image found.")
            except:
                print("No cover image found.")

        translate_and_analyze_titles(collected_titles)

    finally:
        driver.quit()
        print("Scraping completed. Browser closed.")

if __name__ == "__main__":
    print("El País Opinion scraper starting...")
    scrape_opinion_articles()
