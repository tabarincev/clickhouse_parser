TEST_CASES = [
    # case
    [

    ],
    # cast
    [

    ],
    # date
    [
        'DATE "2023-05-01"',

    ],
    # extract
    [
        'EXTRACT(SECOND FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(MINUTE FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(HOUR FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(DAY FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(WEEK FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(MONTH FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(QUARTER FROM "2003-04-12 04:05:06 America/New_York")',
        'EXTRACT(YEAR FROM "2003-04-12 04:05:06 America/New_York")',
    ],
    # interval
    [
        'INTERVAL 1 SECOND',
        'INTERVAL 1 MINUTE',
        'INTERVAL 1 HOUR',
        'INTERVAL 1 DAY',
        'INTERVAL 1 WEEK',
        'INTERVAL 1 MONTH',
        'INTERVAL 1 QUARTER',
        'INTERVAL 1 YEAR',
    ],
    # substring
    [
        'SUBSTRING("s" FROM "'
    ],
    # timestamp
    [
        'TIMESTAMP "2003-04-12 04:05:06"'
    ],
    # trim
    [
        'TRIM(BOTH "str" FROM "string")',
        'TRIM(LEADING "str" FROM "string")',
        'TRIM(TRAILING "str" FROM "string")',
    ],
    # window function
    [

    ],
    # window function target
    [

    ],
    # function
    [

    ],
    # lambda function
    [
        ''
    ],
    # asterisk
    [
        'table.*',
        '*'
    ],
    # column identifier
    [
        'db.table.column',
        'table.column',
        'column'
    ],
    # literal
    [
        '1',
        '"string"',
        'NULL'
    ],
    # select_union_statement
    [

    ],
    # parens
    [
        '(identifier)'
    ],
    # tuple
    [
        '(id, name, user)'
    ],
    # array
    [
        '[id, name, user]'
    ]
]
