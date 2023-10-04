from pyparsing import ParserElement

from src.lexer.statement import Statement
from src.keywords import MODIFY, ORDER, BY


class AlterOrderBy(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + ORDER + BY
            + self._column_expr('expr')  # todo что за экспрешон
        ).set_parse_action(lambda term: {'modify_order_by': term['expr']})
