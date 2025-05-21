#from online_judge_bots.hacker_earth import HackerEarthProblemSubmitter
from online_judge_bots.hacker_earth_scraper import HackerEarthProblemScrapper

class BotDispatcher:
    def __init__(self):
        self.routes = {
            'scrape': {
                'hackerearth.com': HackerEarthProblemScrapper,
            },
            'submit': {
#                'hackerearth.com': HackerEarthProblemSubmitter,
            }
        }

    def choose_website(self, task: str, url: str):
        for domain, handler_class in self.routes.get(task, {}).items():
            if domain in url:
                return handler_class()
        return None