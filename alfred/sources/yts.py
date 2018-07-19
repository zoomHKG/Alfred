#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

"""yts.ag scrapping stuffs here"""


class YTS():
    """Class for YTS scrapping"""

    def __init__(self):
        self.crawlUrl = 'https://yts.am/'

    def get_latest(self):
        latest_movies = []
        source_code = requests.get(self.crawlUrl)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        latest_parent = soup.find('div', {'class': 'home-movies'})
        latest_child_div = latest_parent.findAll('div', {'class': 'browse-movie-wrap'})
        for l in latest_child_div:
            movie_name_div = l.find('div', {'class': 'browse-movie-bottom'})
            movie_name = movie_name_div.find('a', {'class': 'browse-movie-title'}).text
            latest_movies.append(movie_name)
        return latest_movies

    def get_featured(self):
        featured_movies = []
        source_code = requests.get(self.crawlUrl)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        featured_parent = soup.find('div', {'id': 'popular-downloads'})
        featured_child_div = featured_parent.findAll('div', {'class': 'browse-movie-wrap'})
        for f in featured_child_div:
            movie_name_div = f.find('div', {'class': 'browse-movie-bottom'})
            movie_name = movie_name_div.find('a', {'class': 'browse-movie-title'}).text
            featured_movies.append(movie_name)
        return featured_movies
