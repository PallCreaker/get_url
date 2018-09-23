import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import pandas as pd


comapnies = pd.read_csv('./output/get_company_url.csv')

