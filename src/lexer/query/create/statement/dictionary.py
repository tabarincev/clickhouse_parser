from pyparsing import *

from src.literals import DOT, LPAR, RPAR
from src.lexer.statement import Statement
from src.keywords import (
    CREATE, DICTIONARY, OR, REPLACE, IF, NOT, EXISTS, ON, CLUSTER, DEFAULT,
    EXPRESSION, HIERARCHICAL, INJECTIVE
)


class CreateDictionary(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            CREATE + DICTIONARY + Optional(OR + REPLACE('replace'))
            + Optional(IF + NOT + EXISTS('exists'))
            + Optional(pyparsing_common.identifier('db_name') + DOT)
            + pyparsing_common.identifier('dictionary_name')
            + Optional(
                ON + CLUSTER
                + pyparsing_common.identifier('cluster_name')
            )  # todo вынести в класс
            + LPAR
            + delimited_list(
                pyparsing_common.identifier('column_name')
                + pyparsing_common.identifier('column_type')
                
            )

        )

