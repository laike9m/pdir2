# Copied from http://stackoverflow.com/a/3681323/2142577.
def get_dict_attr(obj, attr):
    for obj in [obj] + list(obj.__class__.__mro__):
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    raise AttributeError


def is_descriptor(obj):
    return (hasattr(obj, "__get__") or
            hasattr(obj, "__set__") or
            hasattr(obj, "__delete__"))


class Incrementer(object):
    """Class that generates incremental int values.

    auto() in enum/aenum module is not guaranteed to generate incremental
    values, that's why this class is needed.
    """
    __value = -1

    @classmethod
    def auto(cls):
        cls.__value += 1
        return cls.__value
