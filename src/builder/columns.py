from math import prod
from itertools import product
from typing import Dict, List
from collections import namedtuple

from src.builder.builder import BaseBuilder


FactorTerm = namedtuple('FactorTerm', ['neg', 'variable'])


class BooleanBuilder(BaseBuilder):
    def __init__(self):
        self.column_builder = ColumnBuilder()

    def build(self, tree: Dict) -> str:
        tree_p = self.build_tree(tree)
        tree_n = self.process_tree(tree_p)
        return self.repr_factor_term(tree_n)

    def build_tree(self, tree: Dict):
        if isinstance(tree, dict):
            if 'or' in tree:
                or_res = []

                it = iter(tree['or'])
                or_res.extend(self.build_tree(next(it)))

                for op in it:
                    terms = self.build_tree(op)
                    or_res.extend(terms)
                return or_res

            elif 'and' in tree:
                and_res = []

                it = iter(tree['and'])
                and_res.append(self.build_tree(next(it)))

                for op in it:
                    term = self.build_tree(op)
                    and_res.append(term)
                return and_res

            elif any([key for key in self.column_builder.expected_keys]):
                return [FactorTerm(1, [self.column_builder.build_full_expr(tree)])]

            else:
                raise KeyError('Invalid key in tree: {}'.format(tree))
        else:
            raise TypeError('Invalid type of tree element: {}'.format(tree))

    @staticmethod
    def process_tree(tree: Dict) -> List[FactorTerm]:
        product_tree = list(product(*tree))

        return [
            FactorTerm(
                prod([i.neg for i in term]),
                [j for i in term for j in i.variable]
            )
            for term in product_tree
        ]

    @staticmethod
    def repr_factor_term(factor_term: List[FactorTerm]) -> str:
        result = []

        a = [i.variable for i in factor_term]

        for el in a:
            tmp = ' and '.join(el)
            result.append(tmp)
        return ' or '.join(result)


