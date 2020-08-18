import math


def utils_type(obj):
    t = type(obj)
    if t == dict:
        return 'dict'
    if t == list:
        return 'array'
    if t == int:
        return 'int'
    if t == float:
        return 'float'
    if t == str:
        return 'string'
    return str(t)


def utils_array_length(array):
    return len(array)


def utils_array_clone(array):
    return array.copy()


def utils_array_concat(array1, array2):
    if type(array1) != list:
        array1 = [array1]
    if type(array2) != list:
        array2 = [array2]
    return [*array1, *array2]


def utils_array_index_of(array, search):
    idx = array.index(search)
    if idx is None:
        return -1
    return idx


def utils_array_slice(array, slice_start, slice_stop, slice_step):
    return array[slice(slice_start, slice_stop, slice_step)]


def utils_object_has_key(object_val, key):
    return key in object_val
