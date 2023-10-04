from typing import Dict

from abc import ABC, abstractmethod


class BaseBuilder(ABC):
    @abstractmethod
    def build(self, ast: Dict) -> str:
        pass
