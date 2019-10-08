import requests
import os
import json
import queue
import asyncio

from datetime import datetime
from multiprocessing import Process


# TAGS = ["热门","最新","经典","可播放","豆瓣高分","冷门佳片",
#         "华语","欧美","韩国","日本","动作","喜剧","爱情",
#         "科幻","悬疑","恐怖","成长"]
TAGS = ["治愈"]
PAGE_LIMIT = 100  # 当返回结果小于 page limit 后，每递增一个 offset，减少一个 item，其余与前重复
BASE_URL = "https://movie.douban.com/j/search_subjects?" \
           "type=movie&tag={}&page_limit=" + str(PAGE_LIMIT) + "&page_start={}"
MOVIE_PATH = '/Users/veritas.wang/v/rating-analysis/data/movie/raw_1_movie_lists'

class ListCrawler(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = BASE_URL
        # self.data_queue = queue.Queue()

    # def get_movie_list(self, tag):
    #     offset = 0
    #     while True:
    #         try:
    #             json_data = requests.get(self.base_url.format(tag, offset)).json()
    #         except Exception as e:
    #             print(e.__str__())
    #             break
    #         if len(json_data) == 0 or json_data is None:
    #             break
    #         self.data_queue.put({tag + '_' + str(offset): json_data})
    #         offset += 1

    async def async_get_movie_list(self, tag):
        print("==============\n{}\nSTART TIME:{}\n".format(
            tag, datetime.now().timestamp()))
        offset = 0
        while True:
            try:
                m_url = self.base_url.format(tag, offset * PAGE_LIMIT)
                print(m_url)
                json_data = requests.get(m_url).json()
            except Exception as e:
                print(e.__str__())
                break
            if len(json_data["subjects"]) == 0 or json_data is None:
                break
            # print(json_data)
            self.write_json_file(tag + '_' + str(offset), json_data)
            # self.data_queue.put({tag + '_' + str(offset): json_data})
            # print("REQUEST Q-SIZE:", self.data_queue.qsize())

            offset += 1   
        print("\n{}\nEND TIME:{}\n==============\n".format(
            tag, datetime.now().timestamp()))

    async def async_run(self, tags):
        for tag in tags:
            await asyncio.gather(self.async_get_movie_list(tag))

    def run_get_movie_list(self, tags):
        asyncio.run(self.async_run(tags))

    def put_none_to_q(self):
        self.data_queue.put(None)

    def write_json_file(self, k, json_data):
        # print("==============\n{}\nSTART TIME:{}\n".format(
        #         k, datetime.now().timestamp()))
        target_file = MOVIE_PATH + '/' + k + '.json'
        f = open(target_file, "w")
        f.write(json.dumps(json_data, indent=2, ensure_ascii=False))
        f.close()
        # print("==============\n{}\nEND TIME:{}\n".format(
        #     k, datetime.now().timestamp()))
            
    def _p_write_json_file(self, target_path):
        print("==============\nJSON WRITER START TIME:{}\n".format(
            datetime.now().timestamp()))
        while True:
            print("JSON WRITER, Q-SIZE:", self.data_queue.qsize())
            json_data = self.data_queue.get()
            if json_data is None:
                print("JSON WRITER BREAK")
                break
            k = list(json_data.keys())[0]
            print("==============\n{}\nSTART TIME:{}\n".format(
                k, datetime.now().timestamp()))
            target_file = target_path + '/' + k + '.json'
            f = open(target_file, "w")
            f.write(json.dumps(json_data.get(k), indent=2))
            f.close()
            self.data_queue.task_done()
            print("==============\n{}\nEND TIME:{}\n".format(
                k, datetime.now().timestamp()))

    def _p_info(self, taskname):
        print("========", taskname)
        print('module name:', __name__)
        if hasattr(os, 'getppid'):  # only available on Unix
            print('parent process:', os.getppid())
        print('process id:', os.getpid())

    def p_writer_json(self, target_path):
        self._p_info('writer_json')
        self._p_write_json_file(target_path)

    def multi_json_writer(self, target_path):
        print("==============\nJSON WRITER\nSTART TIME:{}\n".format(
            datetime.now().timestamp()))
        p1 = Process(target=self.p_writer_json, args=(target_path,))
        p2 = Process(target=self.p_writer_json, args=(target_path,))
        p1.start()
        p2.start()
        self.data_queue.join()
        p1.join()
        p2.join()
        print("==============\nJSON WRITER\nEND TIME:{}\n".format(
            datetime.now().timestamp()))
        


def get_path(relative_path):
    cur_path = os.getcwd()
    if relative_path.startswith('/'):
        relative_path = '/' + relative_path
    return cur_path + relative_path


if __name__ == '__main__':
    print("START TIME IS {}".format(datetime.now().timestamp()))
    movie = ListCrawler()
    # movie.multi_json_writer(file_path)
    # p0 = Process(target=movie.run_get_movie_list, args=(TAGS,))
    # p1 = Process(target=movie.p_writer_json, args=(file_path,))
    # p2 = Process(target=movie.p_writer_json, args=(file_path,))
    # p1.start()
    # p2.start()
    # p0.start()
    movie.run_get_movie_list(TAGS)
    # file_path = get_path('data/movie/raw_1_movie_lists')
    # print(file_path)
    # print(type(file_path))
    # movie.data_queue.join()
    # p1.join()
    # p2.join()
    print("START TIME IS {}".format(datetime.now().timestamp()))

