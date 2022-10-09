""" Tests for the public API. """


import io
from unittest import TestCase, mock

from main import main


class Tests(TestCase):
    def test_no_rows(self):
        """ Test that a file with no data rows returns just the header. """
        input_text = (
            """order_id[int], stock[string], price[float], size[int], executed[bool]"""
        )
        input_query_str = "price < 100"

        def mock_open(*args, **kwargs):
            return io.StringIO(input_text)

        with mock.patch("file_structure.open", mock_open):
            main("dummy", input_query_str, "no_rows.csv")

    def test_basic_ok(self):
        """ Test that a file with no data rows returns just the header. """
        input_text = """order_id[int], stock[string], price[float], size[int], executed[bool]
        1, stock1, 99, 3, false"""
        input_query_str = "price < 100"

        def mock_open(*args, **kwargs):
            return io.StringIO(input_text)

        with mock.patch("file_structure.open", mock_open):
            main("dummy", input_query_str, "one_row.csv")

    def test_basic_ok2(self):
        """ Test that a file with no data rows returns just the header. """
        input_text = """order_id[int], stock[string], price[float], size[int], executed[bool]
        1, stock1, 100, 3, false"""
        input_query_str = "price < 100"

        def mock_open(*args, **kwargs):
            return io.StringIO(input_text)

        with mock.patch("file_structure.open", mock_open):
            main("dummy", input_query_str, "one_row2.csv")

    def test_one_ok_one_not(self):
        """ Test that a file with no data rows returns just the header. """
        input_text = """order_id[int], stock[string], price[float], size[int], executed[bool]
        1, stock1, 99, 3, false
        1, stock1, 100, 3, false"""
        input_query_str = "price < 100"

        def mock_open(*args, **kwargs):
            return io.StringIO(input_text)

        with mock.patch("file_structure.open", mock_open):
            main("dummy", input_query_str, "one_ok_one_not.csv")
