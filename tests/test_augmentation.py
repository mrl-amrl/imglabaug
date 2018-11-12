import os
import unittest

from imglabaug import Augmentation


class AugmentationTest(unittest.TestCase):
    """
    Test methods in Augmentation
    """

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_augmentation(self):
        samples = os.path.join("tests", "samples")
        faces = os.path.join(samples, "faces")
        augmentation = Augmentation(rotate_angle=(0, 3), blur_size=(0, 3))
        augmentation.process(os.path.join(faces, "faces.xml"))

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
