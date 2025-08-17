from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import csv

def scrape_airbnb(city,check_in,check_out,no_adults):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(f"https://www.airbnb.pl/s/{city}/homes?flexible_trip_lengths%5B%5D=one_week&monthly_start_date={check_in}&monthly_length=3&monthly_end_date={check_out}&date_picker_type=calendar&checkin={check_in}&checkout={check_out}&adults={no_adults}&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=search_query")

    time.sleep(5)

    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='card-container']")[:10]  # teraz 10 pierwszych

    results = []

    for card in cards:
        try:
            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except:
            link = None
        try:
            name = card.find_element(By.CSS_SELECTOR, "span[data-testid='listing-card-name']").text
        except:
            name = None
        try:
            price = None
            spans = card.find_elements(By.TAG_NAME, "span")
            for i, span in enumerate(spans):
                if "zł" in span.text:
                    if "Pokaż kalkulację ceny" in span.text:
                        # Pobierz wszystkie spany po tym elemencie
                        remaining_text = " ".join(s.text for s in spans[i+1:])
                        price = remaining_text.strip()
                    else:
                        price = span.text.strip()
                    break
        except:
            
            price = None

        results.append({
            
            "name": name,
            "price": price,
            "link": link
        })

    # Zapis do CSV (nadpisuje plik za każdym razem)
    with open("airbnb_results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "price","link"])
        writer.writeheader()
        for offer in results:
            writer.writerow(offer)

    print("Dane zapisane do airbnb_results.csv")

    driver.quit()
