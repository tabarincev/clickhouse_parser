from abc import abstractmethod, ABC
from pyparsing import ParserElement


class Statement(ABC):
    @property
    @abstractmethod
    def notation(self) -> ParserElement:
        pass
