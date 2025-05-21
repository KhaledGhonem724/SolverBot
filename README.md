# SolverBot
## Component 1: main
Contains the FastAPI Logic. <br>
this part is fixed. <br>

<hr>

## Component 2: judge_dispatcher
Contains logic for choosing the suitable submitting/scraping class. <br>
this logic is contained in a class, which initializing method is: <br>
```python
def __init__(self):
    self.routes = {
        'scrape': {
            # <online judge domain>: <scraper class name>
            'TheOnlineJudge.com': TheOnlineJudgeProblemScrapper, # 
        },
        'submit': {
            # <online judge domain>: <submitter class name>
            'TheOnlineJudge.com': TheOnlineJudgeProblemSubmitter,
        }
    }
```
This application structure allows the extension to support other platforms. <br>

<hr>

## Component 3: OJ_Bots
Contains a file for each Online Judge. <br>
Each file MUST have 2 classes: a **submitter class** and **scraper class**. <br>

### The submitter class
it must have a function with the following signature: <br>
```python
def submit_solution(url, code, language, username="bot_username", password="bot_password"): 
    # your logic
    pass 
``` 
which take the following parameters. <br>
* `url`           : string - link to the problem. <br>
* `code`          : string - solution code to be submitted to the OJ. <br>
* `language`      : string - determine the programming language of the code. <br>
* `bot_username`  : string - the username of the user or (default value: the bot username)
* `bot_password`  : string - the password of the user or (default value: the bot password)

### The scraper class
it must have a function with the following signature: <br>
```python
def scrape_problem(url, username="bot_username", password="bot_password"): 
    # your logic
    pass
``` 
which take the following parameters. <br>
* `url`           : string - link to the problem. <br>
* `bot_username`  : string - the username of the user or (default value: the bot username)
* `bot_password`  : string - the password of the user or (default value: the bot password)

<hr>

## Extend the application to support another OJ
to allow the application to support new online judge, just do the following steps:  <br>  
1. add your own file to `OJ_Bots` folder.
2. this file must follow the interface for its inner classes and functions.
3. you must edit the `judge_dispatcher` file by:
   * importing scraper class and submitter class from your OJ_Bot file. 
   * adding your **online judge domain** and **class name** in the initializing method.
4. you don't need to edit the `main` file.

<hr>

### Thank you

SolverBot/
├── OJ_Bots/
│   ├── interfaces
│   │   ├── scraper_interface.py
│   │   └── submitter_interface.py
│   └──  hacker_earth.py
├── CodingFiles/
│   ├── code.cpp
│   ├── code.java
│   └── code.py
├── main.py
└── judge_dispatcher.py
