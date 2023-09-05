from pyparsing import *


class AST:
    def __init__(self, ast: Dict):
        if not isinstance(ast, Dict):
            raise TypeError('Invalid type of ast: Dict expected')
        self.ast = ast

    @property
    def sql_string(self):
        return self._build_sql_string()

    @staticmethod
    def rewrite_with_cte(sql: str) -> str:
        return ''

    def _build_sql_string(self):
        pass


class SQLParser:
    def __init__(self, dialect='clickhouse'):
        if dialect.lower() not in ['clickhouse', 'postgresql']:
            raise ValueError('Invalid SQL dialect')
        self.dialect = dialect

    def parse(self, sql: str) -> AST:
        return AST({})
