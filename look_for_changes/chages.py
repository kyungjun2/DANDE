import os

import win32con
import win32file

actions = \
    {
        1: '파일 생성',
        2: '파일 삭제',
        3: '파일 변경',
        4: '파일 이름 바뀜 - 원본 파일명',
        5: '파일 이름 바뀜 - 바뀐 파일명'
    }


def read_changes(watch_path, stop, queue):
    if os.path.isdir(watch_path) is False:
        return -1

    hDir = win32file.CreateFile(watch_path,
                                     1,
                                     win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
                                     None,
                                     win32con.OPEN_EXISTING,
                                     win32con.FILE_FLAG_BACKUP_SEMANTICS,
                                     None)
    while stop.value:
        results = win32file.ReadDirectoryChangesW(hDir,
                                                  1024,
                                                  True,
                                                  win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                                  win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                                  win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                                  win32con.FILE_NOTIFY_CHANGE_SIZE |
                                                  win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
                                                  None,
                                                  None)

        for action, file in results:
            queue.put([action, file])

    return 0