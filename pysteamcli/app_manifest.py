#!/usr/bin/env python3

"""
Parse Steam's application manifest files.
"""


import itertools


def next_data(it):
    """
    Advances an iterator until new data is found.

    :param it: Character iterator.
    :returns: Data found.
    """

    quotation_mark = lambda c: c != '"'

    data_begin = itertools.dropwhile(quotation_mark, it)
    next(data_begin)

    data = itertools.takewhile(quotation_mark, data_begin)
    return ''.join(data)


def next_scope(it):
    """
    Advances the iterator until a scope closing mark is found.

    :param it: Character iterator.
    :returns: The content of the scope.
    """

    s_counter = 0
    for i in it:
        if i == '{':
            s_counter += 1
        elif i == '}':
            if s_counter == 0:
                break
            else:
                s_counter -= 1
        yield i


def parse_acf_content(it):
    """
    Parse the content of an acf file.

    :param it: Character iterator.
    :returns: The content of an acf file as a dictionary.
    """

    result = list()
    while True:
        try:
            key = next_data(it)

            value_type = next(it)
            next(it)

            if value_type == '\t':
                # Data
                value = next_data(it)

            elif value_type == '\n':
                # Nested scope.
                value = parse_acf_content(next_scope(it))

            else:
                raise Exception

        except StopIteration:
            break

        result.append((key, value))

    return dict(result)


def parse_acf_file(file_path):
    """
    Parse an acf file.
    """

    with open(file_path, 'r') as acf_file:
        content = acf_file.read()
    return parse_acf_content(iter(content))
