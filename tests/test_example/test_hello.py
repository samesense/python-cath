import pytest

from python_cath.concat import concat


@pytest.mark.parametrize(
    ("files", "expected"),
    [
        (
            ("tests/test_example/one", "tests/test_example/two"),
            """c1,c2
v1,v1
v2,v2""",
        ),
    ],
)
def test_hello(files, expected):
    """Example test with parametrization."""
    concat(files, "tmpOut")
    with open("tmpOut") as f:
        lines = f.read().strip()
    assert lines == expected
