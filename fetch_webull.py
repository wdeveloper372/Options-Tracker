"""
fetch_webull.py
----------------
Responsible for authenticating with the Webull Sandbox API, 
retrieving your account identifiers, and fetching raw order history 
data to be saved into the database.
"""

import os
import importlib
from dotenv import load_dotenv
from webull.core.client import ApiClient
from webull.trade.trade_client import TradeClient

# Load local environment variables from the .env file
load_dotenv()

# Version patch for Webull SDK to prevent missing version attributes
_webull_core = importlib.import_module("webull")
if not hasattr(_webull_core, "__version__"):
    _webull_core.__version__ = "1.0.0"

def fetch_webull_trades():
    """
    Connects to the Webull API using secure keys, fetches the primary 
    account list, and queries the order history for that account.
    
    Returns:
        dict/list: The raw JSON order history data if successful, else None.
    """
    # Retrieve secure credentials from environment variables
    webull_api_key = os.getenv("WEBULL_API_KEY")
    webull_api_secret = os.getenv("WEBULL_API_SECRET")
    
    # Initialize the core API client and trading client
    api_client = ApiClient(webull_api_key, webull_api_secret, "us")
    trade_client = TradeClient(api_client)

    try:
        print("Connecting to Webull Sandbox to fetch accounts...")
        account_response = trade_client.account_v2.get_account_list()
        
        if account_response.status_code == 200:
            accounts = account_response.json()
            if not accounts:
                print("❌ No accounts found.")
                return None
                
            # Grab the primary account ID from the list
            target_account_id = accounts[0]["account_id"]
            print(f"✅ Found Account ID: {target_account_id}")
            
            print("Fetching order history for this account...")
            order_response = trade_client.order_v3.get_order_history(target_account_id)
            
            if order_response.status_code == 200:
                orders_data = order_response.json()
                print(f"🚀 SUCCESS! Retrieved order history.")
                return orders_data
            else:
                # Fixed string formatting error across lines
                print(f"❌ Failed to fetch orders: {order_response.status_code} - {order_response.text}")
                return None
                
        else:
            print(f"❌ Failed to fetch accounts: {account_response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Execution failed: {e}")
        return None