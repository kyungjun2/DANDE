"""
    TODO
        1. 함수로 단순화
        2. main 파일에 디렉터리 감시 분기점 추가
        3. KeyboardInterrupt 로 꺼질 수 있도록 코드 제작
"""


from ctypes import c_bool
from multiprocessing import Process, Queue, Value

from look_for_changes import chages
from python_encrypt import encrypt

if __name__ == '__main__':
    q = Queue()
    s = Value(c_bool, True)
    enc = encrypt.EncryptFile(b'1234567890123456', 6)
    path = "C:\\Users\\이경준\\Pictures\\Screenshots"
    if path[-1] != '\\':
        path = path + '\\'

    changeDetection_process = Process(target=chages.read_changes, args=(path, s, q,))
    changeDetection_process.start()

    while True:
        try:
            if q.qsize() is not 0:
                chg = q.get()
                print(chg)

                if (chg[0] == 1 or chg[0] == 3) and (chg[1].split('.')[0] != 'decrypted' and chg[1].split('.')[-1] != 'encrypted'):
                    encryption_process = Process(target=enc.encrypt_file, args=(path + chg[1],))
                    encryption_process.start()
                    encryption_process.join()
        except KeyboardInterrupt:
            break
    s.value = False
    changeDetection_process.join()
