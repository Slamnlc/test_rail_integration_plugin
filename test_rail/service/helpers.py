import os
from typing import List


def split_list(elements: List, separator: int) -> List[List]:
    """
    Split list by parts
    :param elements: list of elements
    :param separator: int value
    :return: list of lists
    """
    result, index = [], 0
    while True:
        result.append(elements[index:index + separator])
        index += separator
        if index >= len(elements):
            break
    return result


def get_env(key: str, default_value=None):
    """
    Function for getting environment variable with boolean value
    :param key: name of environment variable
    :param default_value: default value
    :return:
    """
    variable_value = os.getenv(key, default_value)
    tmp_var = str(variable_value).lower()
    if tmp_var == 'true':
        return True
    elif tmp_var == 'false':
        return False
    else:
        return variable_value
