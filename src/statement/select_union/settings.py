from pyparsing import *

from src.keywords import SETTINGS
from src.literals import EQ_SINGLE
from src.statement.statement import Statement


class Settings(Statement):
    @property
    def notation(self):
        return (
            SETTINGS + delimited_list(self.settings_expr)('settings')
        ).set_parse_action(
            lambda term: {'settings': term['settings'].as_list()}
        )

    @property
    def settings_expr(self):
        return (
            pyparsing_common.identifier('setting')
            + EQ_SINGLE
            + MatchFirst([
                pyparsing_common.identifier,
                pyparsing_common.number
            ])('value')
        ).set_parse_action(
             lambda term: {
                'setting': term['setting'],
                'value': term['value']
             }
        )


# {'settings': [{'setting': 'a', 'value': 1}, {'setting': 'b', 'value': 'c'}]}
