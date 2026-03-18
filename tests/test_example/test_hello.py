import pytest

from python_cath.concat import concat


@pytest.mark.parametrize(
    ("vals", "expected"),
    [(("c1,c2\nv1,v1", "c1,c2\nv2,v2"), "c1,c2\nv1,v1\nv2,v2",),],
)
def test_hello(vals, expected):
    """Example test with parametrization."""
    with open("one", "w") as fout:
        print(vals[0], file=fout)
    with open("two", "w") as fout:
        print(vals[1], file=fout)
    files = ("one", "two")
    concat(files, "tmpOut")
    with open("tmpOut") as f:
        lines = f.read().strip()
    assert lines == expected


def test_mismatched_headers():
    """Concat raises ValueError when file headers differ."""
    with open("one", "w") as fout:
        print("c1,c2\nv1,v1", file=fout)
    with open("two", "w") as fout:
        print("a,b\nv2,v2", file=fout)
    with pytest.raises(ValueError, match="Headers do not match"):
        concat(("one", "two"), "tmpOut")
