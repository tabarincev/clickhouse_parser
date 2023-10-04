from typing import Dict
from textwrap import dedent

from src.builder.builder import BaseBuilder


class SettingsBuilder(BaseBuilder):  # todo test
    def build(self, ast: Dict) -> str:
        if 'settings' not in ast['select_union_statement']:
            raise ValueError(
                'Invalid structure of SQL AST - Expected "settings" key'
            )

        settings_ast = ast['select_union_statement']['settings']

        return dedent(
            'settings {settings_list}'.format(
                settings_list=','.join([
                    '{name}={value}'.format(
                        name=setting['setting'],
                        value=setting['value']
                    ) for setting in settings_ast['settings']
                ])
            )
        )
