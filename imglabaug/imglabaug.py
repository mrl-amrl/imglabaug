from .reader import parse_xml_file

import cv2
import os
import imutils
import math


def rotate(origin, point, angle):
    angle = math.radians(angle)

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return qx, qy


class Augmentation:
    def __init__(self, rotate_angle=(0, 0), blur_size=(0, 0)):
        self.rotate_angles = range(rotate_angle[0], rotate_angle[1])
        self.blur_sizes = range(blur_size[0], blur_size[1])

    def process(self, input_xml_file):
        directory = os.path.dirname(input_xml_file)
        image_items = parse_xml_file(input_xml_file)

        for image_item in image_items:
            image_file = os.path.join(directory, image_item.image_file)

            image = cv2.imread(image_file)

            for box_item in image_item.boxes:
                x = box_item.left
                y = box_item.top
                w = box_item.width
                h = box_item.height

                roi = image[y:y + h, x:x + w]
