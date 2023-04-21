import asyncio
from functools import lru_cache

import httpx

from core.lib.lru_cache import async_lru_cache


# 请求次数
baidu_num = 0


async def parse_data():
    result = await get_baidu()
    return result


@async_lru_cache()
async def get_baidu():
    print('请求百度')
    global baidu_num
    baidu_num += 1
    async with httpx.AsyncClient() as client:
        response = await client.get('http://www.baidu.com')
    result = response.text
    return result


@lru_cache()
def get_data():
    print('get_data')
    return 3


if __name__ == '__main__':
    result = asyncio.run(parse_data())

    result2 = asyncio.run(parse_data())
    print(result2)
    print(f'{baidu_num = }')