class ColumnBuilder:  # todo BaseBuilder
    expected_keys = (
        'case_term',
        'cast_term',
        'date_term',
        'extract_term',
        'interval_term',
        'substring_term',
        'timestamp_term',
        'trim_term',
        'window_function_term',
        'window_function_target_term',
        'function_term',
        'lambda_function_term',
        'asterisk_term',
        'column_term',
        'literal_term',
        'select_union_statement',
        'parens_term',
        'tuple_term',
        'array_term'
    )

    def build_full_expr(self, ast: Dict) -> str:
        result = ''

        if isinstance(ast, Dict):
            if not ast:
                return result

            # if any(['or', 'and' in ast]):
            #     result += self.build_boolean_op(ast)

            if 'case_term' in ast:
                result += self.build_case(ast)

            elif 'cast_term' in ast:
                pass

            elif 'date_term' in ast:
                result += self.build_date(ast)

            elif 'extract_term' in ast:
                result += self.build_extract(ast)

            elif 'interval' in ast:
                result += self.build_interval(ast)

            elif 'substring' in ast:
                pass

            elif 'timestamp' in ast:
                result += self.build_timestamp(ast)

            elif 'trim' in ast:
                result += self.build_trim(ast)

            elif 'window_function' in ast:
                result += self.build_window_function(ast)

            elif 'window_function_target' in ast:
                result += self.build_window_function_target(ast)

            elif 'function_term' in ast:
                result += self.build_function(ast)

            elif 'lambda_function' in ast:
                result += self.build_lambda_function(ast)

            elif 'asterisk_term' in ast:
                result += self.build_asterisk(ast)

            elif 'column_term' in ast:
                result += self.build_column_identifier(ast)

            elif 'literal_term' in ast:
                result += self.build_literal(ast)

            elif 'select_union_statement' in ast:
                pass

            elif 'parens_term' in ast:
                result += self.build_parens(ast)

            elif 'tuple_term' in ast:
                result += self.build_tuple(ast)

            elif 'array_term' in ast:
                result += self.build_array(ast)

            elif 'index_term' in ast:
                result += self.build_index(ast)
            else:
                raise ValueError(
                    'Invalid structure of AST - {keys} expected'.format(
                        keys=', '.join(self.expected_keys)
                    )
                )
        else:
            raise TypeError('Invalid type in SQL AST - "Dict" expected')
        return result

    # def build_boolean_op(self, tree: Dict) -> str:
    #     tree_p = self._build_bool_tree(tree)
    #     tree_n = self._process_tree(tree_p)
    #     return self._repr_factor_term(tree_n)

    def _build_bool_tree(self, tree: Dict):
        if isinstance(tree, dict):
            if 'or' in tree:
                or_res = []

                it = iter(tree['or'])
                or_res.extend(self._build_bool_tree(next(it)))

                for op in it:
                    terms = self._build_bool_tree(op)
                    or_res.extend(terms)
                return or_res

            elif 'and' in tree:
                and_res = []

                it = iter(tree['and'])
                and_res.append(self._build_bool_tree(next(it)))

                for op in it:
                    term = self._build_bool_tree(op)
                    and_res.append(term)
                return and_res

            elif any([key for key in ColumnBuilder().expected_keys]):
                return [FactorTerm(1, [ColumnBuilder().build_full_expr(tree)])]
            else:
                raise KeyError('Invalid key in tree: {}'.format(tree))
        else:
            raise TypeError('Invalid type of tree element: {}'.format(tree))

    def _process_tree(self, tree: Dict) -> List[FactorTerm]:
        product_tree = list(product(*tree))

        return [
            FactorTerm(
                prod([i.neg for i in term]),
                [j for i in term for j in i.variable]
            )
            for term in product_tree
        ]

    def _repr_factor_term(self, factor_term: List[FactorTerm]) -> str:
        result = []

        a = [i.variable for i in factor_term]

        for el in a:
            tmp = ' and '.join(el)
            result.append(tmp)
        return ' or '.join(result)

    def build_case(self, ast: Dict) -> str:
        if 'case_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "case_term" key'
            )
        return 'case {identifier} {cases} {else_expr} end'.format(
            identifier=ast['case_term'].get('identifier', ''),
            else_expr=ast['case_term'].get('else', ''),
            cases=[
                'when {when} then {then}'.format(
                    when=self.build_full_expr(case['case']['when']),
                    then=self.build_full_expr(case['case']['then'])
                ) for case in ast['case_term']['cases']
            ]
        )

    def build_cast(self, ast: Dict) -> str:
        return ''

    @staticmethod
    def build_date(ast: Dict) -> str:
        if 'date_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "date_term" key'
            )
        return 'date "{date}"'.format(date=ast['date_term'])

    def build_extract(self, ast: Dict) -> str:
        if 'extract_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "extract_term" key'
            )
        return 'extract({extract_type} from {extract_from})'.format(
            extract_type=ast['extract_term']['extract_type'],
            extract_from=self.build_full_expr(ast['extract_term']['extract_from'])
        )

    def build_interval(self, ast: Dict) -> str:
        if 'interval_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "interval_term" key'
            )
        return 'interval {expr} {date_type}'.format(
            expr=self.build_full_expr(ast['interval_term']['expr']),
            date_type=ast['interval_term']['date_type']
        )

    def build_substring(self, ast: Dict) -> str:
        return ''

    @staticmethod
    def build_timestamp(ast: Dict) -> str:
        if 'timestamp_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "timestamp_term" key'
            )
        return 'timestamp "{timestamp_string}"'.format(
            timestamp_string=ast['timestamp_term']
        )

    def build_trim(self, ast: Dict) -> str:
        if 'trim_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "trim_term" key'
            )
        return 'trim({trim_type} "{string}" from {expr})'.format(
            trim_type=ast['trim_term']['type'],
            string=ast['trim_term']['string'],
            expr=self.build_full_expr(ast['trim_term']['from_expr'])
        )

    def build_window_function(self, ast: Dict) -> str:
        return ''

    def build_window_function_target(self, ast: Dict) -> str:
        return ''

    def build_function(self, ast: Dict) -> str:
        if 'function_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "function_term" key'
            )
        return '{function_name}({distinct}{args})'.format(
            function_name=ast['function_term']['name'],
            distinct='distinct ' if ast['function_term'].get('distinct') else '',
            args=', '.join([
                self.build_full_expr(arg)
                for arg in ast['function_term']['args']
            ])
        )

    def build_lambda_function(self, ast: Dict) -> str:
        return ''

    @staticmethod
    def build_asterisk(ast: Dict) -> str:
        if 'asterisk_term' not in ast:
            raise ValueError(
                 'Invalid structure of SQL AST - Expected "asterisk_term" key'
            )
        return '{table}*'.format(
            table='{table}.'.format(
                table=ast['asterisk_term']['table']
            ) if ast['asterisk_term'].get('table') else '',
        )

    @staticmethod
    def build_column_identifier(ast: Dict) -> str:
        if 'column_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "column_term" key'
            )
        return '{database}{table}{column}'.format(
            database='{database}.'.format(
                database=ast['column_term']['database']
            ) if ast['column_term'].get('database') else '',
            table='{table}.'.format(
                table=ast['column_term']['table']
            ) if ast['column_term'].get('table') else '',
            column=ast['column_term']['column']
        )

    @staticmethod
    def build_literal(ast: Dict) -> str:
        if 'literal_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "literal_term" key'
            )
        if 'numeric' in ast['literal_term']:
            return '{num}'.format(
                num=ast['literal_term']['numeric']
            )
        elif 'string' in ast['literal_term']:
            return '{string}'.format(
                string=ast['literal_term']['string']
            )
        elif 'literal' in ast['literal_term']:
            return 'NULL'
        else:
            raise ValueError(
                'Invalid structure of SQL AST: Expected {} keys'.format(
                    ', '.join(['numeric', 'string', 'literal'])
                )
            )

    def build_select_union_statement(self, ast: Dict) -> str:
        pass

    def build_parens(self, ast: Dict) -> str:
        if 'parens_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "parens_term" key'
            )
        return '({expr})'.format(
            expr=self.build_full_expr(ast['parens_term'])
        )

    def build_tuple(self, ast: Dict) -> str:
        if 'tuple_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "tuple_term" key'
            )
        return '({exprs})'.format(
            exprs=', '.join([
                self.build_full_expr(arg)
                for arg in ast['tuple_term']['args']
            ])
        )

    def build_array(self, ast: Dict) -> str:
        if 'array_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "array_term" key'
            )
        return '[{exprs}]'.format(
            exprs=', '.join([
                self.build_full_expr(arg)
                for arg in ast['array_term']['args']
            ])
        )

    def build_index(self, ast: Dict) -> str:
        if 'index_term' not in ast:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "index_term" key'
            )
        return '{term}[{index}]'.format(
            term=self.build_full_expr(ast['index_term']['term']),
            index=self.build_full_expr(ast['index_term']['index'])
        )


if __name__ == '__main__':
    c = ColumnBuilder().build_full_expr({'and': [{'or': [{'column_term': {'column': 'c'}}, {'column_term': {'column': 'm'}}]}, {'column_term': {'column': 'a'}}, {'column_term': {'column': 'g'}}]})