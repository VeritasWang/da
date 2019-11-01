import requests
import bs4
import lxml


def get_html(url):
    try:
        movie_detail = requests.get(url)
        movie_detail.raise_for_status()
        movie_detail.endcodding = 'utf-8'
        return movie_detail.text
    except Exception as e:
        print(e.__str__())
        return "Error in get html"

def get_content(movie_detail):
    soup = bs4.BeautifulSoup(movie_detail, 'lxml')
    print(soup.prettify())


a = get_html('https://movie.douban.com/subject/1292722/')
get_content(a)