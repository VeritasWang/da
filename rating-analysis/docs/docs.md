# Purpose
Purge the rating of movies and books

# Plan
## Step one - get raw data
- movie
1. Get movie lists with different tag
Douban has 17 tags, ["热门","最新","经典","可播放","豆瓣高分","冷门佳片","华语","欧美","韩国","日本","动作","喜剧","爱情","科幻","悬疑","恐怖","成长"]. One movie may has multiple tags.
movie list can be get via the request `https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit=5&page_start=0'

Data will be stored in json data in `data/movie/raw_1_movie_lists.

2. Order movies and associate them with given tags
3. Get detail info of a movie, e.g. casting, rating
4. Assoicate a movie with IMDB rating

- books
## Step two - categorize data