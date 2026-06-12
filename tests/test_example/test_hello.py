import pytest
from python_cath.__main__ import app
from python_cath.concat import concat
from typer.testing import CliRunner

runner = CliRunner()


@pytest.mark.parametrize(
    ("vals", "expected"),
    [
        (
            ("c1,c2\nv1,v1", "c1,c2\nv2,v2"),
            "c1,c2\nv1,v1\nv2,v2",
        ),
    ],
)
def test_hello(tmp_path, vals, expected):
    """Example test with parametrization."""
    one = tmp_path / "one"
    two = tmp_path / "two"
    out = tmp_path / "tmpOut"
    one.write_text(vals[0] + "\n")
    two.write_text(vals[1] + "\n")
    concat((str(one), str(two)), str(out))
    assert out.read_text().strip() == expected


def test_mismatched_headers(tmp_path):
    """Concat raises ValueError when file headers differ."""
    one = tmp_path / "one"
    two = tmp_path / "two"
    one.write_text("c1,c2\nv1,v1\n")
    two.write_text("a,b\nv2,v2\n")
    with pytest.raises(ValueError, match="Headers do not match"):
        concat((str(one), str(two)), str(tmp_path / "out"))


def test_empty_file_list(tmp_path):
    """Concat raises ValueError when given an empty file list."""
    with pytest.raises(ValueError, match="must not be empty"):
        concat([], str(tmp_path / "out"))


def test_empty_header(tmp_path):
    """Concat raises ValueError when a file has an empty header."""
    one = tmp_path / "one"
    one.write_text("\nv1,v1\n")
    with pytest.raises(ValueError, match="empty or missing header"):
        concat([str(one)], str(tmp_path / "out"))


def test_output_collides_with_input(tmp_path):
    """Concat raises ValueError when output path matches an input path."""
    one = tmp_path / "one"
    one.write_text("c1,c2\nv1,v1\n")
    with pytest.raises(ValueError, match="same path as the output"):
        concat([str(one)], str(one))


def test_cli_last_arg_is_output(tmp_path):
    """The CLI treats the final positional argument as the output file."""
    one = tmp_path / "one"
    two = tmp_path / "two"
    out = tmp_path / "out"
    one.write_text("c1,c2\nv1,v1\n")
    two.write_text("c1,c2\nv2,v2\n")
    result = runner.invoke(app, [str(one), str(two), str(out)])
    assert result.exit_code == 0
    assert out.read_text().strip() == "c1,c2\nv1,v1\nv2,v2"


def test_cli_two_files_errors_without_overwriting(tmp_path):
    """With only two files there is one input; the CLI must error instead of
    overwriting the second file (the would-be output)."""
    one = tmp_path / "one"
    two = tmp_path / "two"
    one.write_text("c1,c2\nv1,v1\n")
    two.write_text("c1,c2\nv2,v2\n")
    result = runner.invoke(app, [str(one), str(two)])
    assert result.exit_code != 0
    # The second file must be left untouched, not overwritten by the cat.
    assert two.read_text() == "c1,c2\nv2,v2\n"
