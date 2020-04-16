import ctypes
import ctypes.util

libzfs = ctypes.CDLL(str(
    ctypes.util.find_library("zfs")
))

LZC_DATASET_TYPE_ZFS = 2

ZFS_TYPE_FILESYSTEM = (1 << 0)
ZFS_TYPE_SNAPSHOT   = (1 << 1)
ZFS_TYPE_VOLUME     = (1 << 2)
ZFS_TYPE_POOL       = (1 << 3)
ZFS_TYPE_BOOKMARK   = (1 << 4)


class ZFS:

    def __init__(self):
        self._zfs_handle = self.__zfs_init()

    def __dealloc__(self):
        if self.__zfs_handle is not None:
            libzfs.libzfs_fini(self.__zfs_handle)

    def __zfs_init(self) -> ctypes.c_void_p:
        libzfs_init = libzfs.libzfs_init
        libzfs_init.restype = ctypes.c_void_p
        return ctypes.c_void_p(libzfs_init())

    def __zfs_open(
        self,
        dataset_name: bytes,
        dataset_type: int=(ZFS_TYPE_FILESYSTEM|ZFS_TYPE_VOLUME)
    ) -> ctypes.c_void_p:
        zfs_open = libzfs.zfs_open
        zfs_open.restype = ctypes.c_void_p
        res = zfs_open(
            self._zfs_handle,
            ctypes.c_char_p(dataset_name),
            ctypes.c_int(dataset_type)
        )
        if res is None:
            raise Exception("dataset not found")
        return ctypes.c_void_p(res)

    def mountpoint(self, dataset_name: bytes) -> bytes:
        zfs_is_mounted = libzfs.zfs_is_mounted
        zfs_is_mounted.restype = ctypes.c_bool

        dataset_handle = self.__zfs_open(dataset_name)
        res = ctypes.c_char_p()
        ret = zfs_is_mounted(
            dataset_handle,
            ctypes.POINTER(type(res))(res)
        )
        libzfs.zfs_close(dataset_handle)

        return res.value if (ret is True) else None


__zfs = ZFS()
mountpoint = __zfs.mountpoint
