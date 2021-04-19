import bs4 as bs
import requests

html = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
print(html.text)