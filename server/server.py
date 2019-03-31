"""
Examiner project, server module.
"""


import sqlite3
from xmlrpc.server import SimpleXMLRPCServer
from time import time


def ping():
    """
    Ping.
    """
    return True


def get_last(data):
    """
    Returns dict(data[-1]) if data else False
    """
    return dict(data[-1]) if data else False


def create_group(group_name):
    """
    Creates the group.
    """
    if not group_name:
        return False
    CURSOR.execute(
        "SELECT * FROM groups WHERE name=?",
        (group_name,)
    )
    group = get_last(CURSOR.fetchall())
    if group is not False:
        return False
    CURSOR.execute(
        "INSERT INTO groups VALUES (?)",
        (group_name,)
    )
    return True


def register(user_name, password, is_admin, group_name):
    """
    Tries to register the user.
    """
    if not user_name:
        return False
    CURSOR.execute(
        "SELECT rowid, * FROM groups WHERE name=?",
        (group_name,)
    )
    group = get_last(CURSOR.fetchall())
    CURSOR.execute(
        "SELECT rowid, * FROM users WHERE name=?",
        (user_name,)
    )
    user = get_last(CURSOR.fetchall())
    if group is False:
        return False
    if user is not False:
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
    CURSOR.execute(
        "SELECT rowid, * FROM users WHERE name=?",
        (user_name,)
    )
    user = get_last(CURSOR.fetchall())
    if user is False:
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


