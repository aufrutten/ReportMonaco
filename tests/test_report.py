from unittest.mock import patch
import pytest
import report


class TestCompareStartEndTime:

    def test_with_atypical_argument(self):
        with pytest.raises(TypeError):
            report.compare_start_end_time('123')

    def test_with_typical_argument(self):
        argument = {'SVF': {'start': {'date': '2018-05-24', 'time': '12:02:58.917'},
                            'end': {'date': '2018-05-24', 'time': '12:04:03.332'},
                            'name': 'Sebastian Vettel',
                            'car': 'FERRARI'
                            }
                    }

        result_zero = {'SVF': {'start': {'date': '2018-05-24', 'time': '12:02:58.917'},
                               'end': {'date': '2018-05-24', 'time': '12:04:03.332'},
                               'name': 'Sebastian Vettel',
                               'car': 'FERRARI',
                               'result': '0:01:04.415000'
                               }
                       }

        result_one = {'0:01:04.415000': 'SVF'}

        result_of_function = report.compare_start_end_time(argument)
        assert result_of_function[0] == result_zero
        assert result_of_function[1] == result_one


class TestMergeDicts:

    def test_with_atypical_argument(self):
        with pytest.raises(TypeError):
            report.merge_dicts('123', 123, [])

    def test_with_two_dicts(self):
        first_dict = {'TEST': {'name': 'ihor',
                               'age': 90,
                               }
                      }
        second_dict = {'TEST': {'family': 'Four',
                                'live': True}
                       }

        third_dict = {'TEST': {'sex': 'M',
                               'country': 'DE'}
                      }

        result = {'TEST': {'name': 'ihor',
                           'age': 90,
                           'family': 'Four',
                           'live': True,
                           'sex': 'M',
                           'country': 'DE'}
                  }

        assert report.merge_dicts(first_dict, second_dict, third_dict) == result


class TestFindDriver:

    def test_with_atypical_argument(self, tmp_path_with_files_more_exp):
        with pytest.raises(TypeError):
            report.find_driver(1231, tmp_path_with_files_more_exp)

    def test_to_find_driver(self, tmp_path_with_files):
        result = report.find_driver('Sebastian Vettel', tmp_path_with_files)
        assert result == '  1. Sebastian Vettel    | FERRARI                   | 0:01:04.415000'

    def test_while_driver_not_found(self, tmp_path_with_files):
        result = report.find_driver('Ihor', tmp_path_with_files)
        assert result == 'Driver not found'


class TestPrintToConsole:

    def test_print_function(self, capsys):
        test_list = [['Aufrutten Ihor', 'AUDI A5', '0:01:03.321']]
        result = report.print_to_console(test_list)
        assert result == '  1. Aufrutten Ihor      | AUDI A5                   | 0:01:03.321'


class TestBuildReport:

    def test_with_atypical_argument(self):
        with pytest.raises(TypeError):
            report.build_report(123)

    def test_with_argument_str(self, tmp_path_with_files):
        result_zero = {'SVF': {'start': {'date': '2018-05-24', 'time': '12:02:58.917'},
                               'end': {'date': '2018-05-24', 'time': '12:04:03.332'},
                               'name': 'Sebastian Vettel',
                               'car': 'FERRARI',
                               'result': '0:01:04.415000'}
                       }

        result_one = {'0:01:04.415000': 'SVF'}
        result_of_function = report.build_report(str(tmp_path_with_files))
        assert result_of_function[0] == result_zero
        assert result_of_function[1] == result_one


class TestPrintReport:

    def test_with_atypical_argument(self):
        with pytest.raises(TypeError):
            report.print_report(123, {})

    def test_with_correct_argument(self, tmp_path_with_files):
        result = report.print_report(str(tmp_path_with_files))
        assert result == '  1. Sebastian Vettel    | FERRARI                   | 0:01:04.415000'

    def test_with_reverse_mode(self, tmp_path_with_files_more_exp):
        result = report.print_report(str(tmp_path_with_files_more_exp), reverse=True).split('\n\n')[0]
        assert result == '  1. Lewis Hamilton      | MERCEDES                  | 0:06:47.540000'


class TestMain:

    @patch('report.parser_cli.main')
    def test_main(self, mock_func, tmp_path_with_files_more_exp, capsys):

        # first case
        mock_func.return_value = {'files': str(tmp_path_with_files_more_exp), 'driver': None, 'desc': None}
        report.main()
        out, err = capsys.readouterr()
        assert str(out).split('\n\n')[0] == '  1. Sebastian Vettel    | FERRARI                   | 0:01:04.415000'

        # second case
        mock_func.return_value = {'files': str(tmp_path_with_files_more_exp), 'driver': None, 'desc': True}
        report.main()
        out, err = capsys.readouterr()
        assert str(out).split('\n\n')[0] == '  1. Lewis Hamilton      | MERCEDES                  | 0:06:47.540000'

        # third case
        mock_func.return_value = {'files': str(tmp_path_with_files_more_exp), 'driver': 'Lewis Hamilton', 'desc': True}
        report.main()
        out, err = capsys.readouterr()
        assert out == '  1. Lewis Hamilton      | MERCEDES                  | 0:06:47.540000\n'

