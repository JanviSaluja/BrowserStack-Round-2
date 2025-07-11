# El País Opinion Articles Scraper

## Overview

This project contains a Python-based web scraper that extracts articles from the Opinion section of *El País*, a leading Spanish news outlet. The scraper uses Selenium for automated browser interaction, `googletrans` for translating article titles from Spanish to English, and performs basic textual analysis to identify frequently repeated words across translated article titles.

---

## Features

- Automatically navigates to the *El País* Opinion section.
- Extracts the first five articles, printing their Spanish titles and content snippets.
- Downloads cover images associated with each article, if available.
- Translates article titles into English using Google Translate API via the `googletrans` library.
- Analyzes translated titles to detect any words repeated more than twice, providing simple frequency counts.
- Runs in headless mode using Selenium Chrome WebDriver for efficient automated scraping.

---

## Requirements

- Python 3.7+
- Google Chrome browser installed (compatible version with ChromeDriver)
- ChromeDriver executable available in PATH or same directory as the script
- Python packages:
  - `selenium`
  - `requests`
  - `googletrans==4.0.0-rc1`

You can install the required Python packages using:

```bash
pip install -r requirements.txt
