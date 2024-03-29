from typing import Dict

from ftg.exceptions import JSONParseException


def read_int_value(dict_: Dict,
                   key: str,
                   default_value: int) -> int:
    return read_value_of_type(dict_,
                              key,
                              default_value,
                              int)


def read_str_value(dict_: Dict,
                   key: str,
                   default_value: str) -> str:
    return read_value_of_type(dict_,
                              key,
                              default_value,
                              str)


def read_bool_value(dict_: Dict,
                    key: str,
                    default_value: bool) -> bool:
    return read_value_of_type(dict_,
                              key,
                              default_value,
                              bool)


def read_value_of_type(dict_: Dict,
                       key: str,
                       default_value,
                       expected_type):
    if key in dict_.keys():
        value = dict_[key]
    else:
        value = default_value

    if type(value) is not expected_type:
        raise JSONParseException(F"Wrong type for \"{key}\". "
                                 F"Expected {expected_type.__name__} but got {type(value).__name__}")

    return value
