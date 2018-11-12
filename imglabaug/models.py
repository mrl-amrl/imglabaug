class Image:
    def __init__(self):
        self.image_file = ""
        self.boxes = []

    def parse(self, image_child):
        self.image_file = image_child.attrib['file']
        for item in image_child:
            self.boxes.append(Box().parse(item))

        return self


class Part:
    def __init__(self):
        self.name = ""
        self.x = 0
        self.y = 0

    def parse(self, item_child):
        self.name = item_child.attrib['name']
        self.x = int(item_child.attrib['x'])
        self.y = int(item_child.attrib['y'])

        return self


class Box:
    def __init__(self):
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.right = 0
        self.bottom = 0

        self.parts = []

    def parse(self, item_child):
        self.left = int(item_child.attrib['left'])
        self.top = int(item_child.attrib['top'])
        self.width = int(item_child.attrib['width'])
        self.height = int(item_child.attrib['height'])
        self.bottom = self.top + self.height
        self.right = self.left + self.width

        for item in item_child:
            self.parts.append(Part().parse(item))

        return self
