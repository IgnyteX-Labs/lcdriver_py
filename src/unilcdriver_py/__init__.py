"""Display complicated text output on any lcd"""
from .base_display_module import DisplayModule
from .version import version


__all__ = ["version", "DisplayModule", "use"]


def use(new_module: DisplayModule) -> LCDriverInstance:
    """
    Use a specific display module
    :param new_module: The new module to use
    :return:
    """
    return LCDriverInstance(new_module)
