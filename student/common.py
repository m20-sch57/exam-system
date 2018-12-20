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
        return {'color': '#E8DC00'}
    elif score == maxscore:
        return {'color': '#6FCB36',
                'picture': Qt.QPixmap(TICK50)}
    else:
        return {'color': '#F10608',
                'picture': Qt.QPixmap(CROSS50)}


LEFT50 = os.path.join('images', 'left-50x50.png')
RIGHT50 = os.path.join('images', 'right-50x50.png')
TICK50 = os.path.join('images', 'tick-50x50.png')
CROSS50 = os.path.join('images', 'cross-50x50.png')
EXAM30 = os.path.join('images', 'exam-30x30.png')
