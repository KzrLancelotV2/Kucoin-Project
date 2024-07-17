from kucoin.client import Client

api_key = "6692560b8433fb0001fe4ec5"
api_secret = "1755430a-034e-432c-a1c2-a0f67215ee69"
passphrase = "FuturesProject2"

def config_client():
    client = Client(api_key= api_key, api_secret= api_secret, passphrase=passphrase)    

    try:
        accounts = client.get_accounts()
        print("API credentials are valid!\n")
        print(accounts)
        
    except Exception as e:
        print(f"Failed to retrieve accounts: {e}")
        
    return client

