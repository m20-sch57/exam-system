"""
Contains common functions and variables.
"""


import os
from PyQt5 import Qt


def get_status(score, maxscore):
    """
    Returns color and picture depending on the result.
    """
    if score == 'Неизв.':
        return {'color': YELLOW1}
    elif score == maxscore:
        return {'color': GREEN1,
                'picture': Qt.QPixmap(TICK50)}
    else:
        return {'color': RED1,
                'picture': Qt.QPixmap(CROSS50)}


GREEN1 = '#6FCB36'
GREEN2 = '#9CFB8E'
YELLOW1 = '#E8DC00'
YELLOW2 = '#FFFA95'
RED1 = '#F10608'
RED2 = '#F94D51'
BLUE1 = '#2EBACB'
LEFT50 = os.path.join('images', 'left-50x50.png')
RIGHT50 = os.path.join('images', 'right-50x50.png')
TICK50 = os.path.join('images', 'tick-50x50.png')
CROSS50 = os.path.join('images', 'cross-50x50.png')
EXAM30 = os.path.join('images', 'exam-30x30.png')
