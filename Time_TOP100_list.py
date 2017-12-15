#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re

def download_page(url):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    date=requests.get(url,headers=headers).content
    return date

def parse_html(html):
    movie_name_list=[]
    soup=BeautifulSoup(html,"html.parser")
    ul=soup.find('ul',attrs={'id':'asyncRatingRegion'})
    print '-----------\n1-10:'
    movie_name_list.append(parse_html_ul(ul))
    a=1
    next_page=soup.find('div',attrs={'id':'PageNavigator'}).find('a',attrs={'class':'num'})
    next_url=next_page['href'].lstrip('http://www.mtime.com/top/movie/top100/')
    while a<10:
        next_url=re.sub(r'\d',str(a+1),next_url)
        html=download_page('http://www.mtime.com/top/movie/top100/i'+next_url)
        soup=BeautifulSoup(html,"html.parser")
        ul=soup.find('ul',attrs={'id':'asyncRatingRegion'})
        print '-----------\n',a*10+1,'-',(a+1)*10,':'
        movie_name_list.append(parse_html_ul(ul))
        next_page=soup.find('div',attrs={'id':'PageNavigator'}).find('a',attrs={'class':'num'})
        a=a+1
    print '\n',str(movie_name_list).decode('string_escape')   #这里输出电影名字列表

def parse_html_ul(ul):
    movie_name_list=[]
    for li in ul.find_all('li'):
        h2=li.find('h2',attrs={'class':'px14 pb6'})
        movie_name=h2.find('a')
        movie_name=re.sub(r'^.*target="_blank">','',str(movie_name))
        movie_name=re.sub(r'</a>$','',movie_name)
        print movie_name                                 #这里输入电影名字
        movie_name_list.append(movie_name)
    return movie_name_list

def main():
    download_url='http://www.mtime.com/top/movie/top100/'
    html=download_page(download_url)
    parse_html(html)
    print '\nThat\'s all.'

if __name__ == '__main__':
    main()
