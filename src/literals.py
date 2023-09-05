import pyparsing
import src.keywords as keyword

from pyparsing import Literal, Suppress, MatchFirst, Word, CaselessKeyword
from pyparsing import alphas, alphanums


UNARY, BINARY, TERNARY = 1, 2, 3

string_literal = MatchFirst([
    pyparsing.dbl_quoted_string(),
    pyparsing.sgl_quoted_string()
])

keywords = MatchFirst((
    CaselessKeyword(keyword) for keyword in dir(keyword)
    if not keyword.startswith('__') and keyword == keyword.upper()
))

identifier_word = Word(alphas + '_@#', alphanums + '@$#_')
identifier = ~keywords + identifier_word.copy()

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
NOT_EQ = Literal('!=')
LE = Literal('<=')
GE = Literal('>=')
LT = Literal('<')
GT = Literal('>')
ARROW = Literal('->')

