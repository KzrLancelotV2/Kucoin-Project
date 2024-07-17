import api
from kucoin.client import Client
import extract_data

crypto_data = extract_data.load_or_fetch_crypto_data()
#TODO : add update function to update klines everyday instead of running
# it for the past 30 days each day
#TODO : calculate rsi by hand. (rsi for each coin in each hour)
#TODO : check date of JSON file and update accordingly