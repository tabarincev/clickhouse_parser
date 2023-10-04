from abc import ABC

from pyparsing import pyparsing_common, delimited_list
from pyparsing import Literal, ParserElement, Optional, MatchFirst

from src.literals import string_literal, LPAR, RPAR, COMMA


def is_index_exists(arr: list, index: int) -> bool:
    return index < len(arr) - 1


class MetaSQLEngine(ABC):
    def __new__(cls, name, bases, attrs):
        if not attrs.get('engine_name'):
            raise KeyError('Expected a "engine_name" class field')

        if not isinstance(attrs['engine_name'], ParserElement):
            raise TypeError('Expected "ParserElement" type')

        return super().__new__(cls, name, bases, attrs)


class SQLEngineBase:
    @property
    def engine_args(self) -> ParserElement:
        return delimited_list(string_literal).set_parse_action(
            lambda term: {
                'args': ({
                    'host': term[0],
                    'database': term[1],
                    'user': term[2],
                    'password': term[3]
                } | ({'schema': term[4]}
                     if is_index_exists(term, 4) else {})
                  | ({'use_table_cache': term[5]}
                     if is_index_exists(term, 5) else {})
                )}
        )

    @property
    def notation(self) -> ParserElement:
        return (
            self.engine_name('engine')
            + LPAR
            + self.engine_args('args')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'database_engine': {
                    'name': term['engine'],
                    'args': term['args']
                }
            }
        )


class MaterializedMySQL(SQLEngineBase):
    __metaclass__ = MetaSQLEngine
    engine_name = Literal('MaterializedMySQL')


class MaterializedPostgreSQL(SQLEngineBase):
    __metaclass__ = MetaSQLEngine
    engine_name = Literal('MaterializedPostgreSQL')


class MySQL(SQLEngineBase):
    __metaclass__ = MetaSQLEngine
    engine_name = Literal('MySQL')


class Lazy:
    @property
    def notation(self) -> ParserElement:
        return (
            Literal('Lazy')
            + LPAR + pyparsing_common.integer('seconds') + RPAR
        ).set_parse_action(
            lambda term: {
                'database_engine': {
                    'name': 'Lazy',
                    'args': {'seconds': term['seconds']}
                }
            }
        )


class Atomic:
    @property
    def notation(self) -> ParserElement:
        return Optional(Literal('Atomic').set_parse_action(
            lambda term: {'database_engine': {'name': 'Atomic'}}
        ))


class SQLite:
    @property
    def notation(self) -> ParserElement:
        return (
            Literal('SQLite') + LPAR + string_literal('path') + RPAR
        ).set_parse_action(
            lambda term: {
                'database_engine': {
                    'name': 'SQLite',
                    'args': {'path': term['path']}
                }
            }
        )


class PostgreSQL(SQLEngineBase):
    __metaclass__ = MetaSQLEngine
    engine_name = Literal('PostgreSQL')


class Replicated:
    @property
    def notation(self) -> ParserElement:
        return (
            Literal('Replicated')
            + LPAR
            + string_literal('zoo_path') + COMMA
            + string_literal('shard_name') + COMMA
            + string_literal('replica_name')
            + RPAR
        ).set_parse_action(
            lambda term: {
                'database_engine': {
                    'name': 'Replicated',
                    'args': {
                        'zoo_path': term['zoo_path'],
                        'shard_name': term['shard_name'],
                        'replica_name': term['replica_name']
                    }
                }
            }
        )


class DatabaseEngine:
    @property
    def notation(self) -> ParserElement:
        return MatchFirst([
            MaterializedMySQL().notation,
            MaterializedPostgreSQL().notation,
            MySQL().notation,
            Lazy().notation,
            Atomic().notation,
            SQLite().notation,
            PostgreSQL().notation,
            Replicated().notation
        ])
