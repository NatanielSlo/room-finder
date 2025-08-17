from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.airbnb.pl/s/warsaw/homes?flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2025-09-01&monthly_length=3&monthly_end_date=2025-12-01&date_picker_type=calendar&checkin=2025-09-24&checkout=2025-09-26&adults=2&refinement_paths%5B%5D=%2Fhomes&source=structured_search_input_header&search_type=search_query")

time.sleep(5)

cards = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='card-container']")[:3]

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
        for span in spans:
            if "zł" in span.text:
                prices = re.findall(r'(\d+)\s*zł', span.text)
                if prices:
                    price = min(int(p) for p in prices)
                    price = f"{price} zł"
                break
    except:
        price = None


    results.append({
        "link": link,
        "name": name,
        "price": price
    })

for i, offer in enumerate(results, start=1):
    print(f"Oferta {i}:")
    print(f"  Nazwa: {offer['name']}")
    print(f"  Cena: {offer['price']}")
    print(f"  Link: {offer['link']}")
    print("-" * 50)


driver.quit()
