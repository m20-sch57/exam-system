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


def upper_question_style(question_result, equal):
    """
    Returns style of current question on the upper panel depending on the result.
    """
    if not question_result:
        background_color = 'white'
    elif question_result['share'] == -1:
        background_color = '#FFFA95'
    elif question_result['share'] == 1:
        background_color = '#9CFB8E'
    else:
        background_color = '#F94D51'
    if equal:
        foreground_color = 'blue'
        background_color = '#CCE8FF'
        border_color = '#99D1FF'
    else:
        foreground_color = 'black'
        border_color = 'grey'
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


def get_question_details(question_results):
    """
    Returns score and last answer.
    """
    if not question_results:
        score = '0'
        answer = ''
    elif question_results['share'] == -1:
        score = '?'
        answer = question_results['answer']
    else:
        score = str(question_results['score'])
        answer = question_results['answer']
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
