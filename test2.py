import asyncio
import aiohttp

lists = ['eth', 'btc', 'xmr', 'req', 'xlm', 'etc', 'omg', 'neo', 'btc', 'xmr', 'req', 'xlm', 'etc', 'omg', 'neo']


async def fetch(client, item):
    url = 'https://coincap.io/{endpoint}/{coin_name}'.format(
        endpoint='page',
        coin_name=item.upper()
    )
    async with client.get(url) as resp:
        assert resp.status == 200
        html = await resp.text()
        print(html)


async def main():
    async with aiohttp.ClientSession() as client:
        await asyncio.gather(*[
            asyncio.ensure_future(fetch(client, item))
            for item in lists
        ])


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
