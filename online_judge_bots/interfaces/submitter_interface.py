from abc import ABC, abstractmethod

class BaseSubmitter(ABC):
    @abstractmethod
    def submit_solution(self, url: str, code: str, language: str) -> dict:
        """Submit code to the given problem URL and return result."""
        raise NotImplementedError
