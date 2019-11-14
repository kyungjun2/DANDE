import pywintypes
import win32api
import win32con
import win32event
import win32file

FILE_LIST_DIRECTORY = 0x0001
FILE_ACTION_ADDED = 0x00000001
FILE_ACTION_REMOVED = 0x00000002
FILE_ACTION_CHANGED = 0x00000003
FILE_ACTION_RENAMED_PREVIOUS = 0x00000004
FILE_ACTION_RENAMED_CURRENT = 0x00000005

ASYNC_TIMEOUT = 1000  # 1000ms = 1s
BUF_SIZE = 65536  # 64K


def get_dir_handle(dir_name, async_enabled):
    flags_and_attributes = win32con.FILE_FLAG_BACKUP_SEMANTICS
    if async_enabled:
        flags_and_attributes |= win32con.FILE_FLAG_OVERLAPPED

    dir_handle = win32file.CreateFile(
        dir_name,
        FILE_LIST_DIRECTORY,
        (win32con.FILE_SHARE_READ |
         win32con.FILE_SHARE_WRITE |
         win32con.FILE_SHARE_DELETE),
        None,
        win32con.OPEN_EXISTING,
        flags_and_attributes,
        None
    )
    return dir_handle


def read_dir_changes(dir_handle, size_or_buf, overlapped):
    return win32file.ReadDirectoryChangesW(
        dir_handle,
        size_or_buf,
        True,
        (win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
         win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
         win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
         win32con.FILE_NOTIFY_CHANGE_SIZE |
         win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
         win32con.FILE_NOTIFY_CHANGE_SECURITY),
        overlapped,
        None
    )


def monitor_dir_async(file_path, handle_function, run, key):
    dir_handle = get_dir_handle(file_path, True)
    buffer = win32file.AllocateReadBuffer(BUF_SIZE)
    overlapped = pywintypes.OVERLAPPED()
    overlapped.hEvent = win32event.CreateEvent(None, False, 0, None)
    while run.value:
        read_dir_changes(dir_handle, buffer, overlapped)
        rc = win32event.WaitForSingleObject(overlapped.hEvent, ASYNC_TIMEOUT)
        if rc == win32event.WAIT_OBJECT_0:
            bufer_size = win32file.GetOverlappedResult(dir_handle, overlapped, True)
            results = win32file.FILE_NOTIFY_INFORMATION(buffer, bufer_size)
            handle_function(results, file_path, key)
        elif rc == win32event.WAIT_TIMEOUT:
            pass
    win32api.CloseHandle(overlapped.hEvent)
    dir_handle.close()
