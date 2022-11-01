import datetime
import pathlib

from parse_data import parseLog, parseAbbreviations
import parser_cli


def compare_start_end_time(data):
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


def merge_dicts(dict_one, dict_two, dict_third=None):
    new_dict = {}
    for abbreviation in dict_one:
        if dict_third:
            new_dict[abbreviation] = dict_one[abbreviation] | dict_two[abbreviation] | dict_third[abbreviation]
        else:
            new_dict[abbreviation] = dict_one[abbreviation] | dict_two[abbreviation]
    return new_dict


def build_report(path_to_data):

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


def print_report(path_to_folder_with_data, reverse=False):
    message_list_to_print = []
    data, results = build_report(path_to_folder_with_data)
    sorted_results = [value for value in results.keys()]
    sorted_results.sort()

    for value in sorted_results:
        abbreviation = results[value]
        message_list_to_print.append([data[abbreviation]['name'], data[abbreviation]['car'], value])

    if reverse is False:
        for num, value in enumerate(message_list_to_print):
            message = f"""{num:>3}. {value[0]:<20}| {value[1]:<25} | {value[2]}"""
            print(message, end='\n\n')
    else:
        message_list_to_print.reverse()
        for num, value in enumerate(message_list_to_print):
            message = f"""{num}. {value[0]:<20}| {value[1]:<25} | {value[2]}"""
            print(message, end='\n\n')


def main():
    arguments_cli = parser_cli.main()

    path_to_folder = pathlib.PosixPath(arguments_cli['files'])
    driver = arguments_cli['driver']
    reverse_mode = True if arguments_cli['desc'] else False

    if driver:
        pass
    else:
        print_report(path_to_folder, reverse=reverse_mode)


if __name__ == "__main__":
    main()
