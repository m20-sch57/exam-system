"""
Examiner project, server module.
"""


import os
import time
from xmlrpc.server import SimpleXMLRPCServer


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


def format_str(string):
    """
    Formats string: lowers letters and removes all other symbols except numbers.
    """
    string = string.lower()
    string = string.replace('ё', 'е')
    string = ''.join([c for c in string if c.isalnum()])
    return string


def ping():
    """
    Ping.
    """
    return True


def register_student(group, user, password):
    """
    Tries to register the student.
    """
    if not group in os.listdir('data'):
        return False
    if user in os.listdir(os.path.join('data', group, 'students')) or not user:
        return False
    user_item = Item(os.path.join('data', group, 'students', user, 'info'))
    user_item.set_item('password', password)
    return True


def register_teacher(group, user, password):
    """
    Tries to register the teacher.
    """
    if not group in os.listdir('data'):
        return False
    if user in os.listdir(os.path.join('data', group, 'teachers')) or not user:
        return False
    user_item = Item(os.path.join('data', group, 'teachers', user, 'info'))
    user_item.set_item('password', password)
    return True


def login_student(group, user, password):
    """
    Tries to login the student.
    """
    if not group in os.listdir('data'):
        return False
    if not user in os.listdir(os.path.join('data', group, 'students')):
        return False
    user_item = Item(os.path.join('data', group, 'students', user, 'info'))
    if user_item.get_item('password') != password:
        return False
    return True


def login_teacher(group, user, password):
    """
    Tries to login the teacher.
    """
    if not group in os.listdir('data'):
        return False
    if not user in os.listdir(os.path.join('data', group, 'teachers')):
        return False
    user_item = Item(os.path.join('data', group, 'teachers', user, 'info'))
    if user_item.get_item('password') != password:
        return False
    return True


def list_of_exams(group):
    """
    Returns list of all available exams in the group.
    """
    return os.listdir(os.path.join('data', group, 'exams'))


def get_question(group, user, exam, question):
    """
    Returns the question data.
    """
    question_item = Item(os.path.join('data', group, 'exams', exam, str(question)))
    answer_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, str(question)))
    if question_item.get_item('type') == 'Short':
        return {'type': question_item.get_item('type'),
                'statement': question_item.get_item('statement'),
                'correct': question_item.get_item('correct'),
                'maxscore': question_item.get_item('maxscore'),
                'answer': answer_item.get_item('answer'),
                'score': answer_item.get_item('score')}
    elif question_item.get_item('type') == 'Long':
        return {'type': question_item.get_item('type'),
                'statement': question_item.get_item('statement'),
                'maxscore': question_item.get_item('maxscore'),
                'answer': answer_item.get_item('answer'),
                'score': answer_item.get_item('score')}


def get_exam(group, user, exam):
    """
    Returns all question data in the exam.
    """
    quantity = len(os.listdir(os.path.join('data', group, 'exams', exam))) - 1
    exam_data = [get_question(group, user, exam, question) for question in range(1, quantity + 1)]
    return exam_data


def get_exam_info(group, user, exam):
    """
    Returns exam's info: start time, duration time, total student's score, total maximum score.
    """
    exam_item = Item(os.path.join('data', group, 'exams', exam, 'settings'))
    user_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, 'settings'))
    exam_data = get_exam(group, user, exam)
    quantity = len(os.listdir(os.path.join('data', group, 'exams', exam))) - 1
    if user_item.get_item('start') is False:
        state = 'Not started'
    elif int(time.time()) < int(user_item.get_item('end')):
        state = 'Running'
    else:
        state = 'Finished'
    total_score = 0
    total_maxscore = 0
    for question in range(1, len(exam_data) + 1):
        question_data = exam_data[question - 1]
        if question_data['score'] is not False:
            total_score += max(int(question_data['score']), 0)
        if question_data['maxscore'] is not False:
            total_maxscore += int(question_data['maxscore'])
    return {'state': state,
            'duration': exam_item.get_item('duration'),
            'start': user_item.get_item('start'),
            'end': user_item.get_item('end'),
            'quantity': quantity,
            'total_score': total_score,
            'total_maxscore': total_maxscore}


def start_exam(group, user, exam):
    """
    Starts the exam.
    """
    exam_item = Item(os.path.join('data', group, 'exams', exam, 'settings'))
    user_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, 'settings'))
    current_time = int(time.time())
    duration_time = int(exam_item.get_item('duration')) * 60
    user_item.set_item('start', current_time)
    user_item.set_item('end', current_time + duration_time)
    return True


def finish_exam(group, user, exam):
    """
    Finishes the exam.
    """
    user_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, 'settings'))
    current_time = int(time.time())
    user_item.set_item('end', current_time)
    exam_data = get_exam(group, user, exam)
    for question in range(1, len(exam_data) + 1):
        if exam_data[question - 1]['score'] == '-1':
            # TODO: add notification to teacher
            print("adding notification of question " + str(question))
    return True


def save_answer(group, user, exam, question, answer):
    """
    Saves student's answer.
    """
    answer_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, str(question)))
    answer_item.set_item('answer', answer)
    return True


def check(group, user, exam, question):
    """
    Checks student's answer to the short question.
    """
    question_item = Item(os.path.join('data', group, 'exams', exam, str(question)))
    answer_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, str(question)))
    if question_item.get_item('type') == 'Short':
        answer = answer_item.get_item('answer')
        correct = question_item.get_item('correct').split('\n')
        if format_str(answer) in [format_str(s) for s in correct]:
            answer_item.set_item('score', question_item.get_item('maxscore'))
        else:
            answer_item.set_item('score', 0)
    elif question_item.get_item('type') == 'Long':
        answer_item.set_item('score', -1)
    return True


ENCODING = 'utf-8-sig'
SERVER = SimpleXMLRPCServer(('', 8000))
SERVER.register_function(ping)
SERVER.register_function(register_student)
SERVER.register_function(register_teacher)
SERVER.register_function(login_student)
SERVER.register_function(login_teacher)
SERVER.register_function(list_of_exams)
SERVER.register_function(get_question)
SERVER.register_function(get_exam)
SERVER.register_function(get_exam_info)
SERVER.register_function(start_exam)
SERVER.register_function(finish_exam)
SERVER.register_function(save_answer)
SERVER.register_function(check)
SERVER.serve_forever()
