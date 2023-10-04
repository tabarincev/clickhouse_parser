from pyparsing import MatchFirst, ParserElement, Literal

from src.keywords import FORMAT
from src.lexer.statement import Statement


class Format(Statement):
    @property
    def notation(self) -> ParserElement:
        return (FORMAT + self.format_type('file_format')).set_parse_action(
            lambda term: {'format': {'file_format': term['file_format']}}
        )

    @property
    def format_type(self):
        return MatchFirst([
            Literal('TabSeparated'),
            Literal('TabSeparatedRaw'),
            Literal('TabSeparatedWithNames'),
            Literal('TabSeparatedWithNamesAndTypes'),
            Literal('Template'),
            Literal('TemplateIgnoreSpaces'),
            Literal('CSV'),
            Literal('CSVWithNames'),
            Literal('CSVWithNamesAndTypes'),
            Literal('CustomSeparated'),
            Literal('CustomSeparatedWithNames'),
            Literal('CustomSeparatedWithNamesAndTypes'),
            Literal('Values'),
            Literal('Vertical'),
            Literal('JSONAsString'),
            Literal('JSONStrings'),
            Literal('JSONCompact'),
            Literal('JSONCompactStrings'),
            Literal('JSONEachRow'),
            Literal('JSONEachRowWithProgress'),
            Literal('JSONStringsEachRow'),
            Literal('JSONStringsEachRowWithProgress'),
            Literal('JSONCompactEachRow'),
            Literal('JSONCompactEachRowWithNamesAndTypes'),
            Literal('JSONCompactStringsEachRow'),
            Literal('JSONCompactStringsEachRowWithNamesAndTypes'),
            Literal('JSON'),
            Literal('TSKV'),
            Literal('Pretty'),
            Literal('PrettyCompact'),
            Literal('PrettyCompactMonoBlock'),
            Literal('PrettyNoEscapes'),
            Literal('PrettySpace'),
            Literal('Protobuf'),
            Literal('ProtobufSingle'),
            Literal('Avro'),
            Literal('AvroConfluent'),
            Literal('Parquet'),
            Literal('Arrow'),
            Literal('ArrowStream'),
            Literal('ORC'),
            Literal('RowBinary'),
            Literal('RowBinaryWithNames'),
            Literal('RowBinaryWithNamesAndTypes'),
            Literal('Native'),
            Literal('Null'),
            Literal('XML'),
            Literal('CapnProto'),
            Literal('LineAsString'),
            Literal('Regexp'),
            Literal('RawBLOB'),
            Literal('MsgPack')
        ])
