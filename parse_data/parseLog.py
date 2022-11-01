import os.path
from functools import lru_cache
import pathlib


@lru_cache(maxsize=None)
def parse_of_log_with_results(path_to_file) -> list:
    """
    function parse file log
    get file
    :return (abbreviation, date, time)
    """
    if not (isinstance(path_to_file, str) or isinstance(path_to_file, pathlib.PosixPath)):
        raise TypeError("the object being passed must be str or 'pathlib.PosixPath'")
    if os.path.isfile(path_to_file):
        with open(path_to_file) as file:
            return [[line[:3], line.split('_')[0][3:], line.rstrip().split('_')[1]] for line in file if line != '\n']
    else:
        raise FileNotFoundError(f'file {path_to_file} not exist')


if __name__ == '__main__':  # pragma: no cover
    file_path = pathlib.Path(__file__).parent.parent / 'tests/data/start.log'
    result = parse_of_log_with_results(file_path)
    for content in result:
        print(content)
