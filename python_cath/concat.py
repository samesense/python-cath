import os


def concat(file_list, output_file):
    headers = []
    for afile in file_list:
        with open(afile) as f:
            headers.append(f.readline().rstrip("\n"))
    if len(set(headers)) > 1:
        raise ValueError(f"Headers do not match: {headers}")
    os.system(f"head -1 {file_list[0]} > {output_file}")
    for afile in file_list:
        os.system(f"tail -n +2 {afile} >> {output_file}")
