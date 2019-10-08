import scrapy
import os


MOVIE_IDS = ''
BASE_URL = "https://movie.douban.com/subject/{}/"
MOVIE_DATA_PATH = ''

MOVIE_D = {
    "id": None, "name": None, "year": None, "genre": None,
    "IMDb": None, "rating": None,
    "director": None, "auther": None, "actors": None,
    "web": None, "country": None, "lang": None,
    "show_time": None, "movie_length": None, "alias": None,
    "playable": None
}

SHORT_COMMENTS = [{"id": None}]

LONG_COMMENTS = [{"id": None}]

class MovieSpider(scrapy.Spider):
    name = 'movie'

    def start_requests(self):
        with open(MOVIE_IDS) as f:
            for line in f:
                yield scrapy.Request(
                    url=BASE_URL.format(line), callback=self.parse)

    def parse(self, response):
        cur_dir = response.url.split('/')[-2]
        os.mkdir(MOVIE_DATA_PATH + '/' + cur_dir)
