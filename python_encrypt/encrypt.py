def validate_file(path):
    import os
    return os.path.isfile(path)


def read_file(path):
    try:
        o = open(path, 'rb')
        file_raw = o.read()
        o.close()
        return file_raw
    except IOError:
        return None


def get_size(raw_file):
    if raw_file is None:
        return -1
    else:
        size = len(raw_file)
        return size


def format_size(size):
    if size < 1024:
        return "%dB" % size
    elif size < 1024 ** 2:
        return "%.02fKB" % (size / 1024)
    elif size < 1024 ** 3:
        return "%.02fMB" % (size / (1024 ** 2))
    elif size < 1024 ** 4:
        return "%.02fGB" % (size / (1024 ** 3))


def kill():
    import sys
    sys.exit(-1)


class EncryptFile:
    def __init__(self, key, max_threads):
        self.key = key
        self.block_size = 1024*int(1024/2)
        self.maximum_process = max_threads

    def aes_encrypt(self, data):
        from Crypto.Cipher import AES
        cipher = AES.new(self.key, AES.MODE_ECB)

        if len(data) % 16 != 0:
            print("데이터 블록의 크기가 잘못됨")
            import sys
            sys.exit(-1)
        elif len(data) == 0:
            return None
        else:
            return cipher.encrypt(data)

    def encrypt_block(self, block, number, q, process_count):
        process_count.value += 1

        result = None
        if get_size(block) < 16:
            result = {number: block}

        else:
            i = 0
            encrypted_block = b''
            length = len(block)

            while i < length:
                if i + 16 <= length:
                    encrypted_block += self.aes_encrypt(block[i:i + 16])
                    encrypted_block += block[i + 16:i + 32]
                else:
                    encrypted_block += block[i:]
                i += 32

            result = {number: encrypted_block}

        q.put(result)
        process_count.value += -1

    def encrypt_file(self, path):
        from multiprocessing import Process, Queue, Value
        import time

        if validate_file(path) is False:
            print("파일이 존재하지 않음")
            kill()

        raw_file = read_file(path)
        print("파일 크기 = {0}".format(format_size(get_size(raw_file))))
        if get_size(raw_file) < 16:
            print("파일이 너무 작음")
            kill()

        i = 0
        count = 0
        live_process = Value('i', 0)
        length = len(raw_file)
        maximum_thread = int(length / self.block_size) + 1

        process_list = []
        file_bytes = Queue()

        while i < length:
            p = Process(target=self.encrypt_block, args=(raw_file[i:i+self.block_size], i, file_bytes, live_process, ))
            p.start()
            process_list.append(p)
            count += 1
            i += self.block_size

            printed = False
            while live_process.value > self.maximum_process:
                time.sleep(0.2)
                if printed is False:
                    print("%0.2f" % (((count - 1) / maximum_thread) * 100) + "%")
                    printed = True

        while file_bytes.qsize() < count:
            time.sleep(0.5)
        print("암호화 완료! 결과 모으는중...")

        new_file = b''
        encrypted_files = {}

        while file_bytes.empty() is not True:
            encrypted_files.update(file_bytes.get())

        i = 0
        while i < length:
            new_file = new_file + encrypted_files[i]
            i += self.block_size

        f = open(path[:len(path.split("\\")[-1]) * -1] + path.split("\\")[-1] + '.encrypted', 'wb')
        f.write(new_file)

        print("작업 성공 | {0}".format(f.name))
        f.close()


class DecryptFile:
    def __init__(self, key, max_threads):
        self.key = key
        self.block_size = 1024*int(1024/2)
        self.maximum_process = max_threads

    def aes_decrypt(self, data):
        from Crypto.Cipher import AES
        cipher = AES.new(self.key, AES.MODE_ECB)

        if len(data) % 16 != 0:
            print("데이터 블록의 크기가 잘못됨")
            import sys
            sys.exit(-1)
        elif len(data) == 0:
            return None
        else:
            return cipher.decrypt(data)

    def decrypt_block(self, block, number, q, process_count):
        process_count.value += 1

        if get_size(block) < 16:
            result = {number: block}

        else:
            i = 0
            decrypted_block = b''
            length = len(block)

            while i < length:
                if i + 16 <= length:
                    decrypted_block += self.aes_decrypt(block[i:i + 16])
                    decrypted_block += block[i + 16:i + 32]
                else:
                    decrypted_block += block[i:]
                i += 32

            result = {number: decrypted_block}

        q.put(result)
        process_count.value += -1

    def decrypt_file(self, path):
        from multiprocessing import Process, Queue, Value
        import time

        if validate_file(path) is False:
            print("파일이 존재하지 않음")
            kill()

        raw_file = read_file(path)
        print("파일 크기 = {0}".format(format_size(get_size(raw_file))))
        if get_size(raw_file) < 16:
            print("파일이 너무 작음")
            kill()

        i = 0
        count = 0
        live_process = Value('i', 0)
        length = len(raw_file)
        maximum_thread = int(length / self.block_size) + 1

        process_list = []
        file_bytes = Queue()

        while i < length:
            p = Process(target=self.decrypt_block, args=(raw_file[i:i+self.block_size], i, file_bytes, live_process, ))
            p.start()
            process_list.append(p)

            i += self.block_size
            count += 1

            printed = False
            while live_process.value > self.maximum_process:
                time.sleep(0.2)
                if printed is False:
                    print("%0.2f" % (((count - 1) / maximum_thread) * 100) + "%")
                    printed = True

        while file_bytes.qsize() < count:
            time.sleep(0.5)
        print("복호화 완료! 결과 모으는중...")

        new_file = b''
        encrypted_files = {}

        while file_bytes.empty() is not True:
            encrypted_files.update(file_bytes.get())

        i = 0
        while i < length:
            new_file = new_file + encrypted_files[i]
            i += self.block_size

        f = open(path[:len(path.split("\\")[-1]) * -1] + path.split("\\")[-1][:path.split("\\")[-1].index(".encrypted")],
                 'wb')
        f.write(new_file)
        print("작업 성공 | {0}".format(f.name))
        f.close()
