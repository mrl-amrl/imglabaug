from xml.dom.minidom import parseString


class XMLFile:
    def __init__(self, name="", comment=""):
        self.name = name
        self.comment = comment
        self.images = []

    def append_image(self, image):
        self.images.append(image)

    def __str__(self):
        output = """<?xml version='1.0' encoding='ISO-8859-1'?>
                <dataset>
                <name>{name}</name>
                <comment>{comment}</comment>
                <images>
                """.format(name=self.name, comment=self.comment)

        for image in self.images:
            output += image.__repr__()

        output += "</images>"
        output += "</dataset>"
        return parseString(output).toprettyxml()

    def save(self, output_file):
        with open(output_file, 'w') as output_stream:
            output_stream.write(self.__str__())


class Image:
    def __init__(self, image_file=""):
        self.image_file = image_file
        self.boxes = []

    def parse(self, image_child):
        self.image_file = image_child.attrib['file']
        for item in image_child:
            self.boxes.append(Box().parse(item))

        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = "<image file='{}'>".format(self.image_file)

        for box in self.boxes:
            output += box.__repr__()

        output += "</image>"

        return output


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

    def __str__(self):
        return "<part name='{name}' x='{x}' y='{y}'/>".format(name=self.name, x=self.x, y=self.y)

    def __repr__(self):
        return self.__str__()


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

    def __str__(self):
        output = "<box top='{top}' left='{left}' width='{width}' height='{height}'>".format(top=self.top,
                                                                                            left=self.left,
                                                                                            width=self.width,
                                                                                            height=self.height)

        for part in self.parts:
            output += part.__repr__()

        output += "</box>"

        return output

    def __repr__(self):
        return self.__str__()
