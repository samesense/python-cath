import contextlib
import os
import shutil


def concat(file_list, output_file):
    """Concatenate CSV files that share the same header.

    Args:
        file_list: Paths to input files.
        output_file: Path to write the concatenated output.

    Raises:
        ValueError: If no input files are provided, any file has an empty
            header, an input file path collides with the output file, or
            file headers differ.
    """
    file_list = list(file_list)
    if not file_list:
        raise ValueError("file_list must not be empty")

    real_output = os.path.realpath(output_file)
    for afile in file_list:
        if os.path.realpath(afile) == real_output:
            raise ValueError(
                f"Input file {afile!r} is the same path as the output file"
            )

    with contextlib.ExitStack() as stack:
        handles = [
            stack.enter_context(open(afile, encoding="utf-8"))
            for afile in file_list
        ]
        file_headers = {}
        for afile, fh in zip(file_list, handles):
            header = fh.readline().rstrip("\n")
            if not header:
                raise ValueError(
                    f"File {afile!r} has an empty or missing header"
                )
            file_headers[afile] = header

        unique_headers = set(file_headers.values())
        if len(unique_headers) > 1:
            detail = ", ".join(f"{f!r}: {h!r}" for f, h in file_headers.items())
            raise ValueError(f"Headers do not match: {detail}")

        with open(output_file, "w", encoding="utf-8") as out:
            out.write(next(iter(unique_headers)) + "\n")
            for fh in handles:
                shutil.copyfileobj(fh, out)
