from pyparsing import *

from src.literals import DOT
from src.lexer.statement import Statement

from src.keywords import (
    ALTER, ROW, POLICY, IF, EXISTS, ON, CLUSTER,
    RENAME, TO, AS, RESTRICTIVE, PERMISSIVE, FOR,
    SELECT, USING, ALL, EXCEPT, NONE
)


class AlterRowPolicy(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            ALTER + Optional(ROW) + POLICY + Optional(IF + EXISTS)
            + delimited_list(
                pyparsing_common.identifier('name')
                + Optional(
                    ON + CLUSTER
                    + pyparsing_common.identifier('cluster')
                    + ON
                    + Optional(pyparsing_common.identifier('database') + DOT)
                    + pyparsing_common.identifier('table')
                    + Optional(
                        RENAME + TO
                        + pyparsing_common.identifier('rename_to')
                    )
                )
            )
            + Optional(AS + MatchFirst([RESTRICTIVE, PERMISSIVE]))
            + Optional(FOR + SELECT)
            + Optional(USING + delimited_list(self._column_expr | NONE))
            + Optional(
                TO + delimited_list(pyparsing_common.identifier('role'))
                + (ALL | EXCEPT + ALL)
                + delimited_list(pyparsing_common.identifier('role'))
            )
        )
