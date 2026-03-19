import shutil


def concat(file_list, output_file):
    """Concatenate CSV files that share the same header.

    Args:
        file_list: Paths to input files.
        output_file: Path to write the concatenated output.

    Raises:
        ValueError: If no input files are provided or file headers differ.
    """
    file_list = list(file_list)
    if not file_list:
        raise ValueError("file_list must not be empty")
    file_headers = {}
    for afile in file_list:
        with open(afile) as f:
            file_headers[afile] = f.readline().rstrip("\n")
    unique_headers = set(file_headers.values())
    if len(unique_headers) > 1:
        detail = ", ".join(f"{f!r}: {h!r}" for f, h in file_headers.items())
        raise ValueError(f"Headers do not match: {detail}")
    with open(output_file, "w") as out:
        out.write(next(iter(unique_headers)) + "\n")
        for afile in file_list:
            with open(afile) as f:
                f.readline()  # skip header
                shutil.copyfileobj(f, out)
