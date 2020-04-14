import cython
import cython.util

libzfs = cython.CDLL(str(
    cython.util.find_library("zfs")
))

libzfs.zfs_is_mounted

