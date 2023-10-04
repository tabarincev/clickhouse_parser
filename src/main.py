from pyparsing import *


class AST:
    def __init__(self, ast: dict):
        if not isinstance(ast, dict):
            raise TypeError(
                'Invalid type of ast - {}: Dict expected'.format(type(ast))
            )
        self.ast = ast

    @property
    def sql_string(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def rewrite_with_cte(sql: str) -> str:
        raise NotImplementedError()

    def _build_sql_string(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def get_values_by_key(key, ast):
        if hasattr(ast, 'items'):
            for k, v in ast.items():
                if k == key:
                    yield v

                if isinstance(v, dict):
                    for result in AST.get_values_by_key(key, v):
                        yield result

                elif isinstance(v, list):
                    for d in v:
                        for result in AST.get_values_by_key(key, d):
                            yield result

    def _get_joins(self) -> list:
        all_list_joins = list(self.get_values_by_key('joins', self.ast))
        # print(all_list_joins)
        for join_term in all_list_joins:
            print(join_term)
            print('---' * 100)

        return all_list_joins

    def get_tables(self, formatted=False) -> set:
        if not formatted:
            return set(self.get_values_by_key('table_identifier', self.ast))
        return set(
            map(
                lambda term: '{database}{table}'.format(
                    database='{}.'.format(term.get('database', '')),
                    table=term['table']),
                self.get_values_by_key('table_identifier', self.ast)
            )
        )


class SQLParser:
    def __init__(self, dialect='clickhouse'):
        if dialect.lower() not in ['clickhouse', 'mysql']:
            raise ValueError('Invalid SQL dialect')
        self.dialect = dialect

    def parse(self, sql: str) -> AST:
        raise NotImplementedError()


ast_sql ={'select_union_statement': {'select': {'columns': [{'literal_term': {'numeric': 1}}]}, 'from': {'join_expr': {'select': {'columns': [{'literal_term': {'numeric': 2}}]}, 'from': {'join_expr': {'table_identifier': {'database': 'ab', 'table': 'main_metrics'}, 'joins': [{'operator': {'join_type': 'inner'}, 'table_to_join': {'select': {'columns': [{'literal_term': {'numeric': 3}}]}, 'from': {'join_expr': {'table_identifier': {'database': 'ab', 'table': 'experiments'}}}, 'alias': 'exps'}, 'constraint': {'type': 'using', 'exprs': [{'column_term': {'column': 'experiment_group_id'}}, {'column_term': {'column': 'experiment_group_id_type'}}]}}, {'operator': {'join_type': 'inner'}, 'table_to_join': {'table_identifier': {'database': 'ab', 'table': 'main'}}, 'constraint': {'type': 'on', 'exprs': [{'=': [{'column_term': {'table': 'main', 'column': 'id'}}, {'column_term': {'table': 'experiments', 'column': 'id'}}]}]}}]}}, 'alias': 'mm', 'joins': [{'operator': {'join_type': 'inner'}, 'table_to_join': {'table_identifier': {'database': 'ab2', 'table': 'main2'}}, 'constraint': {'type': 'on', 'exprs': [{'=': [{'column_term': {'table': 'main2', 'column': 'id'}}, {'column_term': {'table': 'experiments2', 'column': 'id'}}]}]}}]}}}}
ast_obj = AST(ast=ast_sql)
print(ast_obj.get_tables(formatted=True))
