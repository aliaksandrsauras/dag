import functools
import logging
import timeit

FMT = "[%(asctime)s] %(process)-5d %(levelname)-8s %(name)-75s:%(lineno)-3d %(message)s"


def init_console_logs_for_module(name, verbose=False):
    logger = logging.getLogger(name)
    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(FMT))
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


def log_timing(fn):
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        start = timeit.default_timer()
        ret = fn(*args, **kwargs)
        end = timeit.default_timer()
        logger = logging.getLogger(fn.__module__)
        logger.info(
            "'%s' from '%s' took %0.4f ms",
            fn.__qualname__,
            fn.__module__,
            (end - start) * 1000
        )
        return ret

    return wrapped
