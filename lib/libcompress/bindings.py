import ctypes
import os

libpath: str = os.path.abspath("lib/libcompress/build/libcompress.so")
lib = ctypes.CDLL(libpath)

# ====
# Compress binding
# ====
lib.huf_compress.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.huf_compress.restype = None
def huf_compress(input_file: str, output_file: str) -> None:
    lib.huf_compress(input_file.encode('utf-8'), output_file.encode('utf-8'))

# ====
# Compress binding
# ====
lib.huf_decompress.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.huf_decompress.restype = None
def huf_decompress(input_file: str, output_file: str) -> None:
    lib.huf_decompress(input_file.encode('utf-8'), output_file.encode('utf-8'))
