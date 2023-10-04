from pyparsing import ParserElement
from pyparsing import delimited_list, pyparsing_common

from src.literals import EQ_SINGLE
from src.lexer.statement import Statement
from src.keywords import MODIFY, SETTINGS


class ModifySettings(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + SETTINGS
            + delimited_list((
                pyparsing_common.identifier('setting')
                + EQ_SINGLE
                + pyparsing_common.identifier('value')
            ).set_parse_action(
                lambda term: {
                    'setting': {
                        'param': term['setting'][0],
                        'value': term['value'][0]
                    }
                }
            ))('settings_list')
        ).set_parse_action(
            lambda term: {'modify_setting': term['settings_list'].as_list()}
        )
