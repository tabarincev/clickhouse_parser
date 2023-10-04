from typing import Dict, List


select_ast = {
  "select_union_statement": {
    "select": {
      "columns": [
        {
          "literal_term": {
            "numeric": 1
          }
        }
      ]
    },
    "from": {
      "join_expr": {
        "select": {
          "columns": [
            {
              "literal_term": {
                "numeric": 2
              }
            }
          ]
        },
        "from": {
          "join_expr": {
            "table_identifier": {
              "database": "ab",
              "table": "main_metrics"
            }
          }
        },
        "alias": "mm",
        "joins": [
          {
            "operator": {
              "join_type": "inner"
            },
            "table_to_join": {
              "select": {
                "columns": [
                  {
                    "literal_term": {
                      "numeric": 3
                    }
                  }
                ]
              },
              "from": {
                "join_expr": {
                  "table_identifier": {
                    "database": "ab",
                    "table": "experiments"
                  }
                }
              },
              "alias": "exps"
            },
            "constraint": {
              "type": "using",
              "exprs": [
                {
                  "column_term": {
                    "column": "experiment_group_id"
                  }
                },
                {
                  "column_term": {
                    "column": "experiment_group_id_type"
                  }
                }
              ]
            }
          }
        ]
      }
    }
  }
}


def get_join(ast: Dict) -> List:
    result = []

    from_expr = ast['select_union_statement'].get('from')

    if not from_expr:
        return []

    while 'joins' in from_expr['join_expr']:
        print(from_expr['join_expr'].get)
        break
    return result


get_join(select_ast)