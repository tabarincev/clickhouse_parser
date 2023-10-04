from pyparsing import ParserElement
from pyparsing import pyparsing_common
from src.lexer.statement import Statement
from src.keywords import ADD, CONSTRAINT, CHECK


class AddConstraint(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            ADD + CONSTRAINT + pyparsing_common.identifier('constraint_name')
            + CHECK + self._column_expr('check_expr')
        ).set_parse_action(
            lambda term: {
                'add_constraint': {
                    'constraint_name': term['constraint_name'][0],
                    'check': term['check_expr']
                }
            }
        )
