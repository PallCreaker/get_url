import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import pandas as pd
import glob
import os
import codecs as cd

# 個別のファイルを取得してマージする

path = r'./output/part/'
all_files = glob.glob(os.path.join(path, "*.csv"))


# with cd.open("filename.csv", "r", "cp932", "ignore") as csv_file:
#     df = pd.read_table(csv_file)

df_from_each_file = (pd.read_csv(f, encoding = 'utf-8') for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)

print(concatenated_df)


# 最後吐き出し
# concatenated_df.to_csv('./output/all_company_information.csv', encoding = 'cp932', index = False)
concatenated_df.to_csv('./output/all_company_information.csv', index = False)


