from pyparsing import pyparsing_common
from pyparsing import ParserElement, Optional

from src.lexer.statement import Statement
from src.keywords import CLEAR, COLUMN, IF, EXISTS, IN, PARTITION


class ClearColumn(Statement):
    def __init__(self, column_expr: ParserElement):
        self._column_expr = column_expr

    @property
    def notation(self) -> ParserElement:
        return (
            CLEAR + COLUMN
            + Optional(IF + EXISTS('exists'))
            + pyparsing_common.identifier('column')
            + IN + PARTITION + self._column_expr('partition')
        ).set_parse_action(
            lambda term: ({
                'clear_column': (
                    {'column': term['column'][0]}
                    | {'partition': term['partition']}
                    | ({'if_exists': True}
                       if term.get('exists') else {})
                )
            })
        )


if __name__ == '__main__':
    from src.columns import ColumnExpr
    from pyparsing import Forward

    expr = Forward()
    select = Forward()

    cc = ClearColumn(
        ColumnExpr(
            column_expr=expr,
            select_union_statement=select
        ).notation
    ).notation

    print(cc.parse_string('clear column name_col in partition "2023-09-12"'))