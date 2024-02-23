import requests

from scraping_book_page import scraping_book_info
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


url = 'https://mybook.ru/catalog/books/?page='
header = {
    'user-agent': UserAgent().random
}


def books_scraping() -> None:
    page = 1
    while True:
        req = requests.get(url=f'{url}{page}', headers=header)
        soup_books = BeautifulSoup(req.text, 'lxml')
        books = soup_books.find_all('div', class_='e4xwgl-0 iJwsmp')
        if books is None:
            break
        for book in books:
            book_url = book.find_next('div', class_='e4xwgl-1 gEQwGK').find('a').get('href')
            print(book_url)
            req_book = requests.get(url=f'https://mybook.ru{book_url}', headers=header)
            scraping_book_info(req_book)
        page += 1


if __name__ == '__main__':
    books_scraping()
