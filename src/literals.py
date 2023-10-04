import pyparsing
import src.keywords as keyword

from src.keywords import *
from pyparsing import Literal, Suppress, MatchFirst, Word, CaselessKeyword
from pyparsing import alphas, alphanums, pyparsing_common, Optional, QuotedString


UNARY, BINARY, TERNARY = 1, 2, 3

string_literal = MatchFirst([
    pyparsing.dbl_quoted_string().set_parse_action(
        lambda term: {'string_literal': term[0][1:-1], 'quote': 'dbl'}
    ),
    pyparsing.sgl_quoted_string().set_parse_action(
        lambda term: {'string_literal': term[0][1:-1], 'quote': 'sgl'}
    ),
    QuotedString('`').set_parse_action(
        lambda term: {'string_literal': term[0], 'quote': 'apos'}
    )


])
#
# keywords = MatchFirst((
#     CaselessKeyword(keyword) for keyword in dir(keyword)
#     if not keyword.startswith('__') and keyword == keyword.upper()
# ))
#

keywords = MatchFirst(
    (UNION, ALL, INTERSECT, EXCEPT, COLLATE, ASC, DESC, ON, USING,
     INNER, CROSS, LEFT, RIGHT, OUTER, FULL, JOIN, AS, SAMPLE,
     NOT, SELECT, DISTINCT, FROM, PREWHERE, WHERE, GROUP, BY, HAVING, ORDER,
     LIMIT, OFFSET, CAST, NULL, IS, BETWEEN, ELSE, END, PARTITION, ARRAY,
     CASE, WHEN, THEN, EXISTS, COLLATE, IN, LIKE, WINDOW, IF, FOR, AND, OR
     )
)


identifier_word = Word(alphas + '_@#', alphanums + '@$#_')
identifier = ~keywords + identifier_word.copy()
# identifier = ~keywords + identifier_word.copy()

database = identifier_word.copy()
table = identifier_word.copy()
column = identifier_word.copy()

function_name = identifier_word.copy()

LPAR, RPAR = map(Suppress, '()')
LBRACKET = Suppress('[')
RBRACKET = Suppress(']')

COMMA = Literal(',')
DOT = Literal('.')

DASH = Literal('-')
PLUS = Literal('+')
ASTERISK = Literal('*')
SLASH = Literal('/')
PERCENT = Literal('%')
CONCAT = Literal('||')
EQ_DOUBLE = Literal('==')
EQ_SINGLE = Literal('=')
NOT_EQ = MatchFirst([Literal('!='), Literal('<>')])
LE = Literal('<=')
GE = Literal('>=')
LT = Literal('<')
GT = Literal('>')
ARROW = Literal('->')

nested_identifier = (
    pyparsing.pyparsing_common.identifier('table')
    + Optional(
        DOT
        + pyparsing.pyparsing_common.identifier('column')
    )
).set_parse_action(
    lambda term: {
        'nested_identifier': (
            {'table': term['table']}
            | ({'column': term['column']}
                if term.get('column') else {})
        )
    }
)