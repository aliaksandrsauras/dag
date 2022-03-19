from random import uniform
from time import sleep

from dag.logs import log_timing


@log_timing
def sum_operator(params):
    return sum(params)


@log_timing
def max_operator(params):
    return max(params)


@log_timing
def min_operator(params):
    return min(params)


@log_timing
def random_sleep_operator(params):
    result = uniform(0, 5)
    sleep(result)
    return result


@log_timing
def zero_division(params):
    return 42 / 0


OPERATORS = {
    "sum": sum_operator,
    "max": max_operator,
    "min": min_operator,
    "sleep": random_sleep_operator,
    "exception": zero_division,
}
