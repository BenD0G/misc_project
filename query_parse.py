""" Utilities for parsing a query string. """
import re
from typing import Any, Callable, Dict


def parse_query_string_simple(query: str) -> Callable:
    """Given a query string like:
        "(price < 100 && executed = true) || (price > 100 && executed = false)"
    return a callable that on a dict (col_name to ColumnInfo) to say whether or not it should be kept.

    Assume for now that query string is valid.

    Only matches simple strings.
    """
    simple_regex = re.compile(r"([a-z_]+) ([><=]) (.*)")  # e.g. "price < 100"

    if match := simple_regex.match(query):
        column_name, operator, comparison_value = match.groups()
        if operator == "=":
            operator = "=="

    return lambda row_dict: eval(
        f"{row_dict[column_name].value} {operator} {row_dict[column_name].column_info.type(comparison_value)}"
    )


def _contents_of_bracket(query: str):
    """Given e.g. ((a or b) or c), return "(a or b) or c".
    Need opening character to be '('

    >>> _contents_of_bracket("(a, b(c or d))")
    'a, b(c or d)'
    """
    opening_bracket_count = 0
    for i, c in enumerate(query):
        if c == "(":
            opening_bracket_count += 1
        elif c == ")":
            opening_bracket_count -= 1

        if opening_bracket_count == 0:
            return query[1:i]


def _query_until_composition(query: str):
    """Given e.g. a & b, return "a".

    >>> _query_until_composition("a & (b or c)")
    'a'
    """
    for i, c in enumerate(query):
        if c in ("&", "|"):
            return query[: i - 1], c, query[i + 1 :]

    return query, None, None


_COMPARISON_REGEX = re.compile(r"([a-z_]+) ([><=]) (.*)")  # e.g. "price < 100"


def parse_query_string2(query: str) -> Callable:
    """Recursive function for generating one callable which calls other callables.
    e.g. (price < 100 && executed = true) || price > 100
    """
    for i, c in enumerate(query):
        if c == "(":
            contents = _contents_of_bracket(query[i:])
            return parse_query_string2(contents)
        else:
            contents_before, composition, contents_after = _query_until_composition(
                query[i:]
            )
            if composition is None:  # No composition: atomic
                return parse_query_string_simple(contents_before)

            left_query = parse_query_string2(contents_before)
            right_query = parse_query_string2(contents_after)
            if composition == "&":
                return lambda x: left_query(x) & right_query(x)
            elif composition == "|":
                return lambda x: left_query(x) | right_query(x)
            elif composition is None:  # No composition: atomic
                return parse_query_string_simple(contents_before)
