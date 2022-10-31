import _io


def parse_of_log_with_results(file: _io.TextIOWrapper):
    """
    function parse file log
    get file
    :return (abbreviation, date, time)
    """
    if not isinstance(file, _io.TextIOWrapper):
        raise TypeError
    return [[line[:3], line.split('_')[0][3:], line.rstrip().split('_')[1]] for line in file if line != '\n']


if __name__ == '__main__':  # pragma: no cover
    with open('../tests/data/start.log') as file_log:
        result = parse_of_log_with_results(file_log)
    for content in result:
        print(content)
