import ctypes
import os

libpath: str = os.path.abspath("lib/libhash/build/libhash.so")
lib = ctypes.CDLL(libpath)

# ====
# FNV-1a binding
# ====
lib.fnv1a.argtypes = [ctypes.c_char_p, ctypes.c_size_t]
lib.fnv1a.restype = ctypes.c_uint64
def fnv1a(data: bytes) -> int:
    return lib.fnv1a(data, len(data))

# ====
# FNV-1a (file) binding
# ====
lib.fnv1a_file.argtypes = [ctypes.c_char_p]
lib.fnv1a_file.restype = ctypes.c_ulong
def fnv1a_file(filename: str) -> int:
    return lib.fnv1a_file(filename.encode())
