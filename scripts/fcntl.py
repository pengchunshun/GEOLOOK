"""fcntl 兼容层（Windows）。

geolib.py 依赖 Unix 专属的 fcntl 模块做项目级跨进程文件锁。
本模块在 Windows 上用 msvcrt.locking 提供等价实现；
在 macOS / Linux / WSL 下则透明转发到真实的 _fcntl 实现。
"""

try:
    # macOS / Linux / WSL：直接透传真实实现
    from _fcntl import *  # noqa: F401,F403
    from _fcntl import __doc__  # noqa: F401
except ImportError:  # pragma: no cover - Windows 专用
    import msvcrt

    LOCK_SH = 1  # 共享锁
    LOCK_EX = 2  # 排他锁
    LOCK_NB = 4  # 非阻塞
    LOCK_UN = 8  # 解锁

    def flock(fd, operation):
        """msvcrt 版 flock：锁定文件第一个字节区域。"""
        pos = fd.tell()
        try:
            fd.seek(0, 2)
            if fd.tell() == 0:
                # msvcrt.locking 需要文件至少有一个字节可锁
                fd.write(" ")
                fd.flush()
            fd.seek(0)
            handle = fd.fileno()
            if operation == LOCK_UN:
                msvcrt.locking(handle, msvcrt.LK_UNLCK, 1)
            elif operation == (LOCK_EX | LOCK_NB):
                try:
                    msvcrt.locking(handle, msvcrt.LK_NBLCK, 1)
                except OSError:
                    raise BlockingIOError(
                        "resource temporarily unavailable")
            elif operation == LOCK_EX:
                msvcrt.locking(handle, msvcrt.LK_LOCK, 1)
            elif operation == (LOCK_SH | LOCK_NB):
                try:
                    msvcrt.locking(handle, msvcrt.LK_NBRLCK, 1)
                except OSError:
                    raise BlockingIOError(
                        "resource temporarily unavailable")
            elif operation == LOCK_SH:
                msvcrt.locking(handle, msvcrt.LK_RLCK, 1)
            else:
                raise NotImplementedError(
                    f"不支持的文件锁操作: {operation}")
        finally:
            try:
                fd.seek(pos)
            except OSError:
                pass
