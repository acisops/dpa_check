__version__ = "2.3.0"

from .dpa_check import \
    calc_model


def test(*args, **kwargs):
    """
    Run py.test unit tests.
    """
    import testr
    return testr.test(*args, **kwargs)
