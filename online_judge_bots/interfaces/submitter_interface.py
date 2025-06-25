from abc import ABC, abstractmethod
from pydantic import BaseModel, field_validator
from typing import Union, Dict

class OnlineJudgeResponseModel(BaseModel):
    online_judge_response: str
    original_submission_link: str

class SubmitResponseModel(BaseModel):
    task_completed: str
    response: Union[str, OnlineJudgeResponseModel]


    @field_validator("task_completed")
    @classmethod
    def check_task_completed(cls, v):
        if v not in ("True", "False"):
            raise ValueError("task_completed must be 'True' or 'False'")
        return v


class BaseSubmitter(ABC):
    @abstractmethod
    def submit_solution(self, url: str, code: str, language: str) -> SubmitResponseModel:
        """Submit code to the given problem URL and return result."""
        raise NotImplementedError
