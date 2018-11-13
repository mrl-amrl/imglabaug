import os
import shutil
import tempfile
import unittest

from imglabaug.models import XMLFile, Image, Box


class XMLFileTest(unittest.TestCase):
    """
    Test methods in XMLFile
    """

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_xml_generator(self):
        path = tempfile.mktemp()
        output_file = os.path.join(path, "output.xml")
        os.mkdir(path)

        try:
            xml_file = XMLFile(name="test from generator", comment="hello world !")

            image = Image()
            image.image_file = "test_image.jpg"

            box = Box()
            box.left = 10
            box.top = 20
            box.width = 100
            box.height = 120
            image.boxes.append(box)

            xml_file.append_image(image)
            xml_file.save(output_file)
        finally:
            self.assertTrue(os.path.exists(output_file))
            shutil.rmtree(path)


if __name__ == '__main__':
    unittest.main()
