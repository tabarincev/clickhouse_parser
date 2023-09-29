import unittest

from typing import Dict
from src.lexer.query.select_union.format import Format


class TestFormatClause(unittest.TestCase):
    def __init__(self):
        super().__init__()
        self.format_clause = Format().notation

    def test_is_dict(self):
        self.assertIsInstance(
            self.format_clause.parse_string('select 1', parse_all=True),
            Dict
        )

    def test_
