from abc import ABC, abstractmethod

class BaseScraper(ABC):
    @abstractmethod
    def scrap_problem(self, url: str) -> dict:
        """Extract problem data from the given URL."""
        raise NotImplementedError
