import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import pandas as pd

# pagenatinoがあるかどうか確かめる
def is_pagenation(page):
    url = 'https://creww.me/ja/search/startup?page=' + str(page)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    next_page = soup.find('li', class_='next')
    link = next_page.find('a')
    print(link.get('href'))
    if link:
        return True
    else:
        return False


get_url = []
# URLを取得する
for i in range(1,):

    if is_pagenation(i):
        start_url = 'https://creww.me/ja/search/startup?page=' + str(i)
        r = requests.get(start_url)
        soup = BeautifulSoup(r.text, 'lxml')
        startup_block = soup.find_all('div', class_='startup-block')
        
        # 企業のリンクを取得して、配列に格納する
        # blockはだいたい18個
        for x in range(len(startup_block)):
            startup_link = startup_block[x].find('div', class_='startup-name')
            get_url.append(startup_link.find('a').get('href'))
    else:
        print('pagenatino end --------------------------')
        break


# 最後吐き出し
df = pd.DataFrame(data=get_url, columns=['get_company_url'])
df.to_csv('./output/get_company_url.csv')