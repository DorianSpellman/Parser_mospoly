import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re


# URL_TEMP = 'https://mospolytech.ru/news/?PAGEN_1='
FILE_NAME = "mospoly.csv"
RESULT = {'title': [], 'content': [], 'date': [], 'link' : []}

for i in range(1, 6):
    URL_TEMP = f'https://mospolytech.ru/news/?PAGEN_1={i}'

    req = requests.get(URL_TEMP)
    soup = bs(req.text, "html.parser")


    class Mospoly:

        def __init__(self, data):
            self.data = data
            self.clear_data = list()

        def to_format(self):
            for data in self.data:
                data = re.sub(r"<[^>]+>", "", str(data), flags=re.S)
                data = data.replace('\n', '')
                data = data.replace('\r', '')
                data = data.replace('\t', '')
                self.clear_data.append(data.strip('\n'))

            return self.clear_data


    titles = Mospoly(soup.find_all('div', class_='card-news-wide__title')).to_format()
    contents = Mospoly(soup.find_all('div', class_='card-news-wide__text')).to_format()
    dates = Mospoly(soup.find_all('div', class_='card-news-wide__date')).to_format()
    links = Mospoly(soup.find_all('a', class_='card-news-wide__link')).to_format()


    for title in titles:
        RESULT['title'].append(title)

    for content in contents:
        RESULT['content'].append(content)

    for date in dates:
        RESULT['date'].append(date)

    for link in links:
        RESULT['link'].append('https://mospolytech.ru' + link)
        


df = pd.DataFrame(data=RESULT)
df.to_csv(FILE_NAME)

