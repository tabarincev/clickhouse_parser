from pyparsing import delimited_list
from pyparsing import Optional, ParserElement

from src.literals import COMMA
from src.lexer.statement import Statement
from src.keywords import OFFSET, LIMIT, WITH, TIES, BY


class BaseLimit:
    def __init__(self, columns_expr: ParserElement):
        self._column_expr = columns_expr

    @property
    def limit_expr(self):
        return (
            self._column_expr('value')
            + Optional((COMMA | OFFSET) + self._column_expr('offset'))
        ).set_parse_action(
            lambda term: ({
                'limit_expr': (
                    {'value': term['value']}
                    | ({'offset': term['offset']}
                       if term.get('offset') else {})
                )
            })
        )


class Limit(BaseLimit, Statement):
    def __init__(self, column_expr: ParserElement):
        super().__init__(column_expr)

    @property
    def notation(self):
        return (
            LIMIT + self.limit_expr('expr')
            + Optional((WITH + TIES)('with_ties'))
        ).set_parse_action(
            lambda term: {
                'limit': {
                    'expr': term['expr'],
                    'with_ties': True if term.get('with_ties') else False
                }
            }
        )


class LimitBy(BaseLimit, Statement):
    def __init__(self, column_expr: ParserElement):
        super().__init__(column_expr)

    @property
    def notation(self):
        return (
            LIMIT + self.limit_expr('expr')
            + BY + delimited_list(self._column_expr)('by_expr')
        ).set_parse_action(
            lambda term: {
                'limit_by': (
                    term['expr']
                    | {'by_expr': term['by_expr'].as_list()}
                )
            }
        )
