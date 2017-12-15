#coding=utf-8

import requests
from bs4 import BeautifulSoup
import codecs

def download_page(url):
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'}
    date=requests.get(url,headers=headers).content
    return date

def parse_html(html):
    movie_name_list=[]
    soup=BeautifulSoup(html,"html.parser")
    ol=soup.find('ol',attrs={'class':'grid_view'})
    movie_name_list.append(parse_html_ol(ol))
    next_page=soup.find('span',attrs={'class':'next'}).find('a')
    while next_page:
        next_url=next_page['href']
        html=download_page('https://movie.douban.com/top250'+next_url)
        soup=BeautifulSoup(html,"html.parser")
        ol=soup.find('ol',attrs={'class':'grid_view'})
        movie_name_list.append(parse_html_ol(ol))
        next_page=soup.find('span',attrs={'class':'next'}).find('a')
    #print '\n',str(movie_name_list).decode('string_escape')   #打印电影名字列表
    return movie_name_list

def parse_html_ol(ol):
    movie_name_list=[]
    for li in ol.find_all('li'):
        div=li.find('div',attrs={'class':'hd'})
        movie_name=div.find('span',attrs={"class":'title'})
        movie_name=str(movie_name).lstrip('<span class="title">').rstrip('</span>')
        #print movie_name                                      #打印电影名字
        movie_name_list.append(movie_name)
    return movie_name_list

def main():
    download_url='https://movie.douban.com/top250'
    html=download_page(download_url)
    with codecs.open('DoubanMovies_Top250','wb') as movienamef:
        movie_name_list=[]
        movie_name_list=parse_html(html)
        for movie_name in movie_name_list:
            movie_name=str(movie_name).decode('string_escape')
            movienamef.write(movie_name)
            movienamef.write('\n')
            print movie_name
        print '\nThat\'s all.'

if __name__ == '__main__':
    main()
