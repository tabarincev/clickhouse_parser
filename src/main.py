from pyparsing import *


class AST:
    def __init__(self, ast: Dict):
        if not isinstance(ast, Dict):
            raise TypeError('Invalid type of ast: Dict expected')
        self.ast = ast

    @property
    def sql_string(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def rewrite_with_cte(sql: str) -> str:
        raise NotImplementedError()

    def _build_sql_string(self) -> str:
        raise NotImplementedError()


class SQLParser:
    def __init__(self, dialect='clickhouse'):
        if dialect.lower() not in ['clickhouse', 'mysql']:
            raise ValueError('Invalid SQL dialect')
        self.dialect = dialect

    def parse(self, sql: str) -> AST:
        raise NotImplementedError()
