from playwright.sync_api import sync_playwright, Playwright
import sqlite3
import os

print(os.path.abspath("coinmarketcap.db"))

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://coinmarketcap.com/")

    conn = sqlite3.connect("coinmarketcap.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coinmarketcap (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            change_24h TEXT,
            market_cap TEXT
        )    
    """)

    rows = page.locator("table.cmc-table tbody tr").all()
    for row in rows:
        name_locator = row.locator("p.coin-item-name")
        if name_locator.count() == 0:
            continue
        name  = name_locator.inner_text()
        price = row.locator("div.sc-631098c-0").inner_text() if row.locator("div.sc-631098c-0").count() > 0 else "N/A"
        changes = row.locator("span.sc-d5c03ba0-0").all()
        change_24h = changes[1].inner_text() if len(changes) >   1 else "N/A"
        market_cap = row.locator("span.jfwGHx").inner_text() if row.locator("span.jfwGHx").count() > 0 else "N/A"

        #print(f"{name} | {price} | {change_24h} | {market_cap}")
        cursor.execute("""
            INSERT OR IGNORE INTO coinmarketcap (name, price, change_24h, market_cap)
            VALUES (?, ?, ?, ?)
        """, (name, price, change_24h, market_cap))
    conn.commit()
    conn.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
