import ctypes
import os

libpath: str = os.path.abspath("lib/libcompress/build/libcompress.so")
lib = ctypes.CDLL(libpath)

# ====
# Compress binding
# ====
lib.compress.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.compress.restype = None
def compress(input_file: str, output_file: str) -> None:
    lib.compress(input_file.encode('utf-8'), output_file.encode('utf-8'))

# ====
# Compress binding
# ====
lib.decompress.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.decompress.restype = None
def decompress(input_file: str, output_file: str) -> None:
    lib.decompress(input_file.encode('utf-8'), output_file.encode('utf-8'))
