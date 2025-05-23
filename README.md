# 🚀 SolverBot

**SolverBot** is an extensible FastAPI-based platform that automates problem scraping and solution submission for various online judges.

---

## 📁 Project Structure

```
SolverBot/
├── main.py                         ← API entry point (FastAPI)
├── online_judge_bots/
│   ├── example_scraper.py          ← Platform-specific scraper (e.g., HackerEarth)
│   ├── example_submitter.py        ← Platform-specific submitter (e.g., HackerEarth)
│   ├── bot_dispatcher.py           ← Dispatcher for routing tasks
│   └── interfaces/
│       ├── scraper_interface.py    ← Abstract scraper base class
│       └── submitter_interface.py  ← Abstract submitter base class
└── coding_files/
    ├── example_code.txt            ← Temp storage for solution code
    └── ...                         ← One code file per platform
```

---

## 🔧 Components

### 1. `main.py` — **API Entry Point**

* Built using **FastAPI**
* Handles incoming requests to scrape or submit solutions
* **⚠️ This file is fixed — do not modify it**

---

### 2. `bot_dispatcher.py` — **Bot Dispatcher**

* Dynamically routes tasks to the correct platform-specific scraper/submitter classes

```python
def __init__(self):
    self.routes = {
        'scrape': {
            'example.com': ExampleOJProblemScraper,
        },
        'submit': {
            'example.com': ExampleOJProblemSubmitter,
        }
    }
```

* To support new platforms, add entries to this dictionary

---

### 3. `submitter.py` — **Submitter Class**

* Each online judge has a corresponding submitter file
* Implements `BaseSubmitter` from `submitter_interface.py`
* Filename must be in `snake_case` (e.g., `example_submitter.py`)

#### ✅ Input JSON:

```json
{
  "url": "",
  "language": "",
  "code": "",
  "username": "default_username",
  "password": "default_password"
}
```

#### ✅ Output JSON:

```json
{
  "status": "submitted",      // or "error"
  "content": "Accepted"       // "Wrong Answer" , "Time Limit Exeeded" Or Error Message 
}
```

#### 📌 Example Template:

```python
# example_submitter.py
from online_judge_bots.interfaces.submitter_interface import BaseSubmitter

class ExampleOJProblemSubmitter(BaseSubmitter):
    def submit(self, data: dict) -> dict:
        url = data.get("url")
        language = data.get("language")
        code = data.get("code")
        username = data.get("username")
        password = data.get("password")

        # Implement submission logic here
        return {
            "status": "submitted",
            "content": "Accepted"
        }
```

---

### 4. `scraper.py` — **Scraper Class**

* Each online judge has a scraper file that implements `BaseScraper` from `scraper_interface.py`
* Filename must be in `snake_case` (e.g., `example_scraper.py`)

#### ✅ Input JSON:

```json
{
  "url": ""
}
```

#### ✅ Output JSON:

```json
{
  "status": "scraped",
  "problem": {
    "problem_handle": "",
    "link": "",
    "website": "",
    "title": "",
    "timelimit": "",
    "memorylimit": "",
    "statement": "",
    "testcases": "",
    "notes": ""
  },
  "tags": []
}
```

#### 📌 Example Template:

```python
# example_scraper.py
from online_judge_bots.interfaces.scraper_interface import BaseScraper

class ExampleOJProblemScraper(BaseScraper):
    def scrape(self, url: str) -> dict:
        # Implement scraping logic here
        return {
            "status": "scraped",
            "problem": {
                "problem_handle": "SUM123",
                "link": url,
                "website": "example.com",
                "title": "Sum of Two Numbers",
                "timelimit": "1s",
                "memorylimit": "256MB",
                "statement": "Calculate the sum of two integers.",
                "testcases": "Input: 2 3\nOutput: 5",
                "notes": "Use fast I/O"
            },
            "tags": ["math", "beginner"]
        }
```

---

### 5. `interfaces/` — **Base Interfaces**

* `scraper_interface.py`:

  ```python
  class BaseScraper:
      def scrap_problem(self, url: str) -> dict:
          raise NotImplementedError
  ```

* `submitter_interface.py`:

  ```python
  class BaseSubmitter:
      def submit_solution(self, data: dict) -> dict:
          raise NotImplementedError
  ```

* **⚠️ These files must not be modified**
---
### 6. `coding_files/` — **Temporary Code Storage**

* Used to temporarily store solution code for submission.
* Each platform can have its own file (e.g., `example_code.txt`).
* These files can be used internally during the submit process.

#### ✅ Developer Note:

You **can** manually add a dedicated file for your online judge (e.g., `yourjudge_code.txt`) if your scraper or submitter needs custom code handling or staging.

Just ensure your submitter writes to and reads from this file as needed. Example:

```python
# In your submitter
with open("coding_files/yourjudge_code.txt", "w") as f:
    f.write(code)
```

* File naming should follow this convention: `snake_case` + `_code.txt` (e.g., `hacker_rank_code.txt`)
* This part is optional — only if your submitter needs it.

---

## ➕ How to Add Support for a New Online Judge

1. **Create a new scraper and submitter class**:

   * Add `your_judge_scraper.py` and `your_judge_submitter.py` in `online_judge_bots/`
   * Implement `BaseScraper` and `BaseSubmitter`

2. **Register them in `bot_dispatcher.py`**:

```python
from online_judge_bots.your_judge_scraper import YourJudgeProblemScraper
from online_judge_bots.your_judge_submitter import YourJudgeProblemSubmitter

self.routes = {
    'scrape': {
        'yourjudge.com': YourJudgeProblemScraper,
    },
    'submit': {
        'yourjudge.com': YourJudgeProblemSubmitter,
    }
}
```

3. **You're done!** No need to touch `main.py`, or interfaces.

---

## 🌟 Support the Project

If you find this project useful, please ⭐ the repo on GitHub — it helps others discover it and keeps the momentum going!

---

## 🙏 Thank You

Thanks for checking out **SolverBot**! Contributions, feature ideas, and bug reports are all welcome.
