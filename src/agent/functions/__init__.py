from .functions import (
    google_search_and_scrape,
    get_current_cryptocurrency_price_usd,
    get_current_stock_price,
)


# Note: register functions you want to be callable by the bot here
functions = {
    "google_search_and_scrape": google_search_and_scrape,
    "get_current_cryptocurrency_price_usd": get_current_cryptocurrency_price_usd,
    "get_current_stock_price": get_current_stock_price,
}
