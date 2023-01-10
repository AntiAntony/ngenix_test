import os.path
from zipfile import ZipFile

import pytest
import xml.etree.ElementTree as ET

from app import config
from app.zips import create_xml, create_zip

FILE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize(
    "file_name, result",
    [
        ('test', 'test.xml'),
        ('test.xml', 'test.xml'),
        (None, None)
    ]
)
def test_create_xml_result(file_name, result):
    file_name = create_xml(file_name)
    assert file_name == result


def test_create_xml_structure():
    file_name = create_xml('test.xml')
    assert file_name == 'test.xml'
    assert os.path.isfile(f'{file_name}')

    parsed_file = ET.parse(file_name)
    root = parsed_file.getroot()
    assert root.tag == 'root'
    assert root.attrib == {}

    child_tags = set(child.tag for child in root)
    assert child_tags == {'var', 'objects'}

    child_names = set(var_elem.attrib.get('name') for var_elem in root.iter('var'))
    assert child_names == {'id', 'level'}

    var_attribs = set()
    for var_elem in root.iter('var'):
        var_attribs.update(set(var_elem.attrib.keys()))
    assert var_attribs == {'name', 'value'}

    level = root.findall("*[@name='level']")
    level_value = level[0].attrib.get('value')
    assert len(level) == 1
    assert level_value.isnumeric()
    assert 0 < int(level_value) <= config.LEVEL_SIZE

    assert 0 < len(list(root.iter('object'))) <= config.NUM_OBJECTS
    assert all(obj.attrib.get('name').isalnum() for obj in root.iter('object'))


@pytest.mark.parametrize(
    "file_name, result",
    [
        ('test', 'test.zip'),
        ('test.zip', 'test.zip'),
        (None, None)
    ]
)
def test_create_zip_result(file_name, result):
    file_name = create_zip(file_name, 2)
    assert file_name == result


def test_create_zip():
    file_name = create_zip('test.zip', 2)
    with ZipFile(file_name) as zip_file:
        assert zip_file.namelist() == ['1.xml', '2.xml']
