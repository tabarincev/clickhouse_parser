from pyparsing import *


from src.lexer.statement import Statement
from src.literals import EQ_SINGLE, string_literal
from src.lexer.query.create.engines import DatabaseEngine

from src.keywords import (
    CREATE, DATABASE, IF, NOT, EXISTS,
    ON, CLUSTER, ENGINE, COMMENT
)


class CreateDatabase(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            CREATE + DATABASE + Optional(IF + NOT + EXISTS('exists'))
            + pyparsing_common.identifier('database_name')
            + Optional(
                ON + CLUSTER
                + pyparsing_common.identifier('cluster_name')
            )
            + Optional(
                ENGINE + EQ_SINGLE + DatabaseEngine().notation('db_engine')
            )
            + Optional(
                COMMENT + string_literal('comment')
            )
        ).set_parse_action(
            lambda term: {
                'create': {
                    'database': (
                        {'name': term['database_name']}
                        | ({'if_not_exists': True}
                           if term.get('exists') else {})
                        | ({'on_cluster': term['cluster_name']}
                           if term.get('cluster_name') else {})
                        | (term['db_engine'][0]
                           if term.get('db_engine') else {})
                        | ({'comment': term['comment']}
                           if term.get('comment') else {})
                    )
                }
            }
        )
