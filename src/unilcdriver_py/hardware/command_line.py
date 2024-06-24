"""
A command line display emulator
"""
from src.unilcdriver_py.base_display_module import DisplayModule, DisplaySize
from src.unilcdriver_py.version import version as lib_version
from sys import stdout

from typing import Tuple


class CommandLineDisplay(DisplayModule):
    """
    A command line display emulator
    """

    def __init__(self, size: DisplaySize = DisplaySize(64, 4), application: str = "unilcdriver",
                 application_version: str = None):
        """
        Initialize the command line display module. You won't be able to use print calls.
        :param application: Name of your application, will be displayed at the top of the command line display
        :param application_version: Version of your application, will be displayed at the top of the command line display
        """
        super().__init__(size)

        # Print the application name and version
        print(f"{application} v{-lib_version if application_version is None else application_version} "
              f"LCD emulator")

        # Print the basic display output
        for i in range(size.y + 1 + 1):  # +1 because "line 0" is also a line
            # and +1 because we want to print one clear line at the start
            print(" " * (size.x + 1))  # print +1 because at pos 0 there is also a character

        # Print the bottom line
        print(f"size: {self.size.x}x{self.size.y} -"
              f" {"=)" if application_version is None else "uld:v" + lib_version}", end="")
        print("\033[F")
        stdout.flush()

    def display_text_at_pos(self, pos: Tuple[int, int], content: str):
        """
        Update a line in the command lines
        :param pos: Position to start displaying text at (x, y) (cursor)
        :param content: Content to display
        :return:
        """
        # Move the cursor to the correct position and then print the content to the line
        # Move the cursor size.y - 1 - pos[1] lines up
        print(("\033[A" * (self.size.y-1 - pos[1])) + "\x1b[2K")
        # move pos[0] characters to the right
        print(f"\r{' ' * pos[0]}{content[:self.size.x - pos[0]]}")
        # move cursor back down
        print(("\033[B" * (self.size.y - pos[1] - 2)))
