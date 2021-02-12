import sqlite3
import config

connection = sqlite3.connect(config.DB_FILE)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypt (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE
    )
""")

cursor.execute("""
    DROP TABLE crypt_price
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypt_price (
        id INTEGER PRIMARY KEY, 
        crypt_id INTEGER,
        open_time NOT NULL,
        open NOT NULL, 
        high NOT NULL, 
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        close_time NOT NULL,
        quote_asset_volume NOT NULL,
        number_trades NOT NULL,
        taker_buy_base NOT NULL,
        taker_buy_quote NOT NULL,
        FOREIGN KEY (crypt_id) REFERENCES crypt (id)
    )
""")

connection.commit()
