import sys
from ast import literal_eval
from functools import lru_cache

from pyparsing import infix_notation, opAssoc
from pyparsing import Forward, Optional, ParserElement, MatchFirst, Group


from src.columns import ColumnExpr
from src.keywords import UNION, ALL, DISTINCT, EXCEPT, INTERSECT

from src.lexer.statement import Statement
from src.lexer.query.select_union.cte import CommonTableExpr
from src.lexer.query.select_union.select import Select
from src.lexer.query.select_union.from_ import From
from src.lexer.query.select_union.array_join import ArrayJoin
from src.lexer.query.select_union.window import Window
from src.lexer.query.select_union.prewhere import PreWhere
from src.lexer.query.select_union.where import Where
from src.lexer.query.select_union.group_by import GroupBy
from src.lexer.query.select_union.having import Having
from src.lexer.query.select_union.order_by import OrderBy
from src.lexer.query.select_union.limit import LimitBy, Limit
from src.lexer.query.select_union.settings import Settings
from src.lexer.query.select_union.into_outfile import IntoOutfile
from src.lexer.query.select_union.format import Format
from src.lexer.query.select_union.window import WindowExpr

from src.utils.infix_processing import UnionOperator, BinaryOperator

sys.setrecursionlimit(3000)
ParserElement.enable_left_recursion()


class SelectUnion(Statement):
    def __init__(self):
        self._column_expr = Forward()
        self._join_expr = Forward()
        self._table_expr = Forward()
        self._window_expr = Forward()
        self._select_union_statement = Forward()

        self._window_expr_clause = WindowExpr(
            window_expr=self._window_expr,
            column_expr=ColumnExpr(
                column_expr=self._column_expr,
                select_union_statement=self._select_union_statement,
                window_expr=self._window_expr
            ).notation
        ).notation

        self._column_expr_clause = ColumnExpr(
            column_expr=self._column_expr,
            select_union_statement=self._select_union_statement,
            window_expr=WindowExpr(
                window_expr=self._window_expr,
                column_expr=ColumnExpr(
                    column_expr=self._column_expr,
                    select_union_statement=self._select_union_statement,
                    window_expr=self._window_expr
                ).notation
            ).notation
        ).notation

    @property
    @lru_cache
    def select_union_term(self) -> ParserElement:
        return (
            Optional(
                CommonTableExpr(self._column_expr_clause).notation('cte')
            )
            + Select(self._column_expr_clause).notation('select')
            + Optional(
                From(
                    join_expr=self._join_expr,
                    column_expr=self._column_expr_clause,
                    table_expr=self._table_expr,
                    select_union_statement=self._select_union_statement
                ).notation('from')
            )
            + Optional(
                ArrayJoin(self._column_expr_clause).notation('array_join')
            )
            + Optional(
                Window(
                    window_expr=self._window_expr,
                    column_expr=self._column_expr
                ).notation('window')
            )
            + Optional(
                PreWhere(self._column_expr_clause).notation('prewhere')
            )
            + Optional(
                Where(self._column_expr_clause).notation('where')
            )
            + Optional(
                GroupBy(self._column_expr_clause).notation('group_by')
                + Optional(
                    Having(self._column_expr_clause).notation('having')
                )
            )
            + Optional(
                OrderBy(self._column_expr_clause).notation('order_by')
            )
            + Optional(
                LimitBy(self._column_expr_clause).notation('limit_by')
            )
            + Optional(
                Limit(self._column_expr_clause).notation('limit')
            )
            + Optional(Settings().notation('settings'))
        ).set_parse_action(
            lambda term: literal_eval(str(
                term.get('cte', {})
                | term['select']
                | term.get('from', {})
                | term.get('array_join', {})
                | term.get('window', {})
                | term.get('prewhere', {})
                | term.get('where', {})
                | term.get('group_by', {})
                | term.get('having', {})
                | term.get('order_by', {})
                | term.get('limit_by', {})
                | term.get('limit', {})
                | term.get('settings', {})
            ))
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
    @lru_cache
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
    import datetime
    start = datetime.datetime.now()
    print(s.parse_string("""
    select 1
from
(
    select 2
    from ab.main_metrics
    inner join (
        select 3
        from ab.experiments
    ) as exps using experiment_group_id, experiment_group_id_type
    inner join ab.main on main.id=experiments.id
) as mm


""", parse_all=True))
    print(datetime.datetime.now() - start)

a = [
    {
        'table1': 'ab.main_metrics',
        'table2': 'ab.experiments',
        'join_condition': 'using',
        'join_fields': ['experiment_group_id', 'experiment_group_id_type']
    },
    {
        'table1': 'ab.experiments',
        'table2': 'ab.main',
        'join_condition': 'on',
        'join_fields': {'ab.experiments': ['id'], 'ab.main': ['id']}
    }
]