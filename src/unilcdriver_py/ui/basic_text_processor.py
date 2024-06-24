"""
The basic text processor is just a "higher level wrapper" to the basic DisplayModule.
It does not do complicated UI operations.
This kind of serves as a middle layer between DisplayModule and the UI API.
"""

from unilcdriver_py.base_display_module import DisplayModule
from typing import List


def clear(module: DisplayModule, line: int = None):
    """
    Clear a line (None for all)
    Don't clear lines before writing to them, rather overwrite them!
    :param module: DisplayModule to display text on
    :param line: Line to clear
    :return:
    """
    [module.display((0, y), " " * module.size.x) for y in range(module.size.y)] if line is None \
        else module.display((0, line), " " * module.size.x)


def right(module: DisplayModule, line: int, content: str):
    """
    Display content on the right side of the display
    :param module: DisplayModule to display text on
    :param line: Line to display at
    :param content: Content to display on the right side
    :return:
    """
    # Figure out at which char to start writing at
    start = module.size.x - len(content)
    # display the padded content
    module.display((start, line), content)


def left(module: DisplayModule, line: int, content: str):
    """
    Display content on the left side of the display
    :param module: DisplayModule to display text on
    :param line: Line to display at
    :param content: Content to display
    :return:
    """
    # display the padded content
    module.display((0, line), content)


def center(module: DisplayModule, line: int, content: str):
    """
    Display a text centered on a specific line
    :param module: DisplayModule to display text on
    :param line: Line to display text at
    :param content: Content to display
    :return:
    """
    # Figure out at which position to start writing content at
    start = min(module.size.x // 2 - len(content) // 2, 0)
    # display the padded content
    module.display((start, line), content)


def display_multiple_centered(module: DisplayModule, line: int, content: List[str]):
    """
    Display multiple small parts of text centered on a specific line
    :param module: DisplayModule to display text on
    :param line: Line to display content on
    :param content: Text content to display
    :return:
    """
    if len(content) == 1:
        center(module, line, content[0])
        return
    length = sum([len(bit) for bit in content])
    space_available = module.size.x - length
    space_between = space_available // (len(content) + 1)
    # +1 because we need -1 space between the bits but +2 spaces at the start and end = +1
    centered_content = " " * space_between + (" " * space_between).join(content) + " " * space_between
    module.display((0, line), centered_content)


def display_multiple_stretched(module: DisplayModule, line: int, content: List[str]):
    """
    Display multiple small parts of text stretched on a specific line
    :param module: DisplayModule to display text on
    :param line: Line to display content on
    :param content: Text content to display
    :return:
    """
    if len(content) == 1:
        center(module, line, content[0])
        return
    length = sum([len(bit) for bit in content])
    space_available = module.size.x - length
    space_between = space_available // (len(content) - 1)
    # we need -1 space between the bits (xy space xy = 1 space with 2 xy)
    module.display((0, line), (" " * space_between).join(content))


def left_right(module: DisplayModule, line: int, left: str, right: str):
    """
    Display content on the left and right side of the display
    :param module: DisplayModule to display text on
    :param line: The line to display at
    :param left: Content of left side of display
    :param right: Content of right side of display
    :return:
    """
    display_multiple_stretched(module, line, [left, right])

def line(module: DisplayModule, line: int):
    """
    Display a simple line on the display
    :param module: DisplayModule to display text on
    :param line: The line to display at
    :return:
    """
    module.display((0, line), "-" * module.size.x)
