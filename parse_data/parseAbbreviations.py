import os
from functools import lru_cache
import pathlib


@lru_cache(maxsize=None)
def parse_of_file_with_abbreviations(path_to_file) -> list:
    """
    function parse file with abbreviations
    get file
    :return (abbreviation, name, car)"""
    if not (isinstance(path_to_file, str) or isinstance(path_to_file, pathlib.PosixPath)):
        raise TypeError("the object being passed must be str of 'pathlib.PosixPath'")

    if os.path.isfile(path_to_file):
        with open(path_to_file) as file:
            return [line.rstrip().split('_') for line in file]
    else:
        raise FileNotFoundError(f'file {path_to_file} not exist')


if __name__ == "__main__":  # pragma: no cover
    file_path = pathlib.Path(__file__).parent.parent / 'tests/data/abbreviations.txt'
    result = parse_of_file_with_abbreviations(file_path)
    for content in result:
        print(content)
