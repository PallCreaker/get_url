import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import pandas as pd
import random
import re

intro_list = ['key', 'url', '会社名_title','会社URL', '紹介文', 'why', 'how', 'what', 'supporter']
info_list  = ['創業者', '所在地', 'チーム', '業界', 'チームの強み', 'サービスの形態', 'ローンチ', 'ラウンド', 'ステージ', '資本金', '会社名', '対象地域', '交際ステータス', '職種', '事業規模', '性別', 'その他', '個人年収', '年齢層']


# 格納するDFを作成
df = pd.DataFrame(columns = intro_list + info_list)

base_url = 'https://creww.me/'
companies = pd.read_csv('./output/get_company_url.csv')

intro_dict = {}
info_dict = {}
# サービスについて情報を取得する 
for key, url in companies.iterrows():

    # sleepを入れる
    sl_num = random.randint(1, 5)
    sleep(sl_num)

    company_url = base_url + url['get_company_url']

    r = requests.get(company_url)
    soup = BeautifulSoup(r.text, 'lxml')

    intro_dict['key'] = key
    intro_dict['url'] = company_url
    intro_dict['会社名_title'] = soup.select('.headline-container span.name')[0].get_text().strip()
    intro_dict['会社URL'] = soup.select('.headline-container div.profile-website-url')[0].a.get_text().strip()

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
            # traceback.print_exc()
            pass
        # 掲載がない場合
        for key in intro_list:
            if key not in intro_dict.keys():
                intro_dict[key] = '記載なし'

    #########
    ######### ここからinformationを取得する
    #########
    get_info_company_url = company_url + '/info'
    nr = requests.get(get_info_company_url)
    soup_info = BeautifulSoup(nr.text, 'lxml')
    # 2つの情報を取得
    for infomation_block in soup_info.select('.panel.panel-default'):
                # ヘッドラインごとにデータを取得する
        headline = infomation_block.find('div', class_='panel-heading')
        # h2がないblockがあるため、
        try:
            if headline.h2.text.strip() == 'スタートアップ情報':
                for row in infomation_block.select('div.info-data .row'):
                    # tableのヘッダーを取得 selectはlist型になる
                    th = row.select('div:nth-of-type(1)')[0].text.strip()

                    # tableの中身にspanがある場合
                    td = ''
                    if row.select('div:nth-of-type(2)')[0].find_all('span'):
                        # rowのなかに、tagがある場合
                        for tag in row.select('div:nth-of-type(2)')[0].find_all('span'):

                            if tag.find_all('a'):
                                # 普通のタグの場合
                                td = td + '[' + tag.a.text + ']'
                            else:
                                # 創業者の場合
                                td = td + '[' + tag.text.strip() + ']'
                    else:
                        # rowのなかに、tagがない場合
                        td = row.select('div:nth-of-type(2)')[0].text.strip()

                    # 値を格納していく
                    info_dict[th] = td

            elif headline.h2.text.strip() == 'サービスのターゲット':
                if infomation_block.select('div.target-data .row'):
                    for row in infomation_block.select('div.target-data .row'):
                        # tableのヘッダーを取得 selectはlist型になる
                        th = row.select('div:nth-of-type(1)')[0].text.strip()
                        
                        # tagを取得する
                        td = ''
                        for tag in row.select('div:nth-of-type(2)')[0].find_all('span'):
                            td = td + '[' + tag.text.strip() + ']'

                        # 値を格納する
                        info_dict[th] = td
            
        except Exception:
            # h2のタグがない場合
            import traceback
            # traceback.print_exc()
            pass
        
        # 掲載がない場合
        for key in info_list:
            if key not in info_dict.keys():
                info_dict[key] = '記載なし'

    # 最後にデータフレームに格納していく
    # 一個の辞書型にする
    intro_dict.update(info_dict)
    df_tmp = pd.DataFrame(intro_dict, index=[intro_dict['key']])
    df = pd.concat([df, df_tmp], sort=False)

    # title = re.sub(re.compile("[!-/:-@[-`’”{-~]"), '', intro_dict['会社名_title'])
    path_name = './output/part/company_' + str(intro_dict['key']) + '.csv'

    # df_tmp.to_csv(path_name, index=False, encoding='shift_jis')
    df_tmp.to_csv(path_name, index=False)

    print('{0} 社目  sleep:{1}'.format(intro_dict['key'], sl_num))
    print(intro_dict['会社名_title'])
    print(info_dict['創業者'])
    print('-----------------------')


# 最後吐き出し
# df.to_csv('./output/get_company_information.csv', index=False, encoding='shift_jis')
df.to_csv('./output/get_company_information.csv', index=False)

print('end===================================')
