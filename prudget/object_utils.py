from collections import OrderedDict


def is_partial_arg(partial, arg):
    partial = partial.strip()
    if partial == '':
        return False

    return arg.startswith(partial)


def infer_dictionary(dictionary, keys):
    keys.sort()
    dictionary = OrderedDict(dictionary)

    result = {}
    for candidate in dictionary.keys():
        for key in keys:
            if is_partial_arg(candidate, key):
                result[key] = dictionary[candidate]

    return result
