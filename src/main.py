from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import time
import os
import requests
from googletrans import Translator
import re
from collections import Counter

BS_USERNAME = 'janvisaluja_FpS5Jj'
BS_ACCESS_KEY = 'NNHxq5YfB18A8e6x5UYg'
BS_HUB_URL = f'https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub.browserstack.com/wd/hub'

def get_options(tag):
    if tag == "Chrome":
        options = ChromeOptions()
        options.set_capability('browserVersion', 'latest')
        options.set_capability('bstack:options', {
            "os": "Windows",
            "osVersion": "10",
            "sessionName": "El Pais Chrome Win"
        })
    elif tag == "Safari":
        options = SafariOptions()
        options.set_capability('browserVersion', 'latest')
        options.set_capability('bstack:options', {
            "os": "OS X",
            "osVersion": "Ventura",
            "sessionName": "El Pais Safari Mac"
        })
    elif tag == "Edge":
        options = EdgeOptions()
        options.set_capability('browserVersion', 'latest')
        options.set_capability('bstack:options', {
            "os": "Windows",
            "osVersion": "11",
            "sessionName": "El Pais Edge Win"
        })
    elif tag == "Pixel":
        options = ChromeOptions()
        options.set_capability('bstack:options', {
            "deviceName": "Google Pixel 7",
            "osVersion": "13.0",
            "realMobile": "true",
            "sessionName": "El Pais Pixel"
        })
    elif tag == "iPhone":
        options = SafariOptions()
        options.set_capability('bstack:options', {
            "deviceName": "iPhone 14",
            "osVersion": "16",
            "realMobile": "true",
            "sessionName": "El Pais iPhone"
        })
    else:
        options = ChromeOptions()
    return options

def download_image(url, filename, tag):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"[{tag}] ✔ Image saved as {filename}")
    except Exception as e:
        print(f"[{tag}] ✖ Could not download image {url}. Reason: {e}")

def translate_and_analyze_titles(titles, tag):
    translator = Translator()
    translated_titles = []

    print(f"[{tag}] Translating titles to English...")
    for title in titles:
        try:
            translated = translator.translate(title, src='es', dest='en')
            translated_titles.append(translated.text)
            print(f"[{tag}] Original: {title}")
            print(f"[{tag}] Translated: {translated.text}\n")
        except Exception as e:
            print(f"[{tag}] Translation failed for '{title}': {e}")
            translated_titles.append(title)

    all_words = []
    for t in translated_titles:
        words = re.findall(r'\b\w+\b', t.lower())
        all_words.extend(words)

    word_counts = Counter(all_words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    if repeated_words:
        print(f"[{tag}] Words repeated more than twice:")
        for word, count in repeated_words.items():
            print(f"[{tag}] '{word}': {count} times")
    else:
        print(f"[{tag}] No words repeated more than twice.")

def scrape_opinion_articles_on_browserstack(tag):
    options = get_options(tag)

    try:
        driver = Remote(command_executor=BS_HUB_URL, options=options)
        print(f"\n=== [{tag}] Session started: {driver.session_id} ===")
        collected_titles = []

        driver.get("https://elpais.com/")
        print(f"[{tag}] Loaded homepage")
        time.sleep(3)

        try:
            accept_cookies = driver.find_element(By.XPATH, "//button[contains(., 'Aceptar')]")
            accept_cookies.click()
            print(f"[{tag}] Accepted cookies")
            time.sleep(2)
        except:
            print(f"[{tag}] No cookie banner")

        driver.get("https://elpais.com/opinion/")
        print(f"[{tag}] Opened opinion section")
        time.sleep(3)

        article_links = driver.find_elements(By.CSS_SELECTOR, "article a")
        article_urls = []
        for link in article_links:
            href = link.get_attribute("href")
            if href and href not in article_urls:
                article_urls.append(href)
            if len(article_urls) >= 5:
                break
        print(f"[{tag}] Collected {len(article_urls)} article URLs")

        for idx, href in enumerate(article_urls):
            print(f"[{tag}] Visiting article {idx+1}: {href}")
            driver.get(href)
            time.sleep(2)

            try:
                title = driver.find_element(By.TAG_NAME, "h1").text
                collected_titles.append(title)
                print(f"[{tag}] Title: {title}")
            except:
                print(f"[{tag}] No title found")

            try:
                paragraphs = driver.find_elements(By.CSS_SELECTOR, "p")
                snippet = " ".join([p.text for p in paragraphs[:3]])
                print(f"[{tag}] Snippet: {snippet[:200]}...")
            except:
                print(f"[{tag}] No snippet found")

            try:
                img = driver.find_element(By.CSS_SELECTOR, "figure img")
                img_url = img.get_attribute("src")
                if img_url:
                    img_filename = os.path.join("images", f"{tag}_article_{idx+1}.jpg")
                    download_image(img_url, img_filename, tag)
                else:
                    print(f"[{tag}] No image found")
            except:
                print(f"[{tag}] No image found")

        translate_and_analyze_titles(collected_titles, tag)

    except Exception as e:
        print(f"[{tag}] TOP LEVEL ERROR: {e}")

    finally:
        try:
            driver.quit()
            print(f"[{tag}] Closed session.")
        except:
            print(f"[{tag}] Could not close driver properly.")

if __name__ == "__main__":
    print("=== Running El País Opinion scraper on BrowserStack across multiple browsers/devices sequentially ===")
    tags = ["Chrome", "Safari", "Edge", "Pixel", "iPhone"]
    for tag in tags:
        scrape_opinion_articles_on_browserstack(tag)
    print("\n=== All sessions completed ===")
