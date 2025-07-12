# El País Opinion Scraper with BrowserStack Integration

This project scrapes the first five opinion articles from the Spanish news website [El País](https://elpais.com/opinion/), extracts the article titles and snippets, downloads cover images, translates titles from Spanish to English, and performs simple text analysis on the translated titles. 

The scraping is performed using Selenium WebDriver, and the tests run remotely on multiple browsers and devices via [BrowserStack](https://www.browserstack.com/).

---

## Features

- Visits the "Opinion" section on El País and scrapes the first five articles.
- Extracts and prints article titles and content snippets.
- Downloads and saves cover images locally.
- Translates article titles to English using Google Translate API.
- Analyzes translated titles to find frequently repeated words.
- Runs scraping sessions sequentially on BrowserStack across multiple browsers/devices:
  - Windows Chrome
  - Mac Safari
  - Windows Edge
  - Google Pixel 7 (Android)
  - iPhone 14 (iOS)

---

## Prerequisites

- Python 3.8+
- Googletrans package (`googletrans==4.0.0-rc1`)
- Selenium (`selenium==4.10.0`)
- Requests package
- BrowserStack account with valid credentials

---

## Installation

1. Clone the repository:
    - git clone https://github.com/JanviSaluja/BrowserStack-Round-2.git
    - cd src
2. Create and actiate a Python virtual enviornment
    - python -m venv venv
    - On Windows: venv\Scripts\activate
3. Install dependencies:
    - pip install -r requirements.txt

## Configuration

- Before running the program, update the code with your BrowserStack credentials in the script.
- Set the BS_USERNAME and BS_ACCESS_KEY enviornment variables with your credentials.

## Usage

1. Run the script:
    - python main.py
2. The program will run sequentially on all the configured browsers and devices, printing output logs and saving images under the images/ directory.



