import pytest

from app.helpers import random_string


@pytest.mark.parametrize(
    'char_len, result',
    [
        (-1, None),
        (0, None),
    ]
)
def test_random_string_wrong_len(char_len, result):
    string = random_string(char_len=char_len)
    assert string == result


def test_random_string():
    string = random_string(char_len=2)
    assert string.isalnum()
    assert len(string) == 2

