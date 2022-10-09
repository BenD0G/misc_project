from io import StringIO
from unittest import TestCase, mock

from file_structure import ColumnInfo, extract_column_info


class Tests(TestCase):
    def test_single_header(self):
        """ Test that a file with only one header works. """
        input_text = "order_id[int]"
        with mock.patch("file_structure.open", return_value=StringIO(input_text)):
            self.assertEqual(
                extract_column_info("dummy"), [ColumnInfo(type=int, name="order_id")]
            )

    def test_multiple_headers(self):
        """ Test that a file with multiple headers works. """
        input_text = (
            "order_id[int], stock[string], price[float], size[int], executed[bool]"
        )

        expected = [
            ColumnInfo(type=int, name="order_id"),
            ColumnInfo(type=str, name="stock"),
            ColumnInfo(type=float, name="price"),
            ColumnInfo(type=int, name="size"),
            ColumnInfo(type=bool, name="executed"),
        ]

        with mock.patch("file_structure.open", return_value=StringIO(input_text)):
            self.assertEqual(extract_column_info("dummy"), expected)
