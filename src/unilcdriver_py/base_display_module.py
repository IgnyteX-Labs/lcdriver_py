"""
Base class and utilities for a DisplayModule
"""
from __future__ import annotations

import abc

from typing import List, Tuple

from .version import version


class DisplaySize:
    """
    Defines the size of a display
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        """
        Create a new DisplaySize, 20x4 for example
        :param x: x size (size 10 means 0-9 are valid)
        :param y: y size (size 10 means 0-9 are valid)
        """
        self.x = x
        self.y = y


class ContentWriteable(abc.ABC):
    @abc.abstractmethod
    def display(self, pos: Tuple[int, int], content: str):
        """
        Display text at a specific position
        A position of (0, 0) will replace the first character of the first line.
        :param pos: Position to start displaying text at (x, y) (cursor)
        :param content: Content to display
        :raises OutOfBoundsException: If the position is out of bounds
        :return:
        """
        pass


class DisplaySnapshot(ContentWriteable):
    """
    A class defining what is currently being displayed on the display
    You can write to this snapshot and change the content but the changes wont get applied until apply() is called.
    """
    content: List[str]
    module: DisplayModule

    def __init__(self, content: List[str], display: DisplayModule):
        """
        Initialize a new DisplayContent class holding the current state of the display
        :param content:
        """
        self.content = content
        self.module = display

    def display(self, pos: Tuple[int, int], content: str):
        """
        Display text at a specific position
        A position of (0, 0) will replace the first character of the first line.
        :param pos: Position to start displaying text at (x, y) (cursor)
        :param content: Content to display
        :raises OutOfBoundsException: If the position is out of bounds
        :return:
        """
        if pos[1] < 0 or pos[1] < self.module.size.y:
            raise OutOfBoundsException(f"Cursor y is out of bounds. Must be between 0 and {self.module.size.y - 1}.")
        if pos[0] < 0 or pos[0] < self.module.size.x:
            raise OutOfBoundsException(f"Cursor x is out of bounds. Must be between 0 and {self.module.size.x - 1}.")
        self.content[pos[1]] = (
                self.content[pos[1]][:pos[0]] +  # content that was there before
                content[:self.module.size.x - pos[0]] +  # new content
                self.content[pos[1]][pos[0] + len(content):]  # previous content
        )

    def apply(self):
        """
        Apply the content back to the display
        :return:
        """
        list(map(lambda item: self.module.display_text_at_pos(item[0], item[1]), enumerate(self.content)))
        self.module.content = self.content


class DisplayModule(ContentWriteable):
    """
    A DisplayModule defines the basic functionality of an lcd
    This contains basic methods for displaying content on the lcd but no complex formatting operations.
    """
    size: DisplaySize
    content: List[str]

    def __init__(self, size: DisplaySize):
        """
        Initialize the display
        :param size: Size of the display
        :return:
        """
        self.size = size
        self.content = ["" for _ in range(size.y)]

    def get_snapshot(self) -> DisplaySnapshot:
        """
        Get a description of the current screen contents
        :return:
        """
        return DisplaySnapshot(self.content, self)

    @abc.abstractmethod
    def display_text_at_pos(self, pos: Tuple[int, int], content: str):
        """
        Display text on a line of the display. Replace the content at the specified position.
        It is guaranteed that the parameters will be in bounds. Content & position will be within the specified size.
        Do not use this method directly. Use display() with the same parameters since it will check bounds and more.
        :param pos: Position to start displaying text at (x, y)
        :param content: Content to display (0-size.x)
        :return:
        """

    def display(self, pos: Tuple[int, int], content: str):
        """
        Display text at a specific position (safe to use directly).
        A position of (0, 0) will replace the first character of the first line.
        This method will check if the parameters are in bound and will update the content of the display
        :param pos: Position to start displaying text at (x, y) (cursor)
        :param content: Content to display
        :raises OutOfBoundsException: If the position is out of bounds
        :return:
        """
        if pos[1] < 0 or pos[1] < self.size.y:
            raise OutOfBoundsException(f"Cursor y is out of bounds. Must be between 0 and {self.size.y - 1}.")
        if pos[0] < 0 or pos[0] < self.size.x:
            raise OutOfBoundsException(f"Cursor x is out of bounds. Must be between 0 and {self.size.x - 1}.")
        tmp = self.content[pos[1]]  # content before
        self.content[pos[1]] = (
                self.content[pos[1]][:pos[0]] +
                content[:self.size.x - pos[0]] +
                self.content[pos[1]][pos[0] + len(content):]
        )
        if tmp != self.content[pos[1]]:
            # Only call if changes have been detected
            self.display_text_at_pos(pos, content)


class OutOfBoundsException(Exception):
    """
    Exception raised when a display is out of bounds
    """
