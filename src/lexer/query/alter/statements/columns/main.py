from pyparsing import MatchFirst, ParserElement, Forward

from .add import AddColumn


class AlterColumn:
    def __init__(self):
        self._column_expr = Forward()

    @property
    def notation(self) -> ParserElement:
        return MatchFirst([
            AddColumn().notation
        ])
