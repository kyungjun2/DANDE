import json
import tkinter.messagebox
from ctypes import c_bool
from multiprocessing import Process, Value, freeze_support
from tkinter import Tk, Frame

from look_for_changes import changes
from python_encrypt import encrypt

run = Value(c_bool, False)
watcher_process = None


def when_changes_occur(results, file_path, key):
    process_list = []
    enc = encrypt.EncryptFile(key=bytes(key, 'utf-8'), max_threads=8)

    for item in results:
        path = file_path + item[1]
        if (item[0] == changes.FILE_ACTION_ADDED or item[0] == changes.FILE_ACTION_CHANGED) and \
                (item[1].split('.')[0] != 'decrypted' and item[1].split('.')[-1] != 'encrypted'):
            p = Process(target=enc.encrypt_file, args=(path,))
            p.start()
            process_list.append(p)

    for p in process_list:
        p.join()


win = Tk()
win.title("message box")

base_frm = Frame(win)
base_frm.pack()

win.geometry("300x300+0+0")
win.resizable(False, False)

label = tkinter.Label(win, text="강제종료시 오류가 생길 수 있습니다!")
label.pack()


def start_button_call():
    tkinter.messagebox.showinfo(title="Message box", message="Start Selected!")
    global run, watcher_process
    try:
        file = open("settings.json", "rb")
        setting = json.load(file)
        path = setting['path']
        if path[-1] is not "\\":
            path = path + '\\'
        key = setting['key']
    except (KeyError, FileNotFoundError, ValueError) as e:
        path = None
        key = None

    if path is None:
        tkinter.messagebox.showinfo(title="Message box", message="settings.json 에 목표 디렉토리, 암호화키를 지정하세요!")
    elif watcher_process is not None:
        tkinter.messagebox.showinfo(title="Message box", message="이미 감시 프로세스가 실행중!")
    else:
        run.value = True
        watcher_process = Process(target=changes.monitor_dir_async, args=(path, when_changes_occur, run, key))
        watcher_process.start()


def stop_button_call():
    tkinter.messagebox.showinfo(title="Message box", message="Stop Selected!")

    global run, watcher_process
    run.value = False

    while True:
        try:
            watcher_process.join()
            watcher_process = None
        except:
            break


def kill_program_button():
    global run, watcher_process
    run.value = False
    while True:
        try:
            watcher_process.join()
            watcher_process = None
        except:
            break

    tkinter.messagebox.showinfo(title="message box", message="Thanks!")
    win.destroy()
    win.quit()


btn1 = tkinter.Button(win, text="Start", command=start_button_call)
btn1.pack(padx="50", pady='10', )

btn2 = tkinter.Button(win, text="Stop", command=stop_button_call)
btn2.pack(padx="50", pady='10')

btn3 = tkinter.Button(win, text="Quit", command=kill_program_button)
btn3.pack(padx="50", pady='10')

btn1.place(x=20, y=70, width=80, height=70)

btn2.place(x=200, y=70, width=80, height=70)

btn3.place(x=20, y=150, width=260, height=40)

if __name__ == "__main__":
    freeze_support()
    win.mainloop()
