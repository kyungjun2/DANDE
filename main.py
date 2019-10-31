import sys

import encrypt

if __name__ == '__main__':
    argv = sys.argv

    if len(argv) < 2:
        print("파라미터 부족")
        sys.exit(0)

    else:
        mode = -1
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
            else:
                pass

        if mode == -1 or len(key) == 0:
            print("파라미터 부족")
            sys.exit(1)

        if mode == 1:
            module = encrypt.EncryptFile(key=bytes(key, 'utf-8'))
            module.encrypt_file(path)
        elif mode == 2:
            module = encrypt.DecryptFile(key=bytes(key, 'utf-8'))
            module.decrypt_file(path)
        sys.exit(0)
