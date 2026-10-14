# Options-Tracker

A Python project to track my options trading positions automatically instead of by hand.

**Status: In progress.** The pieces below work on their own and are not connected yet.

## What works so far
* `fetch_webull.py` connects to the Webull OpenAPI and retrieves account data.
* `options.py` connects to a MySQL database, creates a `trades` table, and inserts a record.
* `docker-compose.yml` runs a MySQL 8 container for the database.
* API keys and database credentials are loaded from a `.env` file, not stored in the code.

## Next steps
- [ ] Fetch options positions from Webull, not just account info
- [ ] Parse the response (ticker, option type, strike, expiration, quantity, cost)
- [ ] Expand the `trades` table and save real positions
- [ ] Prevent duplicate rows when the script reruns
- [ ] Combine the scripts into one `main.py`
- [ ] Add a volume so database data persists, and containerize the app

## Tech Stack
Python, Webull OpenAPI SDK, MySQL, Docker Compose

## Setup
1. Create a `.env` file with `WEBULL_API_KEY`, `WEBULL_API_SECRET`, `WEBULL_API_ID`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`.
2. Start the database: `docker compose up -d`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python fetch_webull.py` or `python options.py`
