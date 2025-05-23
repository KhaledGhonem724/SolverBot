from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException, WebDriverException
)

from interfaces.submitter_interface import BaseSubmitter

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # goes from 'online_judge_bots' to 'SolverBot'
FILE_PATH = BASE_DIR / "coding_files" / "hacker_earth_code.txt"
#FILE_PATH = "/home/khaledghonem/gitrepos/SolverBot/coding_files/hacker_earth_code.txt"
DEFAULT_USERNAME = "khaledghonem724"
DEFAULT_PASSWORD = "GoToCode_72"



problemLink="https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/make-an-array-85abd7ad/"
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
    }
}
'''

def clean_cpp_code(code) -> str:
    return str(code).replace('\\', '\\\\')

class BotUser:
    def __init__(self, driver, username, password):
        self.driver = driver
        self.username = username
        self.password = password

    def check_login_errors(self):
        '''
        Checks if there are any login error messages.

        :return: dict with result status and messages
        '''
        try:
            # Wait until we either leave the login page or timeout
            WebDriverWait(self.driver, 2).until(
                lambda d: "login" not in d.current_url
            )
        except:
            # Timeout: still on login page — check for errors
            pass

        # Check for error messages
        errors_list = self.driver.find_elements(By.CSS_SELECTOR, "ul.errorlist.nonfield")
        if errors_list:
            error_items = errors_list[0].find_elements(By.TAG_NAME, 'li')
            messages = [error.text for error in error_items]
            print("Login Errors:", messages)
            return {"is_done": False, "message": messages}

        print("Successfully logged in!")
        return {"is_done": True, "message": ["Successfully logged in!"]}

    def login(self, sleep_time=2):
        '''
        Logs in to HackerEarth.

        :return: dict with login result and messages
        '''
        self.driver.get("https://www.hackerearth.com/login/")

        # Wait for login form fields to load
        WebDriverWait(self.driver, sleep_time).until(
            EC.presence_of_element_located((By.ID, "id_login"))
        )

        self.driver.find_element(By.ID, "id_login").send_keys(self.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        self.driver.find_element(By.NAME, "signin").click()

        return self.check_login_errors()

class HackerEarthProblemSubmitter(BaseSubmitter):
    '''
    returned JSON object:
    {
          "task_completed": "True",
          "response": {"online_judge_response": oj_response,"original_submission_link": submission_link}
    }
    or JSON object that contains
    {
              "task_completed": "False",
              "response": "the error message"
    }

    '''
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.bot = None

    def create_bot(self,username=None,password=None):
        if  username is None or password is None :
            self.bot = BotUser(self.driver, DEFAULT_USERNAME, DEFAULT_PASSWORD)
        else:
            self.bot = BotUser(self.driver, username ,password )
        self.bot.login()

    def write_code_into_file(self, code):
        #code = clean_cpp_code(code)
        with open(FILE_PATH, "w") as f:
            f.write(code)

    def upload_the_file(self,problem_link):
        self.driver.get(problem_link)
        # where we will upload the file
        file_input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "codeFile"))
        )
        file_input_element.send_keys(str(FILE_PATH))

    def select_programming_language(self, language):
        # Wait for the select dropdown to be clickable
        dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "select.nice-select"))
        )
        select = Select(dropdown)

        # Map language to option value
        lang_map = {
            "cpp": "CPP17",
            "python": "PYTHON3_8",
            "java": "JAVA17"
        }

        if language not in lang_map:
            return {"is_done": False, "message": f"language : {language} is not supported"}

        option_value = lang_map[language]

        # Wait for the option with the desired value to be present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"select.nice-select option[value='{option_value}']")
            )
        )

        # select the option
        select.select_by_value(option_value)

        return {"is_done": True, "message": f"Selected language with value: {option_value}"}

    def response_is_ready(self,driver, submission_link):
        print("iam in response_is_ready")
        driver.get(submission_link)
        spans = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.result > span"))
        )
        print("checking ... ")
        if len(spans) < 2:
            return False  # not enough spans yet
        second_span_text = spans[1].text
        print("until now : "+second_span_text)

        if "Evaluating solution" not in second_span_text:
            return second_span_text  # condition met, return the response
        return False  # keep waiting

    def scrap_oj_response(self, problem_link):
        print("scraping the problem")
        self.driver.get(problem_link+"submissions/")
        print("waiting for element_to_be_clickable")
        #past-submission

        past_submission_table= WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".past-submission"))
        )

        first_row = WebDriverWait(past_submission_table, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table-row.table-body"))
        )

        # Extract relevant data from the first row's columns
        columns = first_row.find_elements(By.CLASS_NAME, "table-column")


        submission_link= columns[6].find_element(By.TAG_NAME, "a").get_attribute("href")
        print(submission_link)
        self.driver.get(submission_link)
        result_spans = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.result > span"))
        )

        oj_response = WebDriverWait(self.driver, 60, poll_frequency=5).until(
            lambda driver: self.response_is_ready(driver, submission_link)
        )

        print("response :", oj_response)

        return {"status": "done", "online_judge_response": oj_response,"original_submission_link": submission_link}

    def submit_solution(self,problem_link,code,language, username = None, password = None):
        '''
        writing the code into internal file
        uploading the file as input
        selecting programming language
        submitting the solution (code file and selected programming language)
        scrape the OJ response
        :param problem_link:
        :param code:
        :param language:
        :param username: Optional
        :param password: Optional
        :param sleep_time: Optional
        :return: the scraped response
        '''
        try:
            # Step 1: create and login the bot user
            try:
                self.create_bot(username, password)
            except Exception as e:
                print(f"Login bot user failed: exception: {e}")
                return {
                    "task_completed": "False",
                    "response": f"Login bot user failed: exception: {e}"
                }
            # Step 2: Writing the code into internal file
            try:
                self.write_code_into_file(code)
            except Exception as e:
                print(f"Failed to write code to internal file: exception: {e}")
                return {
                    "task_completed": "False",
                    "response": f"Failed to write code to internal file: exception: {e}"
                }

            # Step 3: Upload Code File as input
            try:
                self.upload_the_file(problem_link)
            except Exception as e:
                print(f"File upload failed: exception: {e}")
                return {
                    "task_completed": "False",
                    "response": f"File upload failed: exception: {e}"
                }

            print("file uploaded") # Loging

            # Step 4: Select Programming Language
            # NOTE: can be updated to scrape from the OJ through another microservice
            try:
                lang_result = self.select_programming_language(language)
                print(lang_result["message"])
                if not lang_result["is_done"]:
                    return {
                        "task_completed": "False",
                        "response": f"Language selection failed: exception: {lang_result["message"]}"
                    }
            except Exception as e:
                print(f"Language selection failed: exception: {e}")
                return {
                    "task_completed": "False",
                    "response": f"Language selection failed: exception: {e}"
                }

            print(lang_result["message"]) # Loging

            # Step 5: Submitting
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                "a.float-right.button.btn-blue.close-modal-window.submit-code.medium-margin-right"))
                )
                submit_button.click()
            except Exception as e:
                print(f"Submission click failed: exception: {e}")
                return {
                    "task_completed": "False",
                    "response": f"Submission click failed: exception: {e}"
                }

            print("solution submitted") # Loging

            # Step 6: Scrape Submission Result
            # Format : {oj_response , oj_submission_link}
            try:
                response = self.scrap_oj_response(problem_link)
            except Exception as e:
                print(f"Scraping OJ response failed: exception: {e}")
                return {
                    "task_completed": "False",
                    "response": f"Scraping OJ response failed: exception: {e}"
                }

            return {
                "task_completed": "True",
                "response": response
            }
        except Exception as e:
            print(f"Error during submission: {e}")
            return {
                "task_completed": "False",
                "response": str(e)
            }
        finally:
            # quit driver to clean up resources
            if self.driver:
                self.driver.quit()




problem_urls =[
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/equal-strings-79789662-4dbd707c/",
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/make-an-array-85abd7ad/",
    "https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/count-mex-8dd2c00c/"
]
url = problem_urls[2] # try every link to see different results
submitter = HackerEarthProblemSubmitter()
submitter.submit_solution(url,source_code,prog_lang)
