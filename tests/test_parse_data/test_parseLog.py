import pathlib

import pytest

from ...parse_data.parseLog import parse_of_log_with_results


data_dir = pathlib.PosixPath(__file__).parent.parent / 'data'
log_data = data_dir / 'start.log'


class TestOfParseAbbreviations:
    """test class, for testing 'parseAbbreviations.py' """

    def test_with_typical_case(self):
        result = parse_of_log_with_results(log_data)[0]  # getting first result
        assert result == ['SVF', '2018-05-24', '12:02:58.917']

    def test_atypical_case(self):
        with pytest.raises(TypeError):
            parse_of_log_with_results(123)

        with pytest.raises(FileNotFoundError):
            parse_of_log_with_results('test_file_not_exist')
