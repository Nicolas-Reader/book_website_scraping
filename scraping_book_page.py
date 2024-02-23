# Import the necessary libraries.
import json
import requests
from os import mkdir
from bs4 import BeautifulSoup


# Define a function to convert book data to JSON file.
def data_to_json(data: dict, file_name: str, url_cover: str) -> None:
    # Remove invalid characters from the file name.
    for sign in [':', '?', '.', '/', '|', '<', '>', '*', '"', ',']:
        file_name = file_name.replace(sign, '')
    file_name = file_name.replace(' ', '_')
    if len(file_name) >= 50:
        file_name = file_name.split(',')[0]
    path = f'books/main genres/{file_name}'
    try:
        mkdir(path)
    except FileExistsError:
        mkdir(f'{path}_{data['year_of_creation']}')
    with open(f'{path}/{file_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
    print(file_name, 'successful scraping')
    cover_bytes = requests.get(url_cover).content
    with open(f'{path}/{file_name}.jpg', 'ab') as cover:
        cover.write(cover_bytes)


# Define a function to scrape book information from a web page.
def scraping_book_info(req: requests) -> None:
    # Parse the HTML content of the web page.
    soup_book = BeautifulSoup(req.text, 'lxml', )
    full_page = soup_book.find('div', class_='ant-row ant-row-center acq6ib-0 iONKLl')
    try:
        cover_url = full_page.find('picture').find('source').get('srcset').split(' ')[1]
    except AttributeError:
        cover_url = 'https://i1.mybook.io/p/x756/book_covers/38/59/385947e0-5084-4c7e-af93-09e4d79b61fe.jpg'
    try:
        full_info = full_page.find('div', class_='sc-1c0xbiw-0 hvfXON')
    except AttributeError:
        return
    rating = full_info.find('div', class_='sc-1s4c57r-0 goYpPi').find('b').text
    book_name = full_info.find('div', class_='m4n24q-0 hJyrxa').text
    book_author = full_info.find('div', class_='m4n24q-0 bkolKJ').text
    try:
        other_info = full_info.find('div', class_='ant-col sc-1c0xbiw-9 eSjGMZ').find_all('p', class_='lnjchu-1 dPgoNf')
        pages_count = other_info[0].text
        reading_time = other_info[1].text.split('≈ ')[1]
        year_of_creation = other_info[2].text
        age_limit = other_info[3].text
    except IndexError:
        return
    genres = full_page.find('div', class_='sc-1sg8rha-0 gHinNz').find_all('div', class_='sc-1sbv3y7-1 eVvZLL')
    all_genres = []
    for genre in genres:
        all_genres.append(genre.text)
    full_data = {
        'book_name': book_name,
        'book_author': book_author,
        'pages_count': pages_count,
        'reading_time': reading_time,
        'year_of_creation': year_of_creation,
        'rating': rating,
        'age_limit': age_limit,
        'genres': all_genres
    }
    for data in full_data:
        full_data[data] = full_data[data].replace(' ', ' ')

    data_to_json(full_data, book_name.replace(' ', ' '), cover_url)
