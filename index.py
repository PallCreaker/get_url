# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

# ブラウザでアクセスする
driver.get("file:///Users/admin/Desktop/index.html")

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode('utf-8')

# BeautifulSoupで扱えるようにパースします
soup = BeautifulSoup(html, "html.parser")

# idがheikinの要素を表示
print(soup.select_one("#heikin"))