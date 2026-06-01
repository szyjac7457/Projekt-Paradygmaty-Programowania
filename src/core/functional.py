from functools import reduce


def pipe(*fns):
    return lambda x: reduce(lambda v, f: f(v), fns, x)


def compose(*fns):
    return lambda x: reduce(lambda v, f: f(v), reversed(fns), x)
