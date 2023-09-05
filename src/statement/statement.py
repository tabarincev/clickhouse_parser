from pyparsing import ParserElement

from typing import Dict
from abc import abstractmethod, ABC


class Statement(ABC):
    def parse(self, sql: str, validation=True) -> Dict:
        return self.notation.parse_string(sql, parse_all=validation)

    @property
    @abstractmethod
    def notation(self) -> ParserElement:
        pass