def create_exam(group_id):
    """
    Creates the exam.
    """
    CURSOR.execute(
        "INSERT INTO exams VALUES ('', 45, 0, ?)",
        (group_id,)
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
    CURSOR.execute(
        "DELETE FROM examrequests WHERE exam_id=?",
        (exam_id,)
    )
    CURSOR.execute(
        "DELETE FROM submissions WHERE exam_id=?",
        (exam_id,)
    )
    CONNECTION.commit()
    return True


def start_exam(exam_id, user_id):
    """
    Starts the exam.
    """
    exam_data = get_exam_data(exam_id)
    if not exam_data:
        return False
    CURSOR.execute(
        "INSERT INTO examrequests VALUES (?, ?, ?, ?)",
        (user_id, exam_id, int(time()), int(time()) + exam_data['duration'] * 60)
    )
    CONNECTION.commit()
    return True


def finish_exam(exam_id, user_id):
    """
    Finishes the exam.
    """
    CURSOR.execute(
        "UPDATE examrequests SET end=? WHERE student_id=? AND exam_id=?",
        (time(), user_id, exam_id)
    )
    CONNECTION.commit()
    return True


def get_users_by_exam(exam_id):
    """
    Returns users that participated in the exam.
    """
    CURSOR.execute(
        "SELECT rowid, * FROM users WHERE rowid IN " +
        "(SELECT student_id FROM examrequests WHERE exam_id=?)",
        (exam_id,)
    )
    return [dict(user) for user in CURSOR.fetchall()]


def get_exam_data(exam_id):
    """
    Returns exam data.
    """
    CURSOR.execute(
        "SELECT rowid, * FROM exams WHERE rowid=?",
        (exam_id,)
    )
    return get_last(CURSOR.fetchall())


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


def get_questions_ids(exam_id):
    """
    Returns questions' ids in the exam.
    """
    CURSOR.execute(
        "SELECT rowid FROM questions WHERE exam_id=?",
        (exam_id,)
    )
    questions = CURSOR.fetchall()
    return [dict(question)['rowid'] for question in questions]


def get_question_result(question_id, user_id):
    """
    Returns user's result of the question.
    """
    CURSOR.execute(
        "SELECT * FROM submissions WHERE student_id=? AND question_id=?",
        (user_id, question_id)
    )
    result = get_last(CURSOR.fetchall())
    if not result:
        return result
    if result['share'] != -1:
        result['score'] = int(get_question_data(question_id)['maxscore'] * result['share'])
    else:
        result['score'] = 0
    return result


def get_questions_results(exam_id, user_id):
    """
    Returns user's results of the exam.
    """
    return [get_question_result(question_id, user_id) for question_id in get_questions_ids(exam_id)]


def get_results_table(exam_id):
    """
    Returns results table of the exam.
    """
    return [get_questions_results(exam_id, user['rowid']) for user in get_users_by_exam(exam_id)]


def get_exam_data_student(exam_id, user_id):
    """
    Returns exam data for student.
    """
    exam_data = get_exam_data(exam_id)
    if not exam_data:
        return False
    CURSOR.execute(
        "SELECT * FROM examrequests WHERE student_id=? AND exam_id=?",
        (user_id, exam_id)
    )
    request = get_last(CURSOR.fetchall())
    start = request['start'] if request else -1
    end = request['end'] if request else -1
    if not request:
        state = 'Not started'
    elif time() >= end:
        state = 'Finished'
    else:
        state = 'Running'
    total_score = 0
    total_maxscore = 0
    for question_id in get_questions_ids(exam_id):
        result = get_question_result(question_id, user_id)
        maxscore = get_question_data(question_id)['maxscore']
        score = result['score'] if result else 0
        total_maxscore += maxscore
        total_score += score
    return {
        **exam_data,
        'state': state,
        'start': start,
        'end': end,
        'total_score': total_score,
        'total_maxscore': total_maxscore
    }


def create_question(exam_id, question_type):
    """
    Creates question of the exam.
    """
    maxsubs = 1 if question_type == 'Short' else 1000
    CURSOR.execute(
        "INSERT INTO questions VALUES (?, '', '', ?, 1, ?)",
        (question_type, maxsubs, exam_id)
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
    CURSOR.execute(
        "DELETE FROM submissions WHERE question_id=?",
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
    return get_last(CURSOR.fetchall())


def set_question_data(question_data):
    """
    Saves question data.
    """
    CURSOR.execute(
        "UPDATE questions SET type=?, statement=?, correct=?, maxsubs=?, maxscore=? WHERE rowid=?",
        (question_data['type'], question_data['statement'], question_data['correct'],
         question_data['maxsubs'], question_data['maxscore'],
         question_data['rowid'])
    )
    CONNECTION.commit()
    return True


def add_submission(exam_id, question_id, submission_text, user_id):
    """
    Adds submission with submission_text.
    """
    question_data = get_question_data(question_id)
    if not question_data or not submission_text:
        return False
    CURSOR.execute(
        "SELECT * FROM submissions WHERE student_id=? AND question_id=?",
        (user_id, question_id)
    )
    if len(CURSOR.fetchall()) >= question_data['maxsubs']:
        return False
    CURSOR.execute(
        "INSERT INTO submissions VALUES (?, ?, ?, ?, -1)",
        (user_id, exam_id, question_id, submission_text)
    )
    CONNECTION.commit()
    judge_submission(CURSOR.lastrowid)
    return True


def judge_submission(submission_id):
    """
    Judges the submission.
    """
    CURSOR.execute(
        "SELECT * FROM submissions WHERE rowid=?",
        (submission_id,)
    )
    submission = get_last(CURSOR.fetchall())
    question_data = get_question_data(submission['question_id'])
    if not submission or not question_data:
        return False
    if question_data['type'] == 'Short':
        share = judge_short(submission, question_data)
    elif question_data['type'] == 'Long':
        share = judge_long(submission, question_data)
    else:
        share = -1
    CURSOR.execute(
        "UPDATE submissions SET share=? WHERE rowid=?",
        (share, submission_id)
    )
    CONNECTION.commit()
    return True


def judge_short(submission, question_data):
    """
    Judges short question.
    """
    share = -1
    correct_list = question_data['correct'].split('; ')
    correct_list = [s.lower() for s in correct_list]
    if submission['answer'].lower() in correct_list:
        share = 1
    else:
        share = 0
    return share


def judge_long(submission_text, question_data):
    """
    Judges long question.
    """
    return -1


CONNECTION = sqlite3.connect('database.db')
CONNECTION.row_factory = sqlite3.Row
CURSOR = CONNECTION.cursor()

SERVER = SimpleXMLRPCServer(('', 8000))

SERVER.register_function(ping)
SERVER.register_function(create_group)
SERVER.register_function(register)
SERVER.register_function(login)
SERVER.register_function(list_of_published_exams)
SERVER.register_function(list_of_all_exams)
SERVER.register_function(create_exam)
SERVER.register_function(delete_exam)
SERVER.register_function(start_exam)
SERVER.register_function(finish_exam)
SERVER.register_function(get_users_by_exam)
SERVER.register_function(get_exam_data)
SERVER.register_function(set_exam_data)
SERVER.register_function(get_questions_ids)
SERVER.register_function(get_question_result)
SERVER.register_function(get_questions_results)
SERVER.register_function(get_results_table)
SERVER.register_function(get_exam_data_student)
SERVER.register_function(create_question)
SERVER.register_function(delete_question)
SERVER.register_function(get_question_data)
SERVER.register_function(set_question_data)
SERVER.register_function(add_submission)

SERVER.serve_forever()
