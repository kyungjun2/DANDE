import json
import os
import subprocess
import tkinter
from tkinter import messagebox, filedialog

DETACHED_PROCESS = 0x00000008

file_path = None
abspath = os.path.dirname(os.path.abspath(__file__))
if os.path.isdir(abspath + "\\dist"):
    abspath = abspath + "\\dist"

win = tkinter.Tk()
base_frm = tkinter.Frame(win)
base_frm.pack()
win.title("암!호!화! Yeah~")
win.geometry("300x300+0+0")
win.resizable(False, False)
label = tkinter.Label(win, text="Encryption Or Decryption")
label.pack()


def encrypt_button_call():
    try:
        file = open(abspath + "\\settings.json", "rb")
        setting = json.load(file)
        key = setting['key']
    except (KeyError, FileNotFoundError) as e:
        key = None

    messagebox.showinfo(title="Message box", message="Encryption Selected!")
    global file_path

    if file_path is not None and key is not None:
        filepath = abspath + "\\main.exe"
        params = "-encrypt \"{0}\" -key {1} -threads {2}".format(str(file_path), str(key), str(16))
        os.system(filepath + " " + params)
        messagebox.showinfo(title="INFO", message="암호화 완료")

        file_path = None  # 초기화
    else:
        messagebox.showinfo(title="Message box", message="파일 선택 or settings.json 에서 키값 설정")


def decrypt_button_call():
    try:
        file = open(abspath + "\\settings.json", "rb")
        setting = json.load(file)
        key = setting['key']
    except (KeyError, FileNotFoundError) as e:
        key = None

    messagebox.showinfo(title="Message box", message="Decryption Selected!")
    global file_path

    if file_path is not None and key is not None:
        filepath = abspath + "\\main.exe"
        params = "-decrypt \"{0}\" -key {1} -threads {2}".format(str(file_path), str(key), str(16))
        os.system(filepath + " " + params)
        messagebox.showinfo(title="INFO", message="복호화 완료")

        file_path = None  # 초기화
    else:
        messagebox.showinfo(title="Message box", message="파일 선택 or settings.json 에서 키값 설정")


def select_file_button():
    messagebox.showinfo(title="Message box", message="Select File plz!")
    root = tkinter.Tk()
    root.withdraw()

    global file_path
    file_path = filedialog.askopenfilename()


def kill_program_button():
    messagebox.showinfo(title="message box", message="Made by 이경준 박민욱 곽 준 Thanks!")
    win.destroy()
    win.quit()


def how_to_use_button():
    messagebox.showinfo(title="message box", message="How to use Selected!")
    pid = subprocess.Popen(["notepad.exe", abspath + "\\How_To_Use.txt"],
                           creationflags=DETACHED_PROCESS).pid


def watch_directory_program_activate():
    messagebox.showinfo(title="message box", message="폴더 감시 Selected!")
    pid = subprocess.Popen([abspath + "\\directory_watcher.exe"],
                           creationflags=DETACHED_PROCESS).pid


if __name__ == "__main__":
    encrypt_button = tkinter.Button(win, text="Encryption!", command=encrypt_button_call)
    encrypt_button.pack(padx="50", pady='10', )

    decrypt_button = tkinter.Button(win, text="Decryption!", command=decrypt_button_call)
    decrypt_button.pack(padx="50", pady='10')

    selectfile_button = tkinter.Button(win, text="Select File!", command=select_file_button)
    selectfile_button.pack(padx="50", pady="10")

    kill_button = tkinter.Button(win, text="Quit!", command=kill_program_button)
    kill_button.pack(padx="50", pady="10")

    usage_button = tkinter.Button(win, text="How to use??", command=how_to_use_button)
    usage_button.pack(padx="50", pady="10")

    watchdirectory_button = tkinter.Button(win, text="폴더 감시", command=watch_directory_program_activate)
    watchdirectory_button.pack(padx="50", pady="10")

    encrypt_button.place(x=5, y=70, width=145, height=70)
    watchdirectory_button.place(x=5, y=140, width=145, height=70)
    decrypt_button.place(x=150, y=70, width=145, height=70)
    selectfile_button.place(x=5, y=25, width=290, height=40)
    kill_button.place(x=5, y=255, width=290, height=40)
    usage_button.place(x=5, y=210, width=290, height=40)

    win.mainloop()

