import os
import unittest
import tempfile
import shutil

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

        # tmp_directory = tempfile.mktemp()
        tmp_directory = "/tmp/test_imglabaug"
        if os.path.exists(tmp_directory):
            shutil.rmtree(tmp_directory)

        augmentation = Augmentation(
            output_directory=tmp_directory,            
            max_blur_size=9,
            min_blur_size=1,            
            min_move_offset_x=-10,
            max_move_offset_x=10,
            min_move_offset_y=-10,
            max_move_offset_y=10,
            min_rotation_angle=-10,
            max_rotation_angle=10,
            iterations_length=20,
        )

        augmentation.generate(os.path.join(faces, "faces.xml"))
        augmentation.save()

        print "Saved to " + augmentation.output_file

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
