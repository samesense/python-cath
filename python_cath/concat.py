def concat(file_list, output_file):
    """Concatenate CSV files that share the same header.

    Args:
        file_list: Paths to input files.
        output_file: Path to write the concatenated output.

    Raises:
        ValueError: If the input files have mismatched headers.
    """
    headers = []
    for afile in file_list:
        with open(afile) as f:
            headers.append(f.readline().rstrip("\n"))
    if len(set(headers)) > 1:
        raise ValueError(f"Headers do not match: {headers}")
    with open(output_file, "w") as out:
        out.write(headers[0] + "\n")
        for afile in file_list:
            with open(afile) as f:
                f.readline()  # skip header
                out.write(f.read())
