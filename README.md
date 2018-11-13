# imglab + aug = imglabaug
> Image augmentation for dlib's imglab XML files.

[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

### Installation

Provided you already have `imutils`, `opencv` already installed, the `imglabaug` package is completely pip-installable:

```
$ pip install imglabaug
```

### Examples

```python
from imglabaug import Augmentation

augmentation = Augmentation(
            output_directory='somewhere !',
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

augmentation.generate('xml file ...')
augmentation.save()
```

---

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)