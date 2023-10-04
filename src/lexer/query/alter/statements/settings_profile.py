from pyparsing import *

from src.lexer.statement import Statement
from src.keywords import (
    ALTER, SETTINGS, PROFILE, IF, EXISTS, TO, ON, CLUSTER, RENAME,
)


class AlterSettingsProfile(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            ALTER + SETTINGS + PROFILE + Optional(IF + EXISTS)
            + TO + delimited_list(
                pyparsing_common.identifier('name')
                + Optional(
                    ON + CLUSTER
                    + pyparsing_common.identifier('cluster')
                )
                + Optional(
                    RENAME + TO
                    + pyparsing_common.identifier('rename_to')
                )
            )
            # todo
        )