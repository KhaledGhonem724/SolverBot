# 🚀 SolverBot

SolverBot is an extensible automation platform for scraping programming problems and submitting solutions to online judges. Built with FastAPI, it provides a modular API for integrating multiple platforms, starting with HackerEarth.

---

## Features

- **Scrape Problems:** Extract problem statements, constraints, and test cases from supported online judges.
- **Submit Solutions:** Automate code submission (framework in place; extendable for new judges).
- **Modular Design:** Easily add support for new judges via plug-and-play scrapers and submitters.
- **REST API:** Simple endpoints for integration with other tools or UIs.

---

## Project Structure

```
SolverBot/
├── main.py                      # FastAPI entry point
├── requirements.txt             # Python dependencies
├── online_judge_bots/
│   ├── bot_dispatcher.py        # Routes tasks to the correct bot
│   ├── hacker_earth_scraper.py  # HackerEarth scraper implementation
│   ├── hacker_earth_submitter.py# (Stub) HackerEarth submitter
│   └── interfaces/
│       ├── scraper_interface.py # Abstract scraper base class
│       └── submitter_interface.py # Abstract submitter base class
├── coding_files/                # Temporary code storage
└── README.md                    # Project documentation
```

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/SolverBot.git
cd SolverBot
```

### 2. Install dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the API server

```bash
uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

### `POST /scrape`

Scrape a problem statement from a supported online judge.

**Request Body:**
```json
{
  "url": "https://www.hackerearth.com/problem/example/"
}
```

**Response:**
```json
{
  "status": "scraped",
  "problem": {
    "problem_handle": "hacker_earth_example_problem",
    "link": "https://www.hackerearth.com/problem/example/",
    "website": "HackerEarth",
    "title": "Example Problem",
    "timelimit": "1 Sec",
    "memorylimit": "256 MB",
    "statement": "...",
    "testcases": "...",
    "notes": "..."
  },
  "tags": ["math", "greedy"]
}
```

---

### `POST /submit`

Submit a solution to a supported online judge.

**Request Body:**
```json
{
  "url": "https://www.hackerearth.com/problem/example/",
  "code": "print('Hello, world!')",
  "language": "python"
}
```

**Response:**
```json
{
  "status": "submitted",
  "result": {
    "is_submitted": true,
    "response": "Accepted"
  }
}
```

---

## Supported Judges

- **HackerEarth** (scraping supported; submission framework stubbed)
- *Easily extendable to others (see below)*

---

## Extending: Add a New Online Judge

1. **Create Scraper/Submitter Classes:**
   - Implement `BaseScraper` and/or `BaseSubmitter` in `online_judge_bots/`.
2. **Register in `bot_dispatcher.py`:**
   - Add your classes to the `routes` dictionary under the appropriate domain.
3. **No need to modify `main.py` or interfaces.**

---

## Dependencies

- Python 3.8+
- FastAPI
- Uvicorn
- Selenium
- BeautifulSoup4
- (See `requirements.txt` for full list)

---

## Contributing

Pull requests, bug reports, and feature suggestions are welcome! Please open an issue or submit a PR.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
