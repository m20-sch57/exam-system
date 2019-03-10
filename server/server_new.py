"""
Examiner project, server module.
"""


import sqlite3
from xmlrpc.server import SimpleXMLRPCServer


def ping():
    """
    Ping.
    """
    return True


def get_group(group_name):
    """
    Returns id of the group.
    """
    CURSOR.execute(
        "SELECT rowid, * FROM groups WHERE name=?",
        (group_name,)
    )
    groups = CURSOR.fetchall()
    return None if not groups else dict(groups[0])


def get_user(user_name):
    """
    Returns id of the user.
    """
    CURSOR.execute(
        "SELECT rowid, * FROM users WHERE name=?",
        (user_name,)
    )
    users = CURSOR.fetchall()
    return None if not users else dict(users[0])


def register(user_name, password, is_admin, group_name):
    """
    Tries to register the user.
    """
    group = get_group(group_name)
    if group is None:
        return False
    if get_user(user_name) is not None:
        return False
    CURSOR.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?)",
        (user_name, password, is_admin, group['rowid'])
    )
    CONNECTION.commit()
    return True


def login(user_name, password, is_admin):
    """
    Tries to login the user.
    """
    user = get_user(user_name)
    if user is None:
        return False
    if user['password'] != password or user['is_admin'] != is_admin:
        return False
    return user


def list_of_published_exams(group_id):
    """
    Returns list of all published exams in the group.
    """
    CURSOR.execute(
        "SELECT rowid, name FROM exams WHERE published=1 AND group_id=?",
        (group_id,)
    )
    exams = CURSOR.fetchall()
    return [dict(exam) for exam in exams]


def list_of_all_exams(group_id):
    """
    Returns list of all exams in the group.
    """
    CURSOR.execute(
        "SELECT rowid, name FROM exams WHERE group_id=?",
        (group_id,)
    )
    exams = CURSOR.fetchall()
    return [dict(exam) for exam in exams]


def create_exam(exam_name, group_id):
    """
    Creates the exam.
    """
    CURSOR.execute(
        "INSERT INTO exams VALUES (?, 45, 0, ?)",
        (exam_name, group_id)
    )
    CONNECTION.commit()
    return CURSOR.lastrowid


def delete_exam(exam_id):
    """
    Deletes the exam.
    """
    CURSOR.execute(
        "DELETE FROM exams WHERE rowid=?",
        (exam_id,)
    )
    CURSOR.execute(
        "DELETE FROM questions WHERE exam_id=?",
        (exam_id,)
    )
    CONNECTION.commit()
    return True


def get_exam_data(exam_id):
    """
    Returns exam data.
    """
    CURSOR.execute(
        "SELECT rowid, * FROM exams WHERE rowid=?",
        (exam_id,)
    )
    exams = CURSOR.fetchall()
    return {} if not exams else dict(exams[0])


def set_exam_data(exam_data):
    """
    Saves exam data.
    """
    CURSOR.execute(
        "UPDATE exams SET name=?, duration=?, published=? WHERE rowid=?",
        (exam_data['name'], exam_data['duration'],
         exam_data['published'], exam_data['rowid'])
    )
    CONNECTION.commit()
    return True


def get_exam_data_student(exam_id, user_id):
    """
    Returns exam data for student.
    """
    pass


def get_questions_ids(exam_id):
    """
    Returns questions' ids in the exam.
    """
    CURSOR.execute(
        "SELECT rowid FROM questions WHERE exam_id=?",
        (exam_id,)
    )
    questions = CURSOR.fetchall()
    return [dict(question) for question in questions]


def get_questions_results(exam_id, user_id):
    """
    Returns user's results of the exam.
    """
    pass


def create_question(exam_id, question_type):
    """
    Creates question of the exam.
    """
    CURSOR.execute(
        "INSERT INTO questions VALUES (?, '', '', 1, ?)",
        (question_type, exam_id)
    )
    CONNECTION.commit()
    return CURSOR.lastrowid


def delete_question(question_id):
    """
    Deletes question.
    """
    CURSOR.execute(
        "DELETE FROM questions WHERE rowid=?",
        (question_id,)
    )
    CONNECTION.commit()
    return True


def get_question_data(question_id):
    """
    Returns question data.
    """
    CURSOR.execute(
        "SELECT rowid, * FROM questions WHERE rowid=?",
        (question_id,)
    )
    questions = CURSOR.fetchall()
    return {} if not questions else dict(questions[0])


def set_question_data(question_data):
    """
    Saves question data.
    """
    CURSOR.execute(
        "UPDATE questions SET type=?, statement=?, correct=?, maxscore=? WHERE rowid=?",
        (question_data['type'], question_data['statement'],
         question_data['correct'], question_data['maxscore'],
         question_data['rowid'])
    )
    CONNECTION.commit()
    return True


def get_question_data_student(question_id, user_id):
    """
    Returns question data for student.
    """
    pass


CONNECTION = sqlite3.connect('database.db')
CONNECTION.row_factory = sqlite3.Row
CURSOR = CONNECTION.cursor()

SERVER = SimpleXMLRPCServer(('', 8000))

SERVER.register_function(ping)
SERVER.register_function(register)
SERVER.register_function(login)
SERVER.register_function(list_of_published_exams)
SERVER.register_function(list_of_all_exams)
SERVER.register_function(create_exam)
SERVER.register_function(delete_exam)
SERVER.register_function(get_exam_data)
SERVER.register_function(set_exam_data)
SERVER.register_function(get_exam_data_student)
SERVER.register_function(get_questions_ids)
SERVER.register_function(get_questions_results)
SERVER.register_function(create_question)
SERVER.register_function(delete_question)
SERVER.register_function(get_question_data)
SERVER.register_function(set_question_data)
SERVER.register_function(get_question_data_student)

SERVER.serve_forever()
