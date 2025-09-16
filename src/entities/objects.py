import os
from lib.libcompress.bindings import huf_compress

def create_source_object(storage_path: str, state_id: int, file_path: str, file_path_hash: str) -> str | None:
    obj_dir_path: str = os.path.join(storage_path, f"{state_id}")
    obj_path: str = os.path.join(obj_dir_path, file_path_hash)

    os.makedirs(obj_dir_path, exist_ok = True)
    if not os.path.exists(file_path):
        print(f"Unable to create object, file: \"{file_path}\" does not exist.")
        return None
    if not os.path.isfile(file_path):
        print(f"Unable to create object, file: \"{file_path}\" is not a regular file.")
        return None
    if os.path.getsize(file_path) == 0:
        print(f"Unable to create object, file: \"{file_path}\" is empty.")
        return None

    huf_compress(file_path, obj_path)
    return obj_path
