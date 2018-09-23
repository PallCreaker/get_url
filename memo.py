

######################## ストリング内の文字列抽出 #######################


# タグ内の文字列取得
soup.a.string

# タグ内のすべての文字列取得（セパレータ文字、前後文字削除）
soup.get_text("|", strip=True)


######################## ストリング内の削除方法 #######################

# Bタグを削除
div.b.extract()
print('extract: ', div.string)


####################### 抽出方法 #######################

# 複数クラスセレクタ
soup.findAll('div', class_=['A', 'B'])

# 正規表現を使用した抽出
import re
soup.find_all(re.compile("^b"))

# CSSセレクタで取得（すべて）
soup.select('CSSセレクタ')

soup.select("title")
soup.select("p nth-of-type(3)")
soup.select("html head title")
soup.select("head > title")
soup.select("p > #link1")