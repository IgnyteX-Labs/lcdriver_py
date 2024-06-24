====
universal lcd driver
====
unilcdriver is a lightweight project aimed to provide an easy to use API to display text (and UIs) on an segment lcd display.
``unilcddriver_py`` is the python implementation.

Usage
====
Disclaimer
----
The general idea of the project is to simplify the creation of complicated text output on an lcd display of your choice.
This library however does not provide implementations for most lcd displays but rather an interface for you to implement.
In order to use this library you might need to write your implementation of a :py:class:`DisplayModule` for the library to work
with your lcd display.

command line module
----
To test your lcd display locally on your development machine, a sample commandline :py:class:`DisplayModule` is shipped with the
library. To use it initialize the library using
wallah

writing your own module
---
In order to write your own module you need to implement the :py:class:`DisplayModule` interface.
This DisplayModule only needs to give back its size and implement the :autofunction:`display_text_at_pos` method.
The :autofunction:`display_text_at_pos` method is called by the library to display text at a given position on the lcd display.

