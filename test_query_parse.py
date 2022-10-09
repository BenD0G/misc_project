from unittest import TestCase

from file_structure import ColumnInfo, RowInfo
from query_parse import parse_query_string2, parse_query_string_simple


class Tests(TestCase):
    def test_simple(self):
        """ Test a basic case. """
        query_str = "price < 100"
        column_infos = [ColumnInfo(type=float, name="price")]
        input_dict = {"price": RowInfo(column_info=column_infos[0], value=99)}
        input_dict2 = {"price": RowInfo(column_info=column_infos[0], value=100)}

        fn = parse_query_string_simple(query_str)

        self.assertEqual(fn(input_dict), True)
        self.assertEqual(fn(input_dict2), False)

    def test_atomic(self):
        column_infos = [ColumnInfo(type=float, name="price")]

        query = "price < 100"
        query_fn = parse_query_string2(query)
        input_dict = {"price": RowInfo(column_info=column_infos[0], value=99)}
        self.assertEqual(query_fn(input_dict), True)

    def test_composite(self):
        column_infos = [ColumnInfo(type=float, name="price")]

        query = "(price < 100) & (price < 99)"
        query_fn = parse_query_string2(query)
        input_dict = {"price": RowInfo(column_info=column_infos[0], value=99)}
        self.assertEqual(query_fn(input_dict), True)
