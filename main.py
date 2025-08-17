from airbnb_scraper import scrape_airbnb
from booking_scraper import scrape_booking

# --- Parametry, które chcesz przekazać ---
city = "berlin"
check_in = "2025-08-17"
check_out = "2025-08-20"
no_rooms = "1"
no_adults = "2"

# --- Uruchamianie scraperów ---
scrape_airbnb(city, check_in, check_out,no_adults)
#scrape_booking(city, check_in, check_out,no_adults,no_rooms)