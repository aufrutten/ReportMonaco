import datetime
import pathlib

from parse_data import parseLog, parseAbbreviations
import parser_cli


def compare_start_end_time(data) -> tuple[dict, dict]:
    """compare time in start and in end, and take result"""
    if not isinstance(data, dict):
        raise TypeError

    dict_with_results = {}
    for abbreviation in data:

        start = "{}_{}".format(
            data[abbreviation]['start']['date'],
            data[abbreviation]['start']['time']
        )
        end = "{}_{}".format(
            data[abbreviation]['end']['date'],
            data[abbreviation]['end']['time']
        )

        start_time = datetime.datetime.strptime(start, '%Y-%m-%d_%H:%M:%S.%f')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%d_%H:%M:%S.%f')
        result = str(abs(end_time-start_time))

        data[abbreviation]['result'] = result
        dict_with_results[result] = abbreviation
    return data, dict_with_results


def merge_dicts(dict_one, dict_two, dict_third):
    """function merge dicts, or change if key exist"""
    if not (
            isinstance(dict_one, dict) and
            isinstance(dict_two, dict) and
            isinstance(dict_third, dict)
    ):
        raise TypeError("arguments should be dict")

    new_dict = {}
    for abbreviation in dict_one:
        new_dict[abbreviation] = dict_one[abbreviation] | dict_two[abbreviation] | dict_third[abbreviation]
    return new_dict


def find_driver(name_driver, path_to_folder_with_data):
    """function for find driver in data"""

    if not isinstance(name_driver, str):
        raise TypeError('argument driver must be str')

    data, results = build_report(path_to_folder_with_data)

    for abbreviation in data:
        if data[abbreviation]['name'] == name_driver:
            car = data[abbreviation]['car']
            result = data[abbreviation]['result']
            return f'  1. {name_driver:<20}| {car:<25} | {result}'
    else:
        return 'Driver not found'


def print_to_console(list_to_print):
    return '\n\n'.join(
        [f'{num+1:>3}. {name:<20}| {car:<25} | {result}' for num, (name, car, result) in enumerate(list_to_print)]
    )


def build_report(path_to_data):
    """main data collector, get raw data, and return full data"""

    if not (isinstance(path_to_data, str) or isinstance(path_to_data, pathlib.PosixPath)):
        raise TypeError('path should be str or pathlib.PosixPath')

    if isinstance(path_to_data, str):
        path_to_data = pathlib.PosixPath(path_to_data)

    start_log = parseLog.parse_of_log_with_results(
        path_to_data / 'start.log'
    )
    end_log = parseLog.parse_of_log_with_results(
        path_to_data / 'end.log'
    )
    abbreviations_txt = parseAbbreviations.parse_of_file_with_abbreviations(
        path_to_data / 'abbreviations.txt'
    )

    dict_of_start_log = {i[0]: {'start': {'date': i[1], 'time': i[2]}} for i in start_log}
    dict_of_end_log = {i[0]: {'end': {'date': i[1], 'time': i[2]}} for i in end_log}
    dict_of_abbreviations = {i[0]: {'name': i[1], 'car': i[2]} for i in abbreviations_txt}

    data = merge_dicts(dict_of_start_log, dict_of_end_log, dict_of_abbreviations)
    return compare_start_end_time(data)


def print_report(path_to_folder_with_data, reverse=False, driver=None):
    """incoming data handler"""
    if not (isinstance(path_to_folder_with_data, str) and isinstance(reverse, bool)):
        raise TypeError("first argument should be str, second bool")

    if driver is not None:
        return find_driver(driver, path_to_folder_with_data)

    message_list_to_print = []
    data, results = build_report(path_to_folder_with_data)
    sorted_results = [value for value in results.keys()]
    sorted_results.sort()

    for value in sorted_results:
        abbreviation = results[value]
        message_list_to_print.append([data[abbreviation]['name'], data[abbreviation]['car'], value])

    if reverse is False:
        return print_to_console(message_list_to_print)

    else:
        message_list_to_print.reverse()
        return print_to_console(message_list_to_print)


def main():
    """program entry point"""
    arguments_cli = parser_cli.main()

    path_to_folder = arguments_cli['files']
    driver = arguments_cli['driver']
    reverse_mode = True if arguments_cli['desc'] else False

    print(print_report(path_to_folder, reverse=reverse_mode, driver=driver))


if __name__ == "__main__":  # pragma: no cover
    main()
