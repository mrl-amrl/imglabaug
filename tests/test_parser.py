import os
import unittest

from imglabaug import parse_xml_file


class ParseXMLFileTest(unittest.TestCase):
    """
    Test methods in parse_xml_file
    """

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_parser(self):
        samples = os.path.join("tests", "samples")
        faces = os.path.join(samples, "faces")
        result = parse_xml_file(os.path.join(faces, "faces.xml"))
        self.assertTrue(len(result) == 1)
        self.assertTrue(len(result[0].boxes) == 4)
        self.assertTrue(len(result[0].boxes[0].parts) == 2)


if __name__ == '__main__':
    unittest.main()
