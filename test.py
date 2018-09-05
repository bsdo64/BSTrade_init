import json
import os
import shutil
import requests as r
import asyncio
import aiohttp


def refresh_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)


print('request coin info db')
try:
    database = open('coin.json').read()
    db_json = json.loads(database)
except FileNotFoundError:
    db_json = []

print('request coin info api')
idx = 'https://s2.coinmarketcap.com/generated/search/quick_search.json'
res = r.get(idx).json()
coin_info = [{
    'name': coin['name'],
    'slug': coin['slug'],
    'img_id': coin['id'],
    'symbol': coin['symbol'],
} for coin in res]

print('compare coin info')
coin_ids = {coin['img_id'] for coin in coin_info}
database_ids = {coin['img_id'] for coin in db_json}
coin_ids -= database_ids
need_request = [coin for coin in coin_info if coin['img_id'] in coin_ids]

print('need request : ', len(need_request))
if need_request:
    refresh_dir('img')

    print('request image')
    async def fetch(client, item):
        url = 'https://s2.coinmarketcap.com/static/img/coins/128x128/' \
               '{}.png'.format(item['img_id'])

        async with client.get(url) as resp:
            assert resp.status == 200
            img_b = await resp.read()
            with open('img/{}.png'.format(item['slug']), 'wb') as f:
                f.write(img_b)


    async def main():
        async with aiohttp.ClientSession() as client:
            await asyncio.gather(*[
                asyncio.ensure_future(fetch(client, item))
                for item in coin_info
            ])


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print('total coins :', len(database_ids))

print('save coin info')
with open("coin.json", 'wb') as f:
    f.write(bytes(json.dumps(coin_info), encoding='utf-8'))