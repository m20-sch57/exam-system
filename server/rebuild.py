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
    (student_id integer, exam_id integer, question_id integer, answer text, share real)
    """
)

CURSOR.execute(
    "INSERT INTO groups VALUES ('m20')"
)
CURSOR.execute(
    "INSERT INTO users VALUES ('Фёдор Куянов', 'ab1dbbf93be316a67cb38ad2916ed1cd9e3af3a4', 0, 1)"
)
CURSOR.execute(
    "INSERT INTO users VALUES ('Админ', 'ab1dbbf93be316a67cb38ad2916ed1cd9e3af3a4', 1, 1)"
)

CONNECTION.commit()
