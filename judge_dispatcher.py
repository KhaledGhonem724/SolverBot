from OJ_Bots.hacker_earth import HackerEarthProblemScrapper
from OJ_Bots.hacker_earth import HackerEarthProblemSubmitter

class JudgeDispatcher:
    def __init__(self):
        self.routes = {
            'scrape': {
                'hackerearth.com': HackerEarthProblemScrapper,
            },
            'submit': {
                'hackerearth.com': HackerEarthProblemSubmitter,
            }
        }

    def choose_website(self, task: str, url: str):
        for domain, handler_class in self.routes.get(task, {}).items():
            if domain in url:
                return handler_class()
        return None