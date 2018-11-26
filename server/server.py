"""
Examiner project, server.
Version 1.0
"""

import os
import time
from xmlrpc.server import SimpleXMLRPCServer


class Item:
    """
    Item with attributes that should be saved on disk.
    """
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)

    def set_attr(self, attr, value):
        """
        Sets value of the attribute.
        """
        open(os.path.join(self.path, attr), 'w', encoding=ENCODING).write(str(value))

    def get_attr(self, attr):
        """
        Gets value of the attribute.
        """
        if not os.path.isfile(os.path.join(self.path, attr)):
            return False
        return open(os.path.join(self.path, attr), encoding=ENCODING).read()


def format_str(string):
    """
    Formats string: lowers letters and removes all other symbols except numbers.
    """
    # string = string.lower()
    # string = string.replace('ё', 'е')
    # string = ''.join([c for c in string if c.isalnum()])
    # TODO: configure!
    return string


def login(group, user, password):
    """
    Checks if the user is valid.
    """
    if not group in os.listdir('groups'):
        return False
    if not user in os.listdir(os.path.join('groups', group, 'users')):
        return False
    # TODO: add password verification
    return True


def list_of_exams(group):
    """
    Returns list of all available exams in the group.
    """
    return os.listdir(os.path.join('groups', group, 'exams'))


def get_question(group, user, exam, question):
    """
    Returns the question data.
    """
    question_item = Item(os.path.join('groups', group, 'exams', exam, str(question)))
    answer_item = Item(os.path.join('groups', group, 'users', user, exam, str(question)))
    return {'type': question_item.get_attr('type'),
            'statement': question_item.get_attr('statement'),
            'correct': question_item.get_attr('correct'),
            'maxscore': question_item.get_attr('maxscore'),
            'answer': answer_item.get_attr('answer'),
            'score': answer_item.get_attr('score')}


def get_exam(group, user, exam):
    """
    Returns all question data in the exam.
    """
    quantity = len(os.listdir(os.path.join('groups', group, 'exams', exam))) - 1
    exam_data = [get_question(group, user, exam, question) for question in range(1, quantity + 1)]
    return exam_data


def get_exam_info(group, user, exam):
    """
    Returns exam's info: start time, duration time, total student's score, total maximum score.
    """
    exam_item = Item(os.path.join('groups', group, 'exams', exam, 'settings'))
    user_item = Item(os.path.join('groups', group, 'users', user, exam, 'settings'))
    exam_data = get_exam(group, user, exam)
    quantity = len(os.listdir(os.path.join('groups', group, 'exams', exam))) - 1
    if user_item.get_attr('start') is False:
        state = 'Not started'
    elif int(time.time()) < int(user_item.get_attr('end')):
        state = 'Running'
    else:
        state = 'Finished'
    total_score = 0
    total_maxscore = 0
    for question in range(1, len(exam_data) + 1):
        question_data = exam_data[question - 1]
        if question_data['score'] is not False:
            total_score += int(question_data['score'])
        if question_data['maxscore'] is not False:
            total_maxscore += int(question_data['maxscore'])
    return {'state': state,
            'duration': exam_item.get_attr('duration'),
            'start': user_item.get_attr('start'),
            'end': user_item.get_attr('end'),
            'quantity': quantity,
            'total_score': total_score,
            'total_maxscore': total_maxscore}


def start_exam(group, user, exam):
    """
    Starts the exam.
    """
    exam_item = Item(os.path.join('groups', group, 'exams', exam, 'settings'))
    user_item = Item(os.path.join('groups', group, 'users', user, exam, 'settings'))
    current_time = int(time.time())
    duration_time = int(exam_item.get_attr('duration')) * 60
    user_item.set_attr('start', current_time)
    user_item.set_attr('end', current_time + duration_time)
    return True


def finish_exam(group, user, exam):
    """
    Finishes the exam.
    """
    user_item = Item(os.path.join('groups', group, 'users', user, exam, 'settings'))
    current_time = int(time.time())
    user_item.set_attr('end', current_time)
    return True


def save_answer(group, user, exam, question, answer):
    """
    Saves student's answer.
    """
    answer_item = Item(os.path.join('groups', group, 'users', user, exam, str(question)))
    answer_item.set_attr('answer', answer)
    return True


def check(group, user, exam, question):
    """
    Checks student's answer to the short question.
    """
    question_item = Item(os.path.join('groups', group, 'exams', exam, str(question)))
    answer_item = Item(os.path.join('groups', group, 'users', user, exam, str(question)))
    if question_item.get_attr('type') == 'Short':
        answer = answer_item.get_attr('answer')
        correct = question_item.get_attr('correct')
        if format_str(answer) == format_str(correct):
            answer_item.set_attr('score', 1)
        else:
            answer_item.set_attr('score', 0)
    # TODO: add more types!
    return True


ENCODING = 'utf-8-sig'
SERVER = SimpleXMLRPCServer(('', 8000))
SERVER.register_function(login)
SERVER.register_function(list_of_exams)
SERVER.register_function(get_question)
SERVER.register_function(get_exam)
SERVER.register_function(get_exam_info)
SERVER.register_function(start_exam)
SERVER.register_function(finish_exam)
SERVER.register_function(save_answer)
SERVER.register_function(check)
SERVER.serve_forever()
