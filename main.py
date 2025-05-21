from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from online_judge_bots.bot_dispatcher import BotDispatcher
from online_judge_bots.interfaces.scraper_interface import BaseScraper
from online_judge_bots.interfaces.submitter_interface import BaseSubmitter

app = FastAPI()


class SubmissionData(BaseModel):
    url: str
    code: str
    language: str


class ScrapeRequest(BaseModel):
    url: str


@app.post("/submit")
def submit(data: SubmissionData):
    dispatcher = BotDispatcher()
    submitter: BaseSubmitter = dispatcher.choose_website('submit', data.url)

    if not submitter:
        raise HTTPException(status_code=400, detail="Unsupported judge or invalid URL.")

    result = submitter.submit_solution(data.url, data.code, data.language)
    return {"status": "submitted", "result": result}


@app.post("/scrape")
def scrape(data: ScrapeRequest):
    dispatcher = BotDispatcher()
    scraper: BaseScraper = dispatcher.choose_website('scrape', data.url)

    if not scraper:
        raise HTTPException(status_code=400, detail="Unsupported judge or invalid URL.")

    problem = scraper.scrap_problem(data.url)
    return problem

