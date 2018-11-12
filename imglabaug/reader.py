from xml.etree import ElementTree
from .models import Image


def parse_xml_file(input_file):
    tree = ElementTree.parse(input_file)
    root = tree.find('images')
    output = []
    for item in root.findall('image'):
        output.append(Image().parse(item))
    return output
