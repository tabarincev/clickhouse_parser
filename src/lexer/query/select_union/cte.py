from pyparsing import ParserElement, MatchFirst
from pyparsing import delimited_list, pyparsing_common

from src.keywords import WITH, AS
from src.literals import LPAR, RPAR
from src.lexer.statement import Statement


class CommonTableExpr(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self):
        return MatchFirst([
            (
                WITH + pyparsing_common.identifier('identifier')
                + AS
                + LPAR + delimited_list(self._column_expr)('exprs') + RPAR
            ),
            (
                WITH + delimited_list(self._column_expr)('exprs')
            )
        ]).set_parse_action(
            lambda term: {
                'with': (
                    ({'identifier': term['identifier']}
                     if term.get('identifier') else {})
                    | {'exprs': term['exprs'].as_list()}
                )
            }
        )
        # return (
        #     WITH + delimited_list(self._column_expr)('exprs')
        # ).set_parse_action(
        #     lambda term: {'with': {'exprs': term['exprs'].as_list()}}
        # )
