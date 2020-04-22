import json
import os
import time
import datetime
import requests
from math import ceil


# import chisquaredmodel


class Guardian:
    api_key = ""
    url = "https://content.guardianapis.com/"

    def __init__(self, api_key="5046ff4b-1de1-4cd7-ba17-ace15f3e94ed", load_cached=False):
        self.api_key = api_key
        self.settings = {"api-key": api_key}
        self.articles = []
        self.tries = 0
        if load_cached:
            self.__load_articles()

    def add_setting(self, key, value):
        self.settings[key] = value

    def search(self):
        try:
            return requests.get(self.url + "search", self.settings)
        except requests.exceptions.ConnectionError:
            self.__save_articles()

    def search_full(self):
        if len(self.articles) > 0:
            start_year = int(self.articles[-1]["webPublicationDate"][:4])
        else:
            start_year = 2000
        year = datetime.datetime.now().year
        for y in range(start_year, year):
            for m in range(1, 13):
                self.add_setting("from-date", f"{y}-{str(m).zfill(2)}-02")
                if m == 12:
                    self.add_setting("to-date", f"{y + 1}-01-01")
                else:
                    self.add_setting("to-date", f"{y}-{str(m + 1).zfill(2)}-01")
                print(f"\n{self.settings['from-date']} <--> {self.settings['to-date']}")
                self.add_setting("page", 1)
                pages = self.__get_articles()
                print(f"starting at page 1 of {pages} pages...")
                # time.sleep(17.28)
                for i in range(2, pages + 1):
                    # print(f"page {i}...")
                    self.add_setting("page", i)
                    self.__get_articles()
                    # time.sleep(17.28)
        self.__save_articles()

    def __get_articles(self):
        results = self.search()
        if results is None:
            print("Got none. Saving and retrying...")
            self.__save_articles()
            self.__get_articles()
        if results.status_code == 200:
            self.tries = 0
            data = results.json()['response']
            self.articles.extend(x for x in data['results'] if x not in self.articles)
            return data['pages']
        elif results.status_code == 429:
            if self.tries < 2:
                self.tries += 1
                print(
                    f"Received status code {results.status_code} for reason {results.reason}... sleeping for one second")
                time.sleep(1)
                self.__get_articles()
            elif self.tries < 3:
                time.sleep(86400)
                self.__get_articles()
            else:
                self.__save_articles()
                raise ConnectionError
        else:
            if self.tries < 5:
                self.tries += 1
                print(
                    f"Received status code {results.status_code} for reason {results.reason}... sleeping for 5 minutes")
                self.__save_articles()
                time.sleep(300)
                self.__get_articles()
            else:
                self.__save_articles()
                raise ConnectionError

    def __save_articles(self):
        if os.path.isdir("data/news/"):
            with open("data/news/articles.json", "w") as file:
                json.dump(self.articles, file)
        else:
            os.makedirs("data/news/")
            self.__save_articles()

    def __load_articles(self):
        if os.path.exists("data/news/articles.json"):
            with open("data/news/articles.json", "r") as file:
                self.articles = json.load(file)
        else:
            print("Could not load cached articles")


if __name__ == '__main__':
    news = Guardian(load_cached=True)
    news.add_setting("show-fields", "bodyText")
    news.add_setting("page-size", 200)
    news.add_setting("order-by", "oldest")
    news.add_setting("type", "article")
    news.search_full()
    # print(news.search())
