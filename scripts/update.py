from tkinter import *
import os

def DestroyAll():
    for widget in root.winfo_children():
        widget.destroy()

def PrintLog(s):
    LogText.insert(END, s)
    LogText.see(END)
    LogText.update()

def process():
    global LogText
    LogText = Text(frame, font='Arial 14')
    LogText.place(x=0, y=170, height=160, width=460)
    Label(frame, text='Выполняется...', font='Arial 30').place(x=0, y=350, height=50, width=460)
    try:
        path1 = FromEntry.get()
        path2 = 'exams'
        PrintLog('Starting update process.\nSource: ' + path1 + '\nDestination: ' + path2 + '\n\n')
        PrintLog('Reading data in folder' + path1 + ' ...\n')
        AllExams = os.listdir(path1)
        PrintLog('OK!\n\n')
        PrintLog('Readable exams:\n' + '\n'.join(AllExams) + '\n\n')
        PrintLog('Copying data ...\n')
        for exam in AllExams:
            AllExam = os.listdir(os.path.join(path1, exam))
            PrintLog('Reading exam "' + exam + '" ...\n')
            for question in range(len(AllExam)):
                cur_dir = os.path.join(path1, exam, str(question + 1))
                to_dir = os.path.join(path2, exam, str(question + 1))
                PrintLog('question ' + str(question + 1) + ':\n')
                tp = open(cur_dir + '\\type', encoding=encoding).read()
                if tp == 'Тест':
                    PrintLog('  type: ' + tp + '\n')
                    statement = open(cur_dir + '\\statement', encoding=encoding).read()
                    variants = open(cur_dir + '\\variants', encoding=encoding).read().split('\n')
                    correct = open(cur_dir + '\\correct', encoding=encoding).read()
                    statement += '\n\n'
                    for var in range(len(variants)):
                        statement += str(var + 1) + ') ' + variants[var] + '\n'
                    PrintLog('  adding ' + to_dir + '\n')
                    if not os.path.exists(to_dir):
                        os.makedirs(to_dir)
                    open(to_dir + '\\type', 'w', encoding=encoding).write('Short')
                    open(to_dir + '\\statement', 'w', encoding=encoding).write(statement)
                    open(to_dir + '\\correct', 'w', encoding=encoding).write(correct)
                    open(to_dir + '\\maxscore', 'w', encoding=encoding).write('1')
                else:
                    PrintLog('  WARNING: type "' + tp + '" not supported\n')
            PrintLog('updating exam settings...\n')
            to_dir = os.path.join(path2, exam, 'settings')
            if not os.path.exists(to_dir):
                os.makedirs(to_dir)
            open(to_dir + '\\duration', 'w', encoding=encoding).write('5')
            PrintLog('OK!\n\n')
        Label(frame, text='Успешно!', fg='green', font='Arial 30').place(x=0, y=350, height=50, width=460)
    except:
        PrintLog('ERROR\n*exiting*')
        Label(frame, text='Ошибка!', fg='red', font='Arial 30').place(x=0, y=350, height=50, width=460)
        

root = Tk()
root.geometry('500x500')
root.title('Update')
Label(root, text='Обновить экзамены', font='Arial 30').pack()
frame = Frame(root)
frame.place(x=20, y=80, height=400, width=460)
Label(frame, text='Путь к папке с экзаменами:', font='Arial 20').place(x=0, y=0, height=40, width=460)
FromEntry = Entry(frame, width=40, font='Arial 14')
FromEntry.place(x=0, y=50, height=30, width=460)
ProcessButton = Button(frame, text='Запустить обновление', fg='blue', font='Arial 30', command=process)
ProcessButton.place(x=0, y=90, height=70, width=460)
encoding='utf-8-sig'
root.mainloop()
