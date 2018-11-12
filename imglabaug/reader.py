from xml.etree import ElementTree
from .models import Image


def parse_xml_file(input_file):
    tree = ElementTree.parse(input_file)
    root = tree.find('images')
    for item in root.findall('image'):
        yield Image().parse(item)
