"""
Upgrades exams from older version.
"""


import os
import sys
from xmlrpc.client import ServerProxy


class Item:
    """
    Item with items that should be saved on disk.
    """
    def __init__(self, path):
        self.path = path

    def set_item(self, item, value):
        """
        Sets value of the item.
        """
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        open(os.path.join(self.path, item), 'w', encoding=ENCODING).write(str(value))

    def get_item(self, item):
        """
        Gets value of the item.
        """
        if not os.path.isfile(os.path.join(self.path, item)):
            return False
        return open(os.path.join(self.path, item), encoding=ENCODING).read()


def upgrade_exams(folder):
    """
    Upgrades all exams in this folder.
    """
    out = sys.stdout
    #out = open('UpgradeLog.txt', 'w', encoding=ENCODING)
    out.write('Starting upgrade process.\n')
    exams = os.listdir(folder)
    out.write('Discovered exams:\n')
    out.write('\n'.join(exams))
    out.write('\n')
    for exam in exams:
        out.write(exam + ':\n')
        exam_id = SERVER.create_exam(1)
        settings_item = Item(os.path.join(folder, exam, 'settings'))
        out.write('name=' + exam + ', ' +
                  'duration=' + settings_item.get_item('duration') + ', ' +
                  'published=' + settings_item.get_item('published') + ', ' +
                  'rowid=' + str(exam_id) + '.\n')
        SERVER.set_exam_data({
            'name': exam,
            'duration': int(settings_item.get_item('duration')),
            'published': int(settings_item.get_item('published')),
            'rowid': exam_id
        })
        for question in range(len(os.listdir(os.path.join(folder, exam))) - 1):
            question_item = Item(os.path.join(folder, exam, str(question + 1)))
            question_id = SERVER.create_question(exam_id, question_item.get_item('type'))
            out.write('question #' + str(question + 1) + ': ')
            out.write('type=' + question_item.get_item('type') + '\n')
            if question_item.get_item('type') == 'Short':
                SERVER.set_question_data({
                    'type': 'Short',
                    'statement': question_item.get_item('statement'),
                    'correct': question_item.get_item('correct').replace('\n', '; '),
                    'maxsubs': 1,
                    'maxscore': int(question_item.get_item('maxscore')),
                    'rowid': question_id
                })
                out.write('OK\n')
            elif question_item.get_item('type') == 'Long':
                SERVER.set_question_data({
                    'type': 'Long',
                    'statement': question_item.get_item('statement'),
                    'correct': '',
                    'maxsubs': 1000,
                    'maxscore': int(question_item.get_item('maxscore')),
                    'rowid': question_id
                })
                out.write('OK\n')
            else:
                out.write('ERROR: Undefined type\n')
    out.write('Upgrade process completed.\n')


ENCODING = 'utf-8-sig'
SERVER = ServerProxy('http://127.0.0.1:8000')
upgrade_exams('exams')
