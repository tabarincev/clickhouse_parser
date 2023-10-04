from pyparsing import *


from src.lexer.statement import Statement
from src.keywords import (
    ALTER, ROLE, IF, EXISTS, ON, CLUSTER, RENAME, TO, SETTINGS
)


class AlterRole(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            ALTER + ROLE + Optional(IF + EXISTS)
            + delimited_list(
                pyparsing_common.identifier('role_name')
                + Optional(
                    ON + CLUSTER
                    + pyparsing_common.identifier('cluster_name')
                )  # on_cluster clause
                + Optional(
                    RENAME + TO
                    + pyparsing_common.identifier('rename_to')
                )
            )
            + Optional(
                SETTINGS
            )
        )
