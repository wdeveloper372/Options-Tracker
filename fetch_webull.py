import os
from dotenv import load_dotenv
from webull.core.client import ApiClient
from webull.trade.trade_client import TradeClient
import importlib

load_dotenv()
_webull_core = importlib.import_module("webull")
if not hasattr(_webull_core, "__version__"):
    _webull_core.__version__ = "1.0.0"

# --- DIAGNOSTIC CHECK ---
print("--- ENVIRONMENT VARIABLE CHECK ---")
print(f"API Key Found: {os.getenv('WEBULL_API_KEY') is not None}")
print(f"API Secret Found: {os.getenv('WEBULL_API_SECRET') is not None}")
print(f"API ID Found: {os.getenv('WEBULL_API_ID') is not None}")
print("----------------------------------")


webull_api_key = os.getenv("WEBULL_API_KEY")
webull_api_secret = os.getenv("WEBULL_API_SECRET")
webull_api_id = os.getenv("WEBULL_API_ID")


api_client = ApiClient(webull_api_key, webull_api_secret, "us")

trade_client = TradeClient(api_client)

try:
    print("Connecting to official Webull OpenAPI Sandbox...")
    
    # Request the active account list structure linked to your keys
    response = trade_client.account_v2.get_account_list()
    
    if response.status_code == 200:
        print("\n🚀 SUCCESS! RAW WEBULL DATA BLUEPRINT:")
        print("---------------------------------")
        print(response.json())
        print("---------------------------------")
    else:
        print(f"❌ Webull Server Error: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Execution failed: {e}")