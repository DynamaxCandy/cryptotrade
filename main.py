from binance.client import Client
import config
import sqlite3
import time

client = Client(config.API_key, config.Secret_Key)

start = "1 Dec, 2017"
end = "12 FEB, 2021"

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("SELECT id, symbol FROM crypt")

rows = cursor.fetchall()
symbols = []
ids = {}

for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    ids[symbol] = row['id']

tickers = client.get_all_tickers()

for ticker in tickers:
    try:
        if ticker['symbol'] not in symbols:
            cursor.execute("INSERT OR IGNORE INTO crypt(symbol) VALUES (?)",
                           (ticker['symbol'],))

    except Exception as e:
        print(ticker['symbol'])
        print(e)

for symbol in symbols[1000:]:
    klineobj = client.get_historical_klines_generator(symbol, Client.KLINE_INTERVAL_1DAY, start, end)
    klines = list(klineobj)
    try:
        for kline in klines:
            crypt_id = ids[symbol]
            open_time = config.epoch2human(kline[0])
            open_price = kline[1]
            high = kline[2]
            low = kline[3]
            close_price = kline[4]
            volume = kline[5]
            close_time = config.epoch2human(kline[6])
            quote_asset_volume = kline[7]
            number_trades = kline[8]
            taker_buy_base = kline[9]
            taker_buy_quote = kline[10]
            print('Processing ' + symbol + " now...")

            cursor.execute("""
                            INSERT INTO crypt_price (crypt_id, open_time, open, high, low, close, volume, 
                            close_time, quote_asset_volume,number_trades, taker_buy_base, taker_buy_quote)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (crypt_id, open_time, open_price, high, low, close_price, volume, close_time, quote_asset_volume,
                              number_trades, taker_buy_base, taker_buy_quote))

    except Exception as e:
        print(symbol + ' seems having some problems...')
        print(e)

connection.commit()
