from typing import Dict

from select_union import SelectUnion
from create import CreateStatement

from pyparsing import MatchFirst, ParserElement


class Query:
    @property
    def notation(self) -> ParserElement:
        return MatchFirst([
            SelectUnion().notation
        ])

    def parse_sql(self, sql, validation=True) -> Dict:
        return self.notation.parse_string(sql, parse_all=validation)[0]
