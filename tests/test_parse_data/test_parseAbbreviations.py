import pathlib

import pytest

from ...parse_data.parseAbbreviations import parse_of_file_with_abbreviations


data_dir = pathlib.PosixPath(__file__).parent.parent / 'data'
abbreviations_data = data_dir / 'abbreviations.txt'


class TestOfParseAbbreviations:
    """test class, for testing 'parse_of_file_with_abbreviations' """

    def test_with_typical_case(self):
        with open(abbreviations_data, 'r') as file:
            result = parse_of_file_with_abbreviations(file)[0]  # getting first result
            assert result == ['DRR', 'Daniel Ricciardo', 'RED BULL RACING TAG HEUER']

    def test_atypical_case(self):
        with pytest.raises(TypeError):
            parse_of_file_with_abbreviations('anything')
