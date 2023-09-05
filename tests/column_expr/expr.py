TEST_CASES = [
    [
        '-id',
        '+id',
        'not id'
    ],
    [
        'id * name',
        'id / name',
        'id % name'
    ],
    [
        'id + name',
        'id - name',
        'id || name'
    ],
    [
        'id == name',
        'id = name',
        'id != name',
        'id <= name',
        'id >= name',
        'id < name',
        'id > name',
        'id in name',
        'id not in name',
        'id global in name',
        'id global not in name',
        'id like name',
        'id not like name',
        'id ilike name',
        'id not ilike name',
    ],
    [
        'id is null',
        'id is not null'
    ],
    [
        'id between 1 and 2',
        'id not between 1 and 2'
    ],
    [
        'id and name',
        'id or name'
    ],
]
