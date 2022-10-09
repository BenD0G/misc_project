""" Entry point for CSV file parsing. """

from file_structure import extract_column_info, extract_row_infos
from query_parse import parse_query_string


def _write_csv(fname, column_infos, row_infos):
    """ Write data to a CSV file. """
    with open(fname, "w") as f:
        f.write(", ".join(f"{x.name}[{x.type}]" for x in column_infos) + "\n")
        for row_info in row_infos:
            row_values = [row_info[x.name].value for x in column_infos]
            f.write(", ".join(str(row_value) for row_value in row_values))


def main(filename: str, query_str: str, output_fname: str):
    """ Filter the CSV by the query string, and write the new CSV to disk. """
    column_infos = extract_column_info(filename)
    row_infos = extract_row_infos(filename, column_infos)

    query = parse_query_string(query_str)

    filtered_row_infos = filter(query, row_infos)

    _write_csv(output_fname, column_infos, filtered_row_infos)
