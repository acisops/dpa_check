import ska_helpers

__version__ = ska_helpers.get_version(__package__)

from .dpa_check import \
    DPACheck, main, \
    model_path


def test(*args, **kwargs):
    """
    Run py.test unit tests.
    """
    import testr
    if kwargs.get("answer_store", False) and '--answer_store' not in args:
        args += ("--answer_store",)
        kwargs.pop("answer_store")
    return testr.test(*args, **kwargs)

