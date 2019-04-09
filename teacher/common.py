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


def upper_question_style(equal):
    """
    Returns style of current question depending on the result.
    """
    background_color = 'white'
    foreground_color = 'black'
    border_color = 'grey'
    if equal:
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


def main_question_style(question_result):
    """
    Returns main style of current question depending on the result.
    """
    if not question_result:
        main_color = RED
        main_picture = Qt.QPixmap(CROSS)
    elif question_result['share'] == -1:
        main_color = YELLOW
        main_picture = Qt.QPixmap(WARNING)
    elif question_result['share'] == 1:
        main_color = GREEN
        main_picture = Qt.QPixmap(TICK)
    else:
        main_color = RED
        main_picture = Qt.QPixmap(CROSS)
    return {
        'main_color': main_color,
        'main_picture': main_picture
    }


def get_question_details(question_result):
    """
    Returns score and last answer.
    """
    if not question_result:
        score = '0'
        answer = ''
    elif question_result['share'] == -1:
        score = '?'
        answer = question_result['answer']
    else:
        score = str(question_result['score'])
        answer = question_result['answer']
    return {
        'score': score,
        'answer': answer
    }


GREEN = '#6DC180'
RED = '#FF6643'
YELLOW = '#FFA500'
GREY = '#546A74'
USER = os.path.join('images', 'user.png')
EXAM30 = os.path.join('images', 'exam-30x30.png')
LEFT = os.path.join('images', 'left.png')
TICK = os.path.join('images', 'tick.png')
CROSS = os.path.join('images', 'cross.png')
WARNING = os.path.join('images', 'warning.png')
SETTINGS = os.path.join('images', 'settings.png')
CREATE = os.path.join('images', 'create.png')
DELETE = os.path.join('images', 'delete.png')
SAVE = os.path.join('images', 'save.png')
UPDATE = os.path.join('images', 'update.png')
