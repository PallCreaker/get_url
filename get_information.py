import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import pandas as pd


base_url = 'https://creww.me/'
companies = pd.read_csv('./output/get_company_url.csv')

# 格納するDFを作成
df_intro = pd.DataFrame(columns = ['key', 'url', '会社名', '紹介文', 'why', 'how', 'what', 'supporter'])
df_info  = pd.DataFrame(columns = ['創業者', '所在地', 'チーム', '業界', 'チームの強み', 'サービスの形態', 'ローンチ', 'ラウンdの', 'ステージ', '資本金', '会社名', '対象地域', '交際ステータス', '職種', '事業規模', '性別', 'その他', '個人年収', '年齢層'])

intro_dict = {}
# サービスについて情報を取得する 
    # サービス紹介文
    # なぜやっているのか
    # どうやっているのか
    # 今やっていること
    # こんなサポーターを求めています。
for key, url in companies.iterrows():
    # company_url = base_url + url['get_company_url']
    company_url = 'https://creww.me/ja/startup/gifee.co'
    # https://creww.me/ja/startup/caliljp
    r = requests.get(company_url)
    soup = BeautifulSoup(r.text, 'lxml')

    intro_dict['key'] = key
    intro_dict['url'] = company_url
    intro_dict['会社名'] = soup.select('.headline-container span.name')[0].get_text().strip()

    for infomation_block in soup.select('.panel.panel-default'):

        # ヘッドラインごとにデータを取得する
        headline = infomation_block.find('div', class_='panel-heading')

        # h2がないblockがあるため、
        try:
            if headline.h2.text == 'サービス紹介文':
                # headlineがない場合がある
                if infomation_block.get('.panel-body.about-slider .media-heading'):
                    introduction_head = infomation_block.select('.panel-body.about-slider .media-heading')[0].text.strip()
                else:
                    introduction_head = ''
                introduction = introduction_head + '\n' + infomation_block.find('div', class_='about-slider').p.text.strip()
                intro_dict['紹介文'] = introduction
            elif headline.h2.text == 'なぜやっているのか':
                intro_dict['why'] = infomation_block.find('div', class_='media-body').p.text.strip()
            elif headline.h2.text == 'どうやっているのか':
                intro_dict['how'] = infomation_block.find('div', class_='media-body').p.text.strip()
            elif headline.h2.text == '今やっていること':
                # 複数のサービスが存在する
                service = ''
                for service_block in infomation_block.find_all('div', class_ = 'media'):
                    service_head = service_block.find('div', class_ = 'media-heading').text.strip()
                    service_body = service_block.p.text.strip()

                    # サービスの中にタグが埋め込まれている場合がある
                    service_tag = ''
                    if service_block.find_all('span'):
                        for tags in service_block.find_all('span'):
                            service_tag = service_tag + '[' + tags.a.text + ']'

                    service = service + ' \n\n ' + service_head + ' \n ' + service_body + ' \n ' + service_tag
                intro_dict['what'] = service
            elif headline.h2.text == 'こんなサポーターを求めています':
                intro_dict['supporter'] = infomation_block.find('ul').text
        except Exception:
            # h2のタグがない場合
            import traceback
            traceback.print_exc()
            pass
        # 掲載がない場合
        for key in ['key', 'url', '会社名', '紹介文', 'why', 'how', 'what', 'supporter']:
            if key not in intro_dict.keys():
                intro_dict[key] = '記載なし'

    print(intro_dict)
    break


print('end===================================')

