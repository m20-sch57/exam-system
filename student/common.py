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


def get_question_style(question_data, question=None, current_question=None):
    """
    Returns style of current question depending on the result.
    """
    background_color = 'white'
    foreground_color = 'black'
    border_color = 'grey'
    if question_data['score'] == '-1':
        main_color = YELLOW
        main_picture = None
        background_color = '#FFFA95'
    elif question_data['score'] == question_data['maxscore']:
        main_color = GREEN
        main_picture = Qt.QPixmap(TICK)
        background_color = '#9CFB8E'
    else:
        main_color = RED
        main_picture = Qt.QPixmap(CROSS)
        background_color = '#F94D51'
    if question_data['score'] is False:
        background_color = 'white'
    if question == current_question:
        foreground_color = 'blue'
        background_color = '#CCE8FF'
        border_color = '#99D1FF'
    return {
        'background_color': background_color,
        'foreground_color': foreground_color,
        'border_color': border_color,
        'main_color': main_color,
        'main_picture': main_picture
    }


GREEN = '#6DC180'
RED = '#FF6643'
YELLOW = '#FFDB2D'
GREY = '#546A74'
EXAM30 = os.path.join('images', 'exam-30x30.png')
LEFT = os.path.join('images', 'left.png')
TICK = os.path.join('images', 'tick.png')
CROSS = os.path.join('images', 'cross.png')
SETTINGS = os.path.join('images', 'settings.png')
