# 🗺️ Google Maps Scraper

A modular and extensible scraper built with Python and Selenium for extracting business data from Google Maps.  
Designed with clean architecture principles, SOLID design, and separation of concerns.

---

## 🚀 What It Does

This scraper automates Google Maps searches to extract business information such as:

- Business name
- Rating and number of reviews
- Main reviews
- Address and phone number
- Category and opening hours
- Website and booking links
- Main image
- Additional attributes

Results are stored in a CSV file.

---

## 🧱 Architecture Overview

- `BaseScraper`: Abstract base class that defines the scraping contract.
- `SeleniumDriver`: Encapsulates all Selenium-related actions and stealth setup.
- `GoogleMapsScraper`: Concrete implementation for Google Maps scraping.
- `ResultsStore`: In-memory result buffer, shared across components.
- `CSVWriter`: Repository that handles CSV persistence.

---

## ⚙️ Requirements

- Python 3.10+
- Google Chrome (latest version)
- **Chromedriver** (must match your Chrome version)
- Selenium

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔧 Downloading Chromedriver

To run the scraper, you need to download Chromedriver and place it in your project directory or somewhere in your system PATH.

    1.- Check your Chrome version at chrome://settings/help.

    2.- Go to the official Chromedriver page.

    3.- Download the version that matches your Chrome.

    4.- Extract the chromedriver binary and:

        - Place it in your project root directory (recommended), or

        - Add its path to your system’s PATH environment variable.

If placed in the project root, the scraper will automatically detect and launch it.

## 🧪 Running the Scraper

```bash
python run_scraper.py --query "physiotherapist in javea, spain"
```
Or, specifying a language other than English: 

python run_scraper.py --query "fisioterapeuta en javea, españa" --lang "es"

