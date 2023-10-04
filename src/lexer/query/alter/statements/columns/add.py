from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional, MatchFirst

from src.lexer.statement import Statement
from src.lexer.query.alter.clauses.codec import Codec
from src.keywords import ADD, COLUMN, IF, EXISTS, AFTER, FIRST


class AddColumn(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            ADD + COLUMN + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('column')
            + Optional(pyparsing_common.identifier('type'))
            + self._column_expr('default_expr')
            + Optional(Codec(self._column_expr).notation('codec'))
            + Optional(
                MatchFirst([
                    (
                        AFTER + pyparsing_common.identifier('column')
                    ).set_parse_action(
                        lambda term: {'after': term['column'][0]}
                    ),
                    FIRST.set_parse_action(
                        lambda term: {'first': True}
                    )
                ])('column_add_offset')
            )
        ).set_parse_action(
            lambda term: ({
                'add_column': (
                    {'column': term['column'][0]}
                    | {'default_expr': term['default_expr']}
                    | ({'type': term['type'][0]}
                       if term.get('type') else {})
                    | ({'codec': term['codec'][0]}
                       if term.get('codec') else {})
                    | ({'offset': term['colum_add_offset']}
                       if term.get('column_add_offset') else {})
                )
            })
        )
