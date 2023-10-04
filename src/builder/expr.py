# from math import prod
# from itertools import product
# from collections import namedtuple
# from typing import List, Dict
#
#
# from src.builder.builder import BaseBuilder
# from src.builder.columns import ColumnBuilder
#
#
# FactorTerm = namedtuple('FactorTerm', ['neg', 'variable'])
#
#
# class BoolExprBuilder(BaseBuilder):
#     def __init__(self):
#         pass
#
#     def build(self, ast: Dict) -> str:
#         processed_ast = self._process_ast(ast)
#         # print(processed_ast, 'processed_ast')
#         factor_term = self._get_factor_term(processed_ast)
#
#         result = []
#
#         for el in [i.variable for i in factor_term]:
#             tmp = ' and '.join(el)
#             result.append(tmp)
#         return ' or '.join(result)
#
#     @staticmethod
#     def _get_factor_term(tree: List) -> List[FactorTerm]:
#         factor_term = list(product(*tree))
#         print(factor_term)
#         # print([
#         #     FactorTerm(
#         #         prod([i.neg for i in term]),
#         #         [j for i in term for j in i.variable]
#         #     )
#         #     for term in factor_term
#         # ])
#
#     def _process_ast(self, ast: Dict):
#         if isinstance(ast, Dict):
#             if 'or' in ast:
#                 or_res = []
#
#                 it = iter(ast['or'])
#                 or_res.extend(self._process_ast(next(it)))
#
#                 for op in it:
#                     terms = self._process_ast(op)
#                     or_res.extend(terms)
#                 return or_res
#
#             elif 'and' in ast:
#                 and_res = []
#
#                 it = iter(ast['and'])
#                 and_res.append(self._process_ast(next(it)))
#
#                 for op in it:
#                     term = self._process_ast(op)
#                     and_res.append(term)
#                 return and_res
#
#             elif any(key for key in ColumnBuilder().expected_keys):
#                 return [FactorTerm(1, [ColumnBuilder().build_full_expr(ast)])]
#             else:
#                 raise ValueError('Invalid structure of ast: {}'.format(ast))
#         else:
#             raise TypeError('Invalid ast type: "Dict" expected')
#
#
# ast = {
#     'or': [
#         {
#             'and': [
#                 {'column_term': {'column': 'a'}},
#                 {'column_term': {'column': 'b'}}
#             ]
#         },
#         {'column_term': {'column': 'c'}}
#     ]
# }
#
# print(BoolExprBuilder().build(ast))

from itertools import product
from collections import namedtuple
from typing import Dict, List
from math import prod


from src.builder.columns import ColumnBuilder


FactorTerm = namedtuple('FactorTerm', ['neg', 'variable'])


def build(tree: Dict):
    if isinstance(tree, dict):
        if 'or' in tree:
            or_res = []

            it = iter(tree['or'])
            or_res.extend(build(next(it)))

            for op in it:
                terms = build(op)
                or_res.extend(terms)
            return or_res

        elif 'and' in tree:
            and_res = []

            it = iter(tree['and'])
            and_res.append(build(next(it)))

            for op in it:
                term = build(op)
                and_res.append(term)
            return and_res

        elif any([key for key in ColumnBuilder().expected_keys]):
            return [FactorTerm(1, [ColumnBuilder().build_full_expr(tree)])]
        else:
            raise KeyError('Invalid key in tree: {}'.format(tree))
    else:
        raise TypeError('Invalid type of tree element: {}'.format(tree))


def process_tree(tree: Dict) -> List[FactorTerm]:
    product_tree = list(product(*tree))

    return [
        FactorTerm(
            prod([i.neg for i in term]),
            [j for i in term for j in i.variable]
        )
        for term in product_tree
    ]


def repr_factor_term(factor_term: List[FactorTerm]) -> str:
    result = []

    a = [i.variable for i in factor_term]

    for el in a:
        tmp = ' and '.join(el)
        result.append(tmp)
    return ' or '.join(result)


if __name__ == '__main__':
    tree = {'and': [{'or': [{'column_term': {'column': 'c'}}, {'column_term': {'column': 'm'}}]}, {'column_term': {'column': 'a'}}, {'column_term': {'column': 'g'}}]}

    tree_p = build(tree)
    tree_n = process_tree(tree_p)
    print(repr_factor_term(tree_n))

