# coding: utf-8


import requests
from bs4 import BeautifulSoup as bsp
from settings import *
import re


class OfficialAccount:

    oa = None
    oa_url = ''
    collection_name = ''
    page_urls = []
    max_page = -1
    headers = HEADERS
    base_url = BASE_URL

    @classmethod
    def search_oa(cls, oa_name):
        # print 'self.search_oa()'
        search_url = cls.base_url + '/search?q=' + oa_name
        try:
            response = requests.get(search_url, headers=cls.headers)
            # print response.text
            if re.search(u'没有找到相关内容', response.text):
                # print 1
                return False
            else:
                soup = bsp(response.text, 'html.parser')
                # 根据搜索结果
                target = soup.find('a', class_='user')
                # print target['href']
                cls.oa = oa_name
                cls.oa_url = cls.base_url + target['href']
                return cls.oa_url
        except:
            # print 3
            return False

    @classmethod
    def get_max_page(cls):
        # print 'self.get_max_page()'
        try:
            response = requests.get(cls.oa_url, headers=cls.headers)
            soup = bsp(response.text, 'html.parser')
            max_page = int(soup.find_all('div', class_='w4_5')[-1].span.find_all('a')[-1].text)
            # 转为int
            cls.max_page = max_page
            # print type(max_page)
            return max_page
        except:
            return -1

    @classmethod
    def get_page_urls(cls):
        # print 'self.get_page_urls()'
        cls.collection_name = cls.oa_url.split('/')[-1]
        cls.page_urls = [cls.base_url+'/account/'+cls.collection_name+'?start={}'.format(i * 12) for i in
                         range(int(cls.max_page))]

    @classmethod
    def get_article(cls, page_url):
        print 'self.get_article()'
        response = requests.get(page_url, headers=cls.headers)
        soup = bsp(response.text, 'html.parser')
        info = soup.findAll('a', class_='question_link')
        article_names = [i.text.strip() for i in info]
        article_links = [cls.base_url + i['href'] for i in info]
        return zip(article_names, article_links)
