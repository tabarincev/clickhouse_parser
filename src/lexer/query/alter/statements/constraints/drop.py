from pyparsing import ParserElement
from pyparsing import pyparsing_common
from src.lexer.statement import Statement
from src.keywords import DROP, CONSTRAINT


class DropConstraint(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            DROP + CONSTRAINT + pyparsing_common.identifier('constraint_name')
        ).set_parse_action(
            lambda term: {
                'drop_constraint': {
                    'constraint_name': term['constraint_name'][0]
                }
            }
        )
