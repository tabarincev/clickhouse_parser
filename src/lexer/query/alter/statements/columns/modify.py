from pyparsing import pyparsing_common
from pyparsing import ParserElement, MatchFirst, Optional

from src.lexer.statement import Statement
from src.lexer.query.alter.clauses.ttl import TTL
from src.lexer.query.alter.clauses.codec import Codec
from src.keywords import MODIFY, ALTER, COLUMN, IF, EXISTS, TYPE, AFTER, FIRST


class ModifyColumn(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return MatchFirst([
            (
                MODIFY + COLUMN + Optional(IF + EXISTS)
                + pyparsing_common.identifier
                + Optional(pyparsing_common.identifier('column_type'))
                # + default_expr # todo
                + Optional(Codec(self._column_expr).notation)
                + Optional(TTL(self._column_expr).notation)
                + Optional(
                    MatchFirst([
                        AFTER + pyparsing_common.identifier,
                        FIRST
                    ])
                )
            ),
            (
                ALTER + COLUMN + Optional(IF + EXISTS)
                + pyparsing_common.identifier
                + TYPE
                + Optional(pyparsing_common.identifier('column_type'))
                # + default_expr # todo
                + Optional(Codec(self._column_expr).notation)
                + Optional(TTL(self._column_expr).notation)
                + Optional(
                    MatchFirst([  # todo вынести в clauses
                        AFTER + pyparsing_common.identifier,
                        FIRST
                    ])
                )
            )
        ])
