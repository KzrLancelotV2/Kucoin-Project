import api
import json
import time
import os

client = api.config_client()

def fetch_symbols():
    symbols_data = client.get_symbols()
    symbols_json = json.dumps(symbols_data)
    with open('symbols.json', 'w') as f:
        f.write(symbols_json)
    return symbols_data

def add_kline_data(crypto_data, coin, klines):
    if coin not in crypto_data:
        crypto_data[coin] = []
    for entry in klines:
        crypto_data[coin].append({
            'start_time': entry[0],
            'opening_price': entry[1],
            'closing_price': entry[2],
            'highest_price': entry[3],
            'lowest_price': entry[4],
            'trans_amount': entry[5],
            'trans_volume': entry[6]
        })

def fetch_kline_data_for_symbols(symbols_data):  
    crypto_data = {} 
    for symbol_data in symbols_data:
        symbol = symbol_data['symbol']
        klines = client.get_kline_data(symbol, '1hour',
                                       int(time.time() - 30*24*60*60),
                                       int(time.time()))

        if klines:
            print(f"Processing data for {symbol}")
            add_kline_data(crypto_data, symbol, klines)
        else:
            print(f"No trading data available for the past month for {symbol}")
    
    return crypto_data

#only keep data for last 30 days
def remove_older_entries(crypto_data, symbol):
    while len(crypto_data[symbol]) > (30 * 24) + 1:
        crypto_data[symbol].pop(0)
        


def update_crypto_data(symbols_data, crypto_data, last_n_hours):
    for symbol_data in symbols_data:
        symbol = symbol_data['symbol']
        klines = client.get_kline_data(symbol, '1hour',
                                       int(time.time() - last_n_hours*60*60),
                                       int(time.time()))
        if klines:
            print(f"Updating data for {symbol}")
            add_kline_data(crypto_data, symbol, klines)
            remove_older_entries(crypto_data, symbol)
            print(len(crypto_data[symbol]))
            
        else:
            print(f"No trading data available for the past month for {symbol}")
    
    return crypto_data
        

def get_last_modified_time(file_path):
    try:
        # Get the last modification time
        modification_time = os.path.getmtime(file_path)
        return modification_time
    except OSError as e:
        print(f"Error accessing file: {e}")
        return None

def calc_time_since_last_update(file_path):
    last_modified = get_last_modified_time(file_path)
    time_elapsed_sec = int(time.time()) - int(last_modified)
    time_elapsed_hour = (time_elapsed_sec // 3600)
    return time_elapsed_hour
        


def load_or_fetch_crypto_data():
    try:
        with open('crypto_data.json', 'r') as f:
            file_path = 'crypto_data.json'
            print("Data file found. Updating with this hour's data")
            symbols_data = fetch_symbols()    
            crypto_data = json.load(f)
            last_n_hours = calc_time_since_last_update(file_path)
            update_crypto_data(symbols_data, crypto_data, last_n_hours = last_n_hours)
            
    except FileNotFoundError:
        print("Data file not found. Fetching new data.")
        symbols_data = fetch_symbols()
        crypto_data = fetch_kline_data_for_symbols(symbols_data)
        
        with open('crypto_data.json', 'w') as f:
            json.dump(crypto_data, f)

    return crypto_data

