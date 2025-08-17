from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


def scrape_booking(city,check_in,check_out,no_adults,no_rooms):
    # --- Ustawienia Selenium ---
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # odkomentuj, jeśli chcesz uruchamiać w tle
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    # --- URL do scrapowania ---
    # check_in = "2025-08-17"
    # check_out = "2025-08-20"
    # no_rooms = "1"
    # no_adults = "2"
    # city = "berlin"

    url = f"https://www.booking.com/searchresults.html?ss={city}&checkin={check_in}&checkout={check_out}&group_adults={no_adults}&no_rooms={no_rooms}&group_children=0"
    driver.get(url)

    # --- Czekaj, aż wyniki się załadują ---
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="property-card"]')))

    # --- Pobranie pierwszych 10 ofert ---
    offers = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')[:10]

    data = []
    for offer in offers:
        try:
            name = offer.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text
        except:
            name = "Brak nazwy"

        try:
            price = offer.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text
        except:
            price = "Brak ceny"

        try:
            link = offer.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        except:
            link = "Brak linku"

        data.append({
            "name": name,
            "price": price,
            "link": link
        })

    # --- Zapis do CSV (nadpisuje plik za każdym razem) ---
    with open("booking_com_results.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "price", "link"])
        writer.writeheader()
        for offer in data:
            writer.writerow(offer)

    print("Dane zapisane do booking_com_results.csv")

    # --- Wyświetlenie wyników ---
    # for i, offer in enumerate(data, start=1):
    #     print(f"Oferta {i}:")
    #     print(f"  Nazwa: {offer['name']}")
    #     print(f"  Cena: {offer['price']}")
    #     print(f"  Link: {offer['link']}")
    #     print("-" * 50)

    driver.quit()
