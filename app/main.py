import itertools
import multiprocessing
import os
import xml.etree.ElementTree as ET
from typing import Tuple, List
from zipfile import ZipFile

from .config import DIR_PATH, CORES, NUM_ZIP_FILES
from .helpers import clean_dir, find_files_in_dir, make_csv, Timer
from .zips import generate_zips

CPUS = CORES or multiprocessing.cpu_count()


def extract_worker(file: str) -> None:
    dir_file_name = f'dir_{os.path.basename(file).strip(".zip")}'
    os.mkdir(f'{DIR_PATH}/{dir_file_name}')
    zip = ZipFile(file)
    zip.extractall(path=f'{DIR_PATH}/{dir_file_name}')


def process_worker(file: str) -> Tuple[Tuple[str, str], List[Tuple[str, str]]]:
    parsed_file = ET.parse(file)
    root = parsed_file.getroot()
    file_id = None
    file_level = None
    for v in root.iter('var'):
        var_value = v.attrib.get('value')
        var_name = v.attrib.get('name')
        if var_name == 'id':
            file_id = var_value
        elif var_name == 'level':
            file_level = var_value
    return (file_id, file_level), \
           [(file_id, obj.attrib.get('name')) for obj in root.iter('object')]


def no_multiprocess():
    print('No MULTIPROCESSING')

    with Timer(task_name='Extracting files'):
        for file in find_files_in_dir(DIR_PATH, ['.zip']):
            extract_worker(file)

    with Timer(task_name='Process files'):
        results = []
        for file in find_files_in_dir(DIR_PATH, ['.xml']):
            results.append(process_worker(file))

    with Timer(task_name='Write csv'):
        make_csv('levels.csv', [levels for levels, _ in results])
        make_csv('objects.csv', list(itertools.chain.from_iterable(objects for _, objects in results)))


def multiprocess():
    print(f'MULTIPROCESSING Cores {CPUS}')

    with Timer(task_name='Extracting files'):
        pool = multiprocessing.Pool(processes=CPUS)
        _ = [pool.map(extract_worker, find_files_in_dir(DIR_PATH, ['.zip']))]

    with Timer(task_name='Process files'):
        pool = multiprocessing.Pool(processes=CPUS)
        results = pool.map_async(process_worker, find_files_in_dir(DIR_PATH, ['.xml']))
        pool.close()
        pool.join()
        results = results.get()

    with Timer(task_name='Write csv'):
        make_csv('levels.csv', [levels for levels, _ in results])
        make_csv('objects.csv', list(itertools.chain.from_iterable(objects for _, objects in results)))


if __name__ == "__main__":
    clean_dir(DIR_PATH, exclude_types=['.py'])
    with Timer(task_name='Generate zips'):
        generate_zips(NUM_ZIP_FILES)

    no_multiprocess()
    clean_dir(DIR_PATH, exclude_types=['.py', '.zip'])
    multiprocess()
    clean_dir(DIR_PATH, exclude_types=['.py'])

