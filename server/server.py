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


def get_question_data(group, exam, question):
    """
    Returns question data.
    """
    question_item = Item(os.path.join('data', group, 'exams', exam, str(question)))
    if question_item.get_item('type') == 'Short':
        return {
            'type': question_item.get_item('type'),
            'statement': question_item.get_item('statement'),
            'correct': question_item.get_item('correct'),
            'maxscore': question_item.get_item('maxscore')
        }
    elif question_item.get_item('type') == 'Long':
        return {
            'type': question_item.get_item('type'),
            'statement': question_item.get_item('statement'),
            'maxscore': question_item.get_item('maxscore')
        }
    else:
        return {}


def get_question_data_user(group, user, exam, question):
    """
    Returns all question: question data and student's info about the question.
    """
    student_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, str(question)))
    return {
        **get_question_data(group, exam, question),
        'answer': student_item.get_item('answer'),
        'score': student_item.get_item('score')
    }


def get_exam_info(group, exam):
    """
    Returns exam's info.
    """
    exam_item = Item(os.path.join('data', group, 'exams', exam, 'settings'))
    quantity = len(os.listdir(os.path.join('data', group, 'exams', exam))) - 1
    return {
        'published': exam_item.get_item('published'),
        'duration': exam_item.get_item('duration'),
        'quantity': quantity
    }


def get_exam_info_user(group, user, exam):
    """
    Returns exam's info.
    """
    user_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, 'settings'))
    exam_data = get_exam_data_user(group, user, exam)

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

    return {
        **get_exam_info(group, exam),
        'start': user_item.get_item('start'),
        'end': user_item.get_item('end'),
        'state': state,
        'total_score': total_score,
        'total_maxscore': total_maxscore
    }


def get_exam_data(group, exam):
    """
    Returns exam data.
    """
    quantity = get_exam_info(group, exam)['quantity']
    return [
        get_question_data(group, exam, question) for question in range(1, quantity + 1)
    ]


def get_exam_data_user(group, user, exam):
    """
    Returns all exam.
    """
    quantity = get_exam_info(group, exam)['quantity']
    return [
        get_question_data_user(group, user, exam, question) for question in range(1, quantity + 1)
    ]


def list_of_exams(group):
    """
    Returns list of all available exams in the group.
    """
    return os.listdir(os.path.join('data', group, 'exams'))


def list_of_published_exams(group):
    """
    Returns list of published (available for student) exams in the group.
    """
    return [
        exam for exam in list_of_exams(group) if get_exam_info(group, exam)['published'] == '1'
    ]


def start_exam(group, user, exam):
    """
    Starts the exam.
    """
    user_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, 'settings'))
    current_time = int(time.time())
    duration_time = int(get_exam_info(group, exam)['duration']) * 60
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
    # exam_data = get_exam_data_user(group, user, exam)
    # for question in range(1, len(exam_data) + 1):
    #     if exam_data[question - 1]['score'] == '-1':
    #         print("adding notification of question " + str(question))
    return True


def save_answer(group, user, exam, question, answer):
    """
    Saves student's answer.
    """
    student_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, str(question)))
    student_item.set_item('answer', answer)
    return True


def check(group, user, exam, question):
    """
    Checks student's answer to the short question.
    """
    question_data = get_question_data_user(group, user, exam, question)
    student_item = Item(os.path.join('data', group, 'students', user, 'exams', exam, str(question)))
    if question_data['type'] == 'Short':
        answer = student_item.get_item('answer')
        correct = question_data['correct'].split('\n')
        if format_str(answer) in [format_str(s) for s in correct]:
            student_item.set_item('score', question_data['maxscore'])
        else:
            student_item.set_item('score', 0)
    elif question_data['type'] == 'Long':
        student_item.set_item('score', -1)
    return True


ENCODING = 'utf-8-sig'
SERVER = SimpleXMLRPCServer(('', 8000))

SERVER.register_function(ping)
SERVER.register_function(register_student)
SERVER.register_function(register_teacher)
SERVER.register_function(login_student)
SERVER.register_function(login_teacher)
SERVER.register_function(get_question_data)
SERVER.register_function(get_question_data_user)
SERVER.register_function(get_exam_info)
SERVER.register_function(get_exam_info_user)
SERVER.register_function(get_exam_data)
SERVER.register_function(get_exam_data_user)
SERVER.register_function(list_of_exams)
SERVER.register_function(list_of_published_exams)
SERVER.register_function(start_exam)
SERVER.register_function(finish_exam)
SERVER.register_function(save_answer)
SERVER.register_function(check)

SERVER.serve_forever()
