import multiprocessing
import os
import uuid
import xml.etree.ElementTree as ET
from random import randrange
from typing import Union
from zipfile import ZipFile

from .helpers import random_string
from .config import NUM_OBJECTS, LEVEL_SIZE, DIR_PATH, NUM_XML_FILES_IN_ZIP


def create_xml(xml_name: str) -> Union[str, None]:
    if not xml_name:
        return None
    xml_name = xml_name if '.xml' in xml_name else f'{xml_name}.xml'
    root_el = ET.Element('root')
    file_id = uuid.uuid4()
    ET.SubElement(root_el, 'var', attrib={'name': 'id',
                                          'value': str(file_id)})
    ET.SubElement(root_el, 'var', attrib={'name': 'level',
                                          'value': str(randrange(1, LEVEL_SIZE + 1))})
    objects_el = ET.Element('objects')
    for _ in range(randrange(1, NUM_OBJECTS)):
        ET.SubElement(objects_el, 'object', attrib={'name': random_string(10)})
    root_el.append(objects_el)
    tree = ET.ElementTree(root_el)
    tree.write(xml_name)
    return xml_name


def create_zip(zip_name: str, xml_quantity: int) -> Union[str, None]:
    if xml_quantity < 1 or not zip_name:
        return None
    zip_name = zip_name if '.zip' in zip_name else f'{zip_name}.zip'
    with ZipFile(f'{DIR_PATH}/{zip_name}', 'w') as zip_file:
        for i in range(1, xml_quantity + 1):
            file = create_xml(xml_name=random_string(8))
            zip_file.write(file, arcname=f'{i}.xml')
            os.unlink(file)
    return zip_name


def generate_zips(zip_quantity: int) -> None:
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    _ = [pool.starmap(create_zip, [(str(i), NUM_XML_FILES_IN_ZIP) for i in range(1, zip_quantity + 1)])]




