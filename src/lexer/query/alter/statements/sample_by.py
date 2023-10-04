from pyparsing import ParserElement

from src.lexer.statement import Statement
from src.keywords import MODIFY, SAMPLE, BY


class AlterSampleBy(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + SAMPLE + BY + self._column_expr('expr')
        ).set_parse_action(lambda term: {'modify_sample_by': term['expr']})