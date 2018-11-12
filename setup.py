from setuptools import setup

setup(
    name="imglabaug",
    packages=['imglabaug'],
    version="0.0.1",
    description="Image augmentation for dlib's imglab XML files.",
    url="http://github.com/mrl-amrl/imglabaug",
    author="Ahmadreza Zibaei",
    author_email="zibaeiahmadreza@gmail.com",
    license='MIT',
    zip_safe=False,
    keywords=['dlib', 'image processing', 'opencv', 'imglab'],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
