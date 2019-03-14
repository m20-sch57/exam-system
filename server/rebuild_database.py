"""
Rebuilds database: deletes old database.db and creates tables.
"""


import os
import sqlite3


os.remove('database.db')
CONNECTION = sqlite3.connect('database.db')
CONNECTION.row_factory = sqlite3.Row
CURSOR = CONNECTION.cursor()

CURSOR.execute(
    """
    CREATE TABLE groups
    (name text)
    """
)
CURSOR.execute(
    """
    CREATE TABLE users
    (name text, password text, is_admin integer, group_id integer)
    """
)
CURSOR.execute(
    """
    CREATE TABLE exams
    (name text, duration integer, published integer, group_id integer)
    """
)
CURSOR.execute(
    """
    CREATE TABLE questions
    (type text, statement text, correct text, maxsubs integer, maxscore integer, exam_id integer)
    """
)
CURSOR.execute(
    """
    CREATE TABLE examrequests
    (student_id integer, exam_id integer, start integer, end integer)
    """
)
CURSOR.execute(
    """
    CREATE TABLE submissions
    (student_id integer, exam_id integer, question_id integer, answer text, score real)
    """
)

CURSOR.execute(
    "INSERT INTO groups VALUES ('m20')"
)
CURSOR.execute(
    "INSERT INTO users VALUES ('Фёдор Куянов', '8cb2237d0679ca88db6464eac60da96345513964', 0, 1)"
)
CURSOR.execute(
    "INSERT INTO users VALUES ('Админ', '8cb2237d0679ca88db6464eac60da96345513964', 1, 1)"
)

CONNECTION.commit()
