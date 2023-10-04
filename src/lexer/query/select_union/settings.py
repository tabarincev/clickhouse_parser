from pyparsing import ParserElement, MatchFirst
from pyparsing import delimited_list, pyparsing_common

from src.keywords import SETTINGS
from src.literals import EQ_SINGLE
from src.lexer.statement import Statement


class Settings(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            SETTINGS + delimited_list(self.settings_expr)('settings_list')
        ).set_parse_action(
            lambda term: {'settings': term['settings_list'].as_list()}
        )

    @property
    def settings_expr(self) -> ParserElement:
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
