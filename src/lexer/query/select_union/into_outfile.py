from pyparsing import pyparsing_common
from pyparsing import ParserElement, MatchFirst, CaselessLiteral, Optional

from src.literals import string_literal
from src.lexer.statement import Statement
from src.keywords import INTO, OUTFILE, COMPRESSION, LEVEL


class IntoOutfile(Statement):
    @property
    def notation(self) -> ParserElement:
        return (
            INTO + OUTFILE + string_literal('filename')
            + Optional(
                COMPRESSION + self.compression_type('compression')
                + Optional(LEVEL + self.level_type('level'))
            )
        ).set_parse_action(
            lambda term: (
                {'into_outfile': {'filename': term['filename']}}
                | ({'compression': term['compression']}
                    if term.get('compression') else {})
                | ({'level': term['level']}
                    if term.get('level') else {})
            )
        )

    @property
    def compression_type(self):
        return MatchFirst([
            CaselessLiteral('none'),
            CaselessLiteral('gzip'),
            CaselessLiteral('deflate'),
            CaselessLiteral('br'),
            CaselessLiteral('xz'),
            CaselessLiteral('zstd'),
            CaselessLiteral('lz4'),
            CaselessLiteral('bz2')
        ])

    @property
    def level_type(self):
        return pyparsing_common.integer.add_condition(
            lambda term: 0 < int(term[0]) < 13
        )
