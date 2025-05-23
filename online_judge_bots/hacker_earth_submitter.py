from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from interfaces.submitter_interface import BaseSubmitter

username="khaledghonem724"
password="GoToCode_72"
problemLink="https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/make-an-array-85abd7ad/"
storing_file="coding_files/hacker_earth_code.txt"
prog_lang="cpp"
source_code='''
#include<bits/stdc++.h>
using namespace std;
int solve (int N, vector<int> A) {
    unordered_set<int>st;
    int maxi=A[0];
    for (int i=0;i<N;i++){
        st.insert(A[i]);
        maxi= max(maxi,A[i]);
    }
    if(st.size()>2){
        return -1;
    }else{
        return maxi;
    }
}

int main() {

    ios::sync_with_stdio(0);
    cin.tie(0);
    int T;
    cin >> T;
    for(int t_i = 0; t_i < T; t_i++)
    {
        int N;
        cin >> N;
        vector<int> A(N);
        for(int i_A = 0; i_A < N; i_A++)
        {
        	cin >> A[i_A];
        }

        int out_;
        out_ = solve(N, A);
        cout << out_;
        cout << "\n";
    }
}
'''

def clean_cpp_code(self,code) -> str:
    return str(code).replace('/', '//')

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

class Submission:
    def __init__(self):
        self.link = None
        self.lang = None
        self.code = None
        self.judge_response = None
    def __str__(self):
        return (
                '<<<<<<<<<<<<<<<<<<<< Submission printing >>>>>>>>>>>>>>>>>>>> \n'+
                'submission link : ' + str(self.link) + '\n==========================================================================\n' +
                'code language : ' + str(self.lang) + '\n==========================================================================\n' +
                'judge_response : ' + str(self.judge_response) + '\n==========================================================================\n' +
                'code : \n' + str(self.code) + '\n==========================================================================\n'
        )
    def __repr__(self):
        return (
                'submission link : '+ str(type(self.link)) + ' : ' + str(self.link) +'\n' +
                'code language : '+ str(type(self.lang)) + ' : ' + str(self.lang) +'\n' +
                'judge_response : '+ str(type(self.judge_response)) + ' : ' + str(self.judge_response) + '\n' +
                'code : \n'+ str(type(self.code))  + ' : ' + str(self.code) + '\n'
                )
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



class HackerEarthProblemSubmitter(BaseSubmitter):
    def __init__(self,bot_user = None):
        self.driver = webdriver.Chrome()
        self.bot = bot_user
        if self.bot is None:
            self.bot = BotUser(self.driver)
        self.bot.login()
        self.submission = Submission()
    def write_code_into_file(self,code,file_path = "/solutions/hacker_earth_code.txt") -> str:
        '''
        DO :
        1- choose a file to write the code in it        # NOT COMPLETE #
        2- clean the code           (use "cleaner")     # DONE #
        3- write the code in the choosen file           # DONE #
        :param code:
        :param file_path:
        :return:
        '''
        # NEED : choose file_path according to language
        code = clean_cpp_code(code)
        f = open(file_path, "w")
        f.write(code)
        f.close()
        return file_path
    def submit_solution(self,problem_link,code,language,sleep_time=2):
        '''
        DO:
        1- get the solution file                (use "self.write_code_into_file")
        2- choose the programming language      # NOT COMPLETE #
        3- upload the solution file             # DONE #
        4- scrap the judge response             # NOT COMPLETE #
        5- fill "self.submission"               # NOT COMPLETE #
        :param problem_link:
        :param code:
        :param language:
        :param sleep_time:
        :return:
        '''
        # NEED : scrap the result , fill "self.submission"
        # NEED : use "language"
        file_path = self.write_code_into_file(code)
        self.driver.get(problem_link)
        time.sleep(sleep_time)  # time for loading the problem content # not a must

        file_input = self.driver.find_elements(By.ID, "codeFile")[0]
        file_input.send_keys(file_path)
        print(file_input)
        time.sleep(sleep_time)  # time for updating # not a must
        language_select = self.driver.find_elements(By.CLASS_NAME, "nice-select")[0]

        # nice-select
        submit_button = self.driver.find_elements(By.CSS_SELECTOR,
                                             "a[class='float-right button btn-blue close-modal-window submit-code medium-margin-right']")
        time.sleep(sleep_time)  # time for searching # it's a MUST
        # submit_button[0].click()

problem_urls =[
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/equal-strings-79789662-4dbd707c/",
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/make-an-array-85abd7ad/",
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/count-mex-8dd2c00c/"
]
url = problem_urls[2] # try every link to see different results
submitter = HackerEarthProblemSubmitter()
submitter.submit_solution(url,source_code,prog_lang)