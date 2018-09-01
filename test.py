import json
import os
import shutil
import requests as r


def refresh_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)


database = open('coin.json').read()
db_json = json.loads(database)
idx = 'https://s2.coinmarketcap.com/generated/search/quick_search.json'

print('request coin info')
res = r.get(idx).json()
coin_info = [{
    'name': coin['name'],
    'slug': coin['slug'],
    'img_id': coin['id'],
    'symbol': coin['symbol'],
} for coin in res]
coin_symbols = {coin['symbol'] for coin in coin_info}
database_symbols = {coin['symbol'] for coin in db_json}

coin_symbols -= database_symbols

print('save coin info')
with open("coin.json", 'wb') as f:
    f.write(bytes(json.dumps(coin_info), encoding='utf-8'))

need_request = [coin for coin in coin_info if coin['symbol'] in coin_symbols]
print('need request : ', len(need_request))

if need_request:
    refresh_dir('img')

    def img_url_maker(coin_id):
        return 'https://s2.coinmarketcap.com/static/img/coins/128x128/' \
               '{}.png'.format(coin_id)


    img_urls = [img_url_maker(coin['img_id']) for coin in need_request]
    img_binary = []
    print('request image')
    for k, url in enumerate(img_urls):
        res = r.get(url, headers={'Cache-Control': 'public'})
        img_binary.append(res.content)

    print('saving files')
    for k, img in enumerate(img_binary):
        file_name = coin_info[k]['slug']
        with open("img/{}.png".format(file_name), 'wb') as f:
            f.write(img)


print('total coins :', len(coin_info))