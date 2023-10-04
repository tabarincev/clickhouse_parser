from pyparsing import pyparsing_common
from pyparsing import ParserElement, MatchFirst

from src.lexer.statement import Statement
from src.keywords import (
    MODIFY, COLUMN, REMOVE, DEFAULT, ALIAS,
    MATERIALIZED, CODEC, COMMENT, TTL
)


class ModifyRemoveColumn(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            MODIFY + COLUMN
            + pyparsing_common.identifier('column')
            + REMOVE
            + MatchFirst([
                DEFAULT,
                ALIAS,
                MATERIALIZED,
                CODEC,
                COMMENT,
                TTL
            ])('remove_type')
        ).set_parse_action(
            lambda term: ({
                'modify_column': (
                    {'column': term['column'][0]}
                    | {'remove': term['remove_type']}
                )
            })
        )
