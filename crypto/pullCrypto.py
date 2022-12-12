import requests

API_KEY = '246052d1-25f4-42b6-8248-6d3fe6e6226b'

headers = {
    'X-CMC_PRO_API_KEY': API_KEY
}

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
r = requests.get(url, headers=headers)
find_ranks = {}
if r.status_code == 200:
    data = r.json()
    for d in data['data']:
        symbol = d['symbol']
        find_ranks[symbol] = d['cmc_rank']
print(find_ranks)