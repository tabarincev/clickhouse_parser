from ast import literal_eval

from pyparsing import infix_notation, opAssoc
from pyparsing import Forward, Optional, ParserElement, MatchFirst, Group


from src.columns import ColumnExpr
from src.keywords import UNION, ALL, DISTINCT, EXCEPT, INTERSECT
from src.utils.infix_processing import UnionOperator, BinaryOperator

from src.statement.statement import Statement
from src.statement.select_union.select import Select
from src.statement.select_union.into_outfile import IntoOutfile
from src.statement.select_union.format import Format


class SelectUnion(Statement):
    def __init__(self):
        self._column_expr = Forward()

        self._join_expr = Forward()
        self._window_expr = Forward()

        self._select_union_statement = Forward()

    @property
    def select_union_term(self) -> ParserElement:
        return (
            Select(
                ColumnExpr(
                    self._column_expr,
                    self._select_union_statement
                ).notation
            ).notation
        )

    @property
    def select_union_statement(self) -> ParserElement:
        self._select_union_statement << infix_notation(
            self.select_union_term,
            [
                (
                    Group(UNION + Optional(DISTINCT | ALL)),
                    2, opAssoc.LEFT, UnionOperator
                ),
                (
                    MatchFirst([EXCEPT, INTERSECT]),
                    2, opAssoc.LEFT, BinaryOperator
                )
            ]
        )
        return self._select_union_statement

    @property
    def notation(self) -> ParserElement:
        return (
            self.select_union_statement('select')
            + Optional(IntoOutfile().notation('insert_outfile'))
            + Optional(Format().notation('format'))
        ).set_parse_action(
            lambda term: {
                'select_union_statement': (
                    literal_eval(str(term['select']))
                    | term.get('insert_outfile', {})
                    | term.get('format', {})
                )
            }
        )


if __name__ == '__main__':
    s = SelectUnion().notation
    print(s.parse_string('select distinct func(distinct 1) union all select bi format JSONEachRow', parse_all=True))

        # return (
        #     Optional(CommonTableExpr(self._columns_expr).notation)
        #     + Select(self._columns_expr).notation
        #     + Optional(From(self._join_expr, self._column_expr, self._columns_expr).notation)  # todo
        #     + Optional(ArrayJoin(self._columns_expr).notation)
        #     + Optional(Window(self._column_expr, self._columns_expr, self._window_expr).notation)
        #     + Optional(PreWhere(self._column_expr).notation)
        #     + Optional(Where(self._column_expr).notation)
        #     + Optional(GroupBy(self._columns_expr).notation)
        #     + Optional(Having(self._column_expr).notation)
        #     + Optional(OrderBy(self._column_expr).notation)  # todo
        #     + Optional(LimitBy(self._column_expr).notation)
        #     + Optional(Limit(self._column_expr).notation)
        #     + Optional(Settings().settings_expr)
        #     + Optional(Format().notation)
        # )
