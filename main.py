from judge_dispatcher import JudgeDispatcher

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SubmissionData(BaseModel):
    url: str
    code: str
    language: str

# https://www.hackerearth.com/practice/algorithms/searching/linear-search/practice-problems/algorithm/count-mex-8dd2c00c/

@app.post("/submit")
def submit(data: SubmissionData):
    submitter= JudgeDispatcher.choose_website('submit', data.url)
    result = submitter.submit_solution(data.url,data.code,data.language)
    return {"status": "submitted", "result": result}

@app.get("/scrape")
def scrape(url: str):
    scraper = JudgeDispatcher.choose_website('scraper',url)
    problem = scraper.scrap_problem(url)
    return problem
