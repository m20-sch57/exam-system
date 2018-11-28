"""
Safe connection to server.
"""


from xmlrpc.client import ServerProxy
import socket


def read_ip():
    """
    Returns current ip-address of server.
    """
    return open('server.txt', encoding='utf-8-sig').read()


def update_ip(application, ip_address):
    """
    Updates current ip-address of server.
    """
    open('server.txt', 'w', encoding='utf-8-sig').write(ip_address)
    application.server = ServerProxy('http://' + ip_address + ':8000')


def safe_call(application, function):
    """
    Tries to call function. If fails, displays error page.
    """
    try:
        return function()
    except socket.error:
        application.display_login_page('Сервер не отвечает')


def login(application):
    """
    Tries to login the student.
    """
    return safe_call(application, lambda: application.server.login(
        application.group, application.user, application.password))


def list_of_exams(application):
    """
    Returns list of all available exams.
    """
    return safe_call(application, lambda: application.server.list_of_exams(application.group))


def get_exam(application, exam):
    """
    Returns all question data in the exam.
    """
    return safe_call(application, lambda: application.server.get_exam(
        application.group, application.user, exam))


def get_exam_info(application, exam):
    """
    Returns exam's info.
    """
    return safe_call(application, lambda: application.server.get_exam_info(
        application.group, application.user, exam))


def start_exam(application, exam):
    """
    Starts the exam.
    """
    return safe_call(application, lambda: application.server.start_exam(
        application.group, application.user, exam))


def finish_exam(application, exam):
    """
    Finishes the exam.
    """
    return safe_call(application, lambda: application.server.finish_exam(
        application.group, application.user, exam))


def save_answer(application, exam, question, answer):
    """
    Saves student's answer.
    """
    return safe_call(application, lambda: application.server.save_answer(
        application.group, application.user, exam, question, answer))


def check(application, exam, question):
    """
    Checks student's answer.
    """
    return safe_call(application, lambda: application.server.check(
        application.group, application.user, exam, question))


socket.setdefaulttimeout(3)
