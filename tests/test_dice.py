import logging
import random
from itertools import zip_longest as lzip

import pytest


random_seed = 10


@pytest.mark.parametrize("formula, seed, expected", [
    ("1", random_seed, 1),
    ("d1", random_seed, 1),
    ("10d1", random_seed, 10),
    ("10d1 + 1", random_seed, 11),
    ("10d1 - 1", random_seed, 9),
    ("10d1 * 5", random_seed, 50),
    ("10d1 / 5", random_seed, 2),

    # Due to the RNG state, these are all sort of order dependent.
    # Additionally, if one of them fails, everything following will
    # fail.  However, this is probably the best way to exercise the
    # code.  Because the subsequent tests will fail, debugging a test
    # should always start with the first failure and move forward.
    ("4d6", random_seed, 10),
    ("4d6M3", random_seed, 9),
    ("6x4d6M3", random_seed, (9, 11, 7, 9, 13, 9)),
    ("10d6<4", random_seed, 13),
    ("10d6>3", random_seed, 14),
    ("10d6>=3", random_seed, 17),
    ("10d6<=4", random_seed, 17),
    ("10d6==1", random_seed, 2),
    ("10d6!=6", random_seed, 27),
    ("2d6m2", random_seed, 7),
    ("d%", random_seed, 10),
    ("10d%>50M3 + 10 * 2 / 5", random_seed, 262),
])
def test_dsl(formula, seed, expected):
    from dice.parser import parse

    # logging.basicConfig(level=logging.DEBUG)

    values = parse(formula, seed=seed)
    if isinstance(expected, (list, tuple)):
        for value, expect in lzip(values, expected):
            assert value == expect
    else:
        found = next(values)
        assert found == expected
