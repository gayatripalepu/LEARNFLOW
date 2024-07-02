import requests

EXCHANGE_RATE_API_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/"

def fetch_exchange_rate(base_currency, convert_to_currency):
    response = requests.get(EXCHANGE_RATE_API_URL + base_currency)
    if response.status_code != 200:
        raise Exception("Error fetching exchange rates. Please check the API URL and your API key.")
    
    exchange_data = response.json()
    if 'conversion_rates' not in exchange_data:
        raise Exception("Invalid response from API. Please check the API URL and your API key.")
    
    conversion_rates = exchange_data['conversion_rates']
    if convert_to_currency not in conversion_rates:
        raise Exception(f"Conversion rate for {convert_to_currency} not found.")
    
    return conversion_rates[convert_to_currency]

def perform_currency_conversion():
    print("Welcome to the Currency Conversion Tool!")

    try:
        amount_to_convert = float(input("Enter the amount: "))
        base_currency = input("Enter the base currency (e.g., USD, EUR): ").upper()
        target_currency = input("Enter the target currency (e.g., USD, EUR): ").upper()
        
        exchange_rate = fetch_exchange_rate(base_currency, target_currency)
        final_amount = amount_to_convert * exchange_rate
        
        print(f"{amount_to_convert} {base_currency} is equal to {final_amount:.2f} {target_currency}")
    
    except Exception as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    perform_currency_conversion()
