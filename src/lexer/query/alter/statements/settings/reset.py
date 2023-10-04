from pyparsing import ParserElement
from pyparsing import delimited_list, pyparsing_common

from src.lexer.statement import Statement
from src.keywords import RESET, SETTINGS


class ResetSettings(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            RESET + SETTINGS
            + delimited_list(
                pyparsing_common.identifier('setting').set_parse_action(
                    lambda term: {'setting': term['value'][0]}
                )
            )('settings_list')
        ).set_parse_action(
            lambda term: {'reset_settings': term['settings_list'].as_list()}
        )
