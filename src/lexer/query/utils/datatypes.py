from pyparsing import *
from math import log
from functools import lru_cache


class DataType:
    @lru_cache()
    @property
    def integer_type(self):
        return MatchFirst([
            MatchFirst([
                CaselessKeyword('int{bits}'.format(bits=i))
                for i in [pow(2, i) for i in range(int(log(512, 2)))]
            ]),
            MatchFirst([
                CaselessKeyword('uint{bits}'.format(bits=i))
                for i in [pow(2, i) for i in range(int(log(512, 2)))]
            ])
        ])

    @property
    def floating_type(self):
        return MatchFirst([
            CaselessKeyword('float{}'.format(bits=i))
            for i in [32, 64]
        ])

    @property
    def bool_type(self):
        return CaselessKeyword('bool')

    @property
    def string_type(self):
        return MatchFirst([
            
        ])

