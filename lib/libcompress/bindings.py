import ctypes
import os

file_path: str = os.path.dirname(os.path.abspath(__file__))
lib_path: str = os.path.join(file_path, "../../lib/libcompress/build/libcompress.so")
lib = ctypes.CDLL(os.path.normpath(lib_path))

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
