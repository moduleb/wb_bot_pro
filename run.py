import asyncio

from parser import check_price



def main():
    url = 'https://www.wildberries.ru/catalog/180400996/detail.aspx'
    delay = 2
    asyncio.run(check_price(url, delay))


if __name__ == "__main__":
    main()
