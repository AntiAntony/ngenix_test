import csv
import os
import shutil
import string
import time
from random import choices
from typing import Iterable, Any, List, Union


def random_string(char_len: int) -> Union[str, None]:
    """Generate random string with given character length"""
    if char_len < 1:
        return None
    return ''.join(choices(string.ascii_uppercase + string.digits, k=char_len))


def clean_dir(dir_name: str, exclude_types=None):
    """Delete files from directory, exclude list of extensions"""
    for filename in os.listdir(dir_name):
        if any(et in filename for et in exclude_types):
            continue
        file_path = os.path.join(dir_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            pass


def make_csv(file_name: str, data: Iterable[Iterable[Any]]) -> None:
    """Write data to csv file"""
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)


def find_files_in_dir(dir_path: str, extension: List = None) -> List[str]:
    """Get all files in directory recursively with given extensions"""
    if not extension:
        extension = ['.']
    all_files = []
    for (dir_path, _, file_names) in os.walk(dir_path):
        all_files.extend([f'{dir_path}/{file_name}' for file_name in file_names])
    return [file for file in all_files if any(ext in file for ext in extension)]


class Timer:
    def __init__(self, task_name='Task'):
        self.start = time.time()
        self.task_name = f'<{task_name}>'

    def __enter__(self):
        pass
        # print(f'Start <{self.task_name}>')

    def __exit__(self, type, value, traceback):
        print(f'{self.task_name:<30} | {time.time() - self.start:.2f} sec')

