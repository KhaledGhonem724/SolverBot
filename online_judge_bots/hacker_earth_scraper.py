import json
from symtable import Class

from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from interfaces.scraper_interface import BaseScraper

def clean_problem_tags_into_list(str_tags):
    str_tags = str_tags.strip()
    str_tags = str_tags.strip(',')
    temp_list = str_tags.split(',')
    tags_list=[]
    for item in temp_list:
        item = item.strip()
        if len(item) < 2:
            continue
        tags_list.append(item.lower())
    return tags_list

def clean_problem_statement(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove SVG output; keep the preview/script (MathJax_Preview)
    for span in soup.find_all("span", class_=["MathJax_SVG"]):
        span.decompose()

    # Add <br> in empty or spacing spans
    for span in soup.find_all("span", class_=["MJXp-mspace"]):
        if span.string is None:
            br_tag = soup.new_tag("br")
            span.append(br_tag)
    # print(soup.prettify()) # for testing
    return str(soup.prettify())

def clean_sample_io(html):
    soup = BeautifulSoup(html, "html.parser")

    # add <br> after the title "Sample Input" and "Sample Output
    for div in soup.find_all("div"):
        div_text = div.get_text()
        if "Sample" in div_text:
            br_tag = soup.new_tag("br")
            div.append(br_tag)
    # print(soup.prettify()) # for testing
    return str(soup.prettify())

def clean_mathjax_html(html):
    soup = BeautifulSoup(html, "html.parser")
    # Remove MathJax_SVG - and keep MathJax_Preview
    for span in soup.find_all("span", class_=["MathJax_SVG"]):
        span.decompose()
    print(soup.prettify()) # for testing
    return str(soup.prettify())

class BotUser:
    def __init__(self, driver, username = "khaledghonem724",password ="GoToCode_72"):
        self.driver = driver
        self.username = username
        self.password = password
    def check_login_errors(self):
        # check if the login is successful
        # if there are errors print them and return False
        # if not then return True
        errors_list = self.driver.find_elements(By.CSS_SELECTOR, "ul[class ='errorlist nonfield']")
        if len(errors_list) > 0:
            errors = errors_list[0].find_elements(By.TAG_NAME, 'li')
            massage = []
            for error in errors:
                massage.append(error.text)
                print(error.text)
            result = {"is_done": False, "massage": massage}
            print("=======")
            print(result)
            return result
        print("Successfully logged in!")  # testing
        return {"is_done":True,"massage":["Successfully logged in!"]}
    def login(self,sleep_time=2) :
        '''
        :param bot_username: username used to log in
        :param bot_password: password used to log in
        :param sleep_time: number of seconds between each step of the log in
        :return: dict that have 2 keys
        {
            "is_done": bool : True if the login is successful , False otherwise
            "massage": list[str] : list of messages (errors or declaration of Success)
        }
        '''
        # go to log in page, fill the form and submit it
        self.driver.get("https://www.hackerearth.com/login/")
        time.sleep(sleep_time)              # time for updating
        self.driver.find_element(By.ID, "id_login").send_keys(self.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        print("Loging in ...")              # testing
        self.driver.find_element(By.NAME, "signin").click()
        time.sleep(sleep_time)              # time for updating
        return self.check_login_errors()

class Problem:
    def __init__(self):
        self.link = None
        self.title = None
        self.time_limit = None
        self.memory_limit = None
        self.tags = None
        self.statement = None
        self.testcases = None
        self.explanation = None
    def __str__(self):

        return (
                '<<<<<<<<<<<<<<<<<<<< problem printing >>>>>>>>>>>>>>>>>>>> \n'+
                'problem title : ' + str(self.title) + '\n==========================================================================\n' +
                'problem link : ' + str(self.link) + '\n==========================================================================\n' +
                'time_limit : ' + str(self.time_limit) + '\n==========================================================================\n' +
                'memory_limit : ' + str(self.memory_limit) + '\n==========================================================================\n' +
                'tags : ' + str(self.tags) + '\n==========================================================================\n' +
                'statement : \n' + str(self.statement) + '\n==========================================================================\n' +
                'testcases : \n' + str(self.testcases) + '\n==========================================================================\n' +
                'explanation : \n' + str(self.explanation) + '\n'
        )
    def __repr__(self):
        return (
                'problem title : '+ str(type(self.title)) + ' : ' + str(self.title) +'\n' +
                'problem link : '+ str(type(self.link)) + ' : ' + str(self.link) +'\n' +
                'time_limit : '+ str(type(self.time_limit)) + ' : ' + str(self.time_limit) + '\n' +
                'memory_limit : '+ str(type(self.memory_limit)) + ' : ' + str(self.memory_limit) + '\n' +
                'tags : '+ str(type(self.tags)) + ' : ' + str(self.tags) + '\n' +
                'statement : \n'+ str(type(self.statement))  + ' : ' + str(self.statement) + '\n' +
                'testcases : \n'+ str(type(self.testcases))  + ' : ' + str(self.testcases) + '\n' +
                'explanation : \n'+ str(type(self.explanation))  + ' : ' + str(self.explanation) + '\n'
                )
    def generate_problem_handle(self):
        handle:str = self.title.strip().lower().replace(' ', '_')
        handle='hacker_earth_'+handle
        return handle
    def get_json(self):
        return {
            'problem_handle': self.generate_problem_handle(),
            'link': self.link ,
            'website': 'HackerEarth',
            'title': self.title,
            'timelimit': self.time_limit,
            'memorylimit': self.memory_limit,
            'statement': self.statement,
            'testcases': self.testcases,
            'notes': self.explanation
        }

class HackerEarthProblemScrapper(BaseScraper):
    def __init__(self,bot_user = None):
        self.driver = webdriver.Chrome()
        self.bot = bot_user
        if self.bot is None:
            self.bot = BotUser(self.driver)
        self.bot.login()
        self.full_problem_page = None
        self.problem = Problem()
    def scrap_problem(self,problem_link):
        self.driver.get(problem_link)
        self.full_problem_page = self.driver.find_element(By.CLASS_NAME, "practice-problem-container")
        # fill problem attributes
        self.problem.link = problem_link                            # Done
        self.problem.tags = self.set_problem_tags()                 # Need work
        self.problem.title = self.set_problem_title()               # Done
        self.problem.time_limit , self.problem.memory_limit = self.set_problem_limits()     # Done
        self.problem.statement = self.set_problem_statement()
        self.problem.testcases = self.set_problem_testcases()
        self.problem.explanation = self.set_problem_explanation()
        json_object = {
            'status': 'scraped',
            'problem': self.problem.get_json(),
            'tags': self.problem.tags
        }
        print(json.dumps(json_object, indent=4)) # for testing
        return json_object
    def set_problem_tags(self):
        # under development
        MetaData = self.full_problem_page.find_element(By.CLASS_NAME, "problem-meta")
        listofMobileHiddens = MetaData.find_elements(By.CLASS_NAME,"mobile-hidden")
        str_tags = listofMobileHiddens[1]
        return clean_problem_tags_into_list(str_tags.text)
        return str_tags.text
    def set_problem_title(self):
        title = self.full_problem_page.find_element(By.CLASS_NAME,"title")
        return title.text
    def set_problem_limits(self):
        str_limits = self.full_problem_page.find_element(By.CLASS_NAME, "problem-solution-limits").text
        str_limits = str_limits.strip()
        str_limits = str_limits[:-13].strip()

        str_time_limit = str_limits[:str_limits.find("Memory")].strip()
        str_memory_limit = str_limits[str_limits.find("Memory"):].strip()

        # time_limit = int(str_time_limit.split(':')[1])
        # memory_limit = int(str_memory_limit.split(':')[1])

        return str_time_limit + " Sec", str_memory_limit + " MB"
    def set_problem_statement(self):
        web_element_statement = self.full_problem_page.find_element(By.CLASS_NAME, "description")
        html_statement = web_element_statement.get_attribute('innerHTML')
        str_problem_statement = clean_problem_statement(html_statement)
        return str_problem_statement
    def set_problem_testcases(self):
        web_element_testcases = self.full_problem_page.find_element(By.CLASS_NAME, "input-output-container")
        html_testcases = web_element_testcases.get_attribute('innerHTML')
        str_sample_io = clean_sample_io(html_testcases)
        return str_sample_io
    def set_problem_explanation(self):
        web_element_explanation = self.full_problem_page.find_element(By.CLASS_NAME, "explanation")
        html_explanation = web_element_explanation.get_attribute('innerHTML')
        return html_explanation

problem_urls =[
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/equal-strings-79789662-4dbd707c/",
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/make-an-array-85abd7ad/",
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/count-mex-8dd2c00c/"
]
url = problem_urls[2] # try every link to see different results
scrapper = HackerEarthProblemScrapper()
problem = scrapper.scrap_problem(url)
