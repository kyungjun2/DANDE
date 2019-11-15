import re
import sys
import time
from multiprocessing import freeze_support, cpu_count

from python_encrypt import encrypt


def main():
    freeze_support()
    argv = sys.argv
    start_time = time.time()

    if len(argv) < 2:
        print("파라미터 부족")
        sys.exit(1)

    else:
        mode = -1
        max_threads = -1
        key = ''
        path = ''

        for idx in range(1, len(argv), 1):
            if argv[idx] == '-encrypt':
                idx += 1
                print("다음 파일을 암호화 : {0}".format(argv[idx]))

                path = argv[idx]
                mode = 1
            elif argv[idx] == '-decrypt':
                idx += 1
                print("다음 파일을 복호화 : {0}".format(argv[idx]))

                path = argv[idx]
                mode = 2
            elif argv[idx] == '-key':
                idx += 1
                print("작업에 사용할 비밀키 = {0}".format(argv[idx]))

                key = argv[idx]
                if len(key) != 16:
                    print("키 값의 길이가 알맞지 않음")
                    sys.exit(1)
            elif argv[idx] == '-threads':
                idx += 1
                print("최대 쓰레드 수 = {0}".format(argv[idx]))
                max_threads = int(argv[idx])
            else:
                pass

        if mode == -1 or len(key) == 0:
            print("파라미터 부족")
            sys.exit(1)
        if max_threads == -1:
            max_threads = cpu_count()
        if mode == 2 and path.count(".encrypted") == 0:
            print("암호화된 파일이 아님")
            sys.exit(-1)

        path = re.sub(re.compile("/"), r"\\", path)

        if mode == 1:
            module = encrypt.EncryptFile(key=bytes(key, 'utf-8'), max_threads=max_threads)
            module.encrypt_file(path)
        elif mode == 2:
            module = encrypt.DecryptFile(key=bytes(key, 'utf-8'), max_threads=max_threads)
            module.decrypt_file(path)

        print("걸린 시간 : {}초.".format(format(time.time() - start_time, '.2f')))


if __name__ == '__main__':
    main()
    input("아무 키나 눌러서 계속하세요")
    sys.exit(0)
