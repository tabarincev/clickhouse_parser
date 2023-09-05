

class OpNode:
    def __repr__(self):
        return '{{\'{}\':{!r}}}'.format(
            self.operator,
            self.operands
        )


class UnaryOperator(OpNode):
    def __init__(self, tokens):
        self.operator = tokens[0][0]
        self.operands = tokens[0][1]


class BinaryOperator(OpNode):
    def __init__(self, tokens):
        self.operator = tokens[0][1]
        self.operands = tokens[0][::2]


class BetweenOperator:
    def __init__(self, tokens):
        self.column = tokens[0][0]
        self.operator = ' '.join(tokens[0][1])
        self.from_ = tokens[0][2]
        self.to = tokens[0][4]

    def __repr__(self):
        return """
        {
            'between_op': {
                'column': %s,
                'operator': '%s',
                'from': %s,
                'to': %s
            }
        }
        """ % (self.column, self.operator, self.from_, self.to)


class IsNotOperator:
    def __init__(self, tokens):
        self.column = tokens[0][0]
        self.operator = ' '.join(tokens[0][1])

    def __repr__(self):
        return """
        {
            'is_operator': {
                'column': %s,
                'operator': '%s',
                'literal': 'NULL'
            }
        }
        """ % (self.column, self.operator)


class IsInLikeOperator:
    def __init__(self, tokens):
        self.column = tokens[0][0]
        self.operator = ' '.join(tokens[0][1])
        self.second_column = tokens[0][2]

    def __repr__(self):
        return """
        {
            '%s': {
                'column': %s,
                'second_column': %s
            }
        }
        """ % (self.operator, self.column, self.second_column)


class IndexOperator:
    def __init__(self, tokens):
        self.term = tokens[0][0]
        self.index = tokens[0][1]

    def __repr__(self):
        return """
        {
            'index_term': {
                'term': %s,
                'index': %s
            }
        }
        """ % (self.term, self.index)


class AliasOperator:
    def __init__(self, tokens):
        self.expr = tokens[0][0]
        self.alias = tokens[0][2]

    def __repr__(self):
        return """
        {
            'alias_term': {
                'expr': %s,
                'alias': %s
            }
        }
        """ % (self.expr, self.alias)


class UnionOperator(OpNode):
    def __init__(self, tokens):
        self.operator = '_'.join(tokens[0][1]).lower()
        self.operands = tokens[0][::2]
