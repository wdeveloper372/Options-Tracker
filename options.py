"""
options.py
-----------
The core data pipeline script. It connects to your local MySQL database,
ensures the options trading table exists, fetches raw order history via 
the Webull module, filters for filled orders, extracts key contract 
details (legs, strike prices, expiration), and safely inserts them 
into the database.
"""

import os
import mysql.connector
from dotenv import load_dotenv
from fetch_webull import fetch_webull_trades

# Load secure credentials and configuration from the local .env file
load_dotenv()

# Connect to your MySQL database 
# (Note: Use "localhost" when running locally, or your Docker container service name when containerized)
mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = mydb.cursor()

# 1. Create a clean table specifically for your options trades if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS options_trades (
        id INT AUTO_INCREMENT PRIMARY KEY,
        symbol VARCHAR(50),
        option_type VARCHAR(20),
        strike_price DECIMAL(10,2),
        expire_date DATE,
        side VARCHAR(50),
        filled_price DECIMAL(10,2),
        filled_quantity INT,
        status VARCHAR(50)
    )
""")

# 2. Fetch the raw order data from your Webull pipeline module
orders_data = fetch_webull_trades()

if orders_data:
    print("\nProcessing and inserting option trades into MySQL...")
    
    # Loop through the outer list of trade orders
    for combo in orders_data:
        # Each combo item contains an 'orders' list
        sub_orders = combo.get("orders", [])
        
        for order in sub_orders:
            status = order.get("status")
            
            # Filter to only log successfully filled trades
            if status == "FILLED":
                symbol = order.get("symbol")
                side = order.get("position_intent")  # e.g., 'BUY_TO_OPEN'
                filled_price = order.get("filled_price")
                quantity = order.get("filled_quantity")
                
                # Dig into the nested 'legs' array for specific option contract details
                legs = order.get("legs", [])
                if legs:
                    leg = legs[0]
                    option_type = leg.get("option_type")        # 'PUT' or 'CALL'
                    strike_price = leg.get("strike_price")      # e.g., 320.00
                    expire_date = leg.get("option_expire_date") # e.g., '2026-10-21'
                else:
                    option_type, strike_price, expire_date = None, None, None
                
                # 3. Format as a clean parameterized tuple to prevent SQL injection and syntax errors
                sql = """
                    INSERT INTO options_trades 
                    (symbol, option_type, strike_price, expire_date, side, filled_price, filled_quantity, status) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                trade_tuple = (
                    symbol, 
                    option_type, 
                    strike_price, 
                    expire_date, 
                    side, 
                    filled_price, 
                    quantity, 
                    status
                )
                
                # Execute the safe query insertion
                cursor.execute(sql, trade_tuple)
                print(f"✅ Logged: {symbol} Exp: {expire_date} Strike: ${strike_price} {option_type} ({side}) at ${filled_price}")
                
    # Commit all successful insertions to persist them in the database
    mydb.commit()
    print("\n🚀 All options trades successfully saved to your database!")

else:
    print("No order data returned.")

# Cleanly close database connections
cursor.close()
mydb.close()