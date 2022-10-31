import _io


def parse_of_file_with_abbreviations(file: _io.TextIOWrapper):
    """
    function parse file with abbreviations
    get file
    :return (abbreviation, name, car)"""
    if not isinstance(file, _io.TextIOWrapper):
        raise TypeError
    return [line.rstrip().split('_') for line in file]


if __name__ == "__main__":  # pragma: no cover
    with open('../tests/data/abbreviations.txt') as file_abbreviations:
        result = parse_of_file_with_abbreviations(file_abbreviations)
    for content in result:
        print(content)
