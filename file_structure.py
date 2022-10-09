""" Utilities for extracting the column info for a given CSV file. """

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(eq=True)
class ColumnInfo:
    """ What each column of a .csv file represents. """

    type: type
    name: str


@dataclass
class RowInfo:
    """ What each row represents. """

    column_info: ColumnInfo
    value: Any


def extract_column_info(filename: str) -> List[ColumnInfo]:
    """Given a filename, extract the header info, to be used for processing.
    Assume for now that header line is syntactically valid (no error handling).
    """
    with open(filename, "r") as f:
        headers = f.readline().split(",")

    type_name_to_type = {"int": int, "string": str, "float": float, "bool": bool}

    # `headers` should be a list of strings like ["order_id[int]"]
    ret = []
    for header in headers:
        parts = header.strip().split("[")
        name = parts[0]
        type_ = parts[1][:-1]  # Ignore closing "]"
        ret.append(ColumnInfo(type=type_name_to_type[type_], name=name))

    return ret


def extract_row_infos(
    filename: str, column_infos: List[ColumnInfo]
) -> List[Dict[str, RowInfo]]:
    """Given a filename, extract the row infos, maps from column name to RowInfo.
    Assume for now that lines are syntactically valid (no error handling).
    """
    ret = []
    with open(filename, "r") as f:
        _ = f.readline()  # header
        for line in f.readlines():
            row_infos = {}
            values = line.split(",")
            for i, value in enumerate(values):
                column_info = column_infos[i]
                value = column_info.type(value.strip())
                row_infos[column_info.name] = RowInfo(
                    column_info=column_info, value=value
                )
            ret.append(row_infos)
    return ret
