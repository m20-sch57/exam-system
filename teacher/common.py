"""
Contains common functions and variables.
"""


import os
from PyQt5 import Qt


def return_lambda(function, *args, **kwargs):
    """
    Returns lambda: function(*args, **kwargs)
    """
    return lambda: function(*args, **kwargs)


def upper_question_style(question, current_question):
    """
    Returns style of current question depending on the result.
    """
    background_color = 'white'
    foreground_color = 'black'
    border_color = 'grey'
    if question == current_question:
        foreground_color = 'blue'
        background_color = '#CCE8FF'
        border_color = '#99D1FF'
    return (
        'color: ' + foreground_color + ';'
        'background: ' + background_color + ';'
        'border-style: solid;'
        'border-width: 1px;'
        'border-color: ' + border_color + ';'
        'border-radius: 5px;'
        'padding: 5px;'
        'font-size: 27px;'
    )


GREEN = '#6DC180'
RED = '#FF6643'
YELLOW = '#FFDB2D'
GREY = '#546A74'
USER = os.path.join('images', 'user.png')
EXAM30 = os.path.join('images', 'exam-30x30.png')
LEFT = os.path.join('images', 'left.png')
TICK = os.path.join('images', 'tick.png')
CROSS = os.path.join('images', 'cross.png')
SETTINGS = os.path.join('images', 'settings.png')
CREATE = os.path.join('images', 'create.png')
DELETE = os.path.join('images', 'delete.png')
