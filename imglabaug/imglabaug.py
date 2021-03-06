from .reader import parse_xml_file
from .models import XMLFile, Image, Part, Box

import uuid
import cv2
import os
import copy
import imutils
import math
import random

from itertools import combinations


def random_string():
    return uuid.uuid4().hex


def rotate(origin, point, angle):
    angle = math.radians(-angle)

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

    return int(qx), int(qy)


def randrange(a, b):
    return random.randrange(a, b)


operation_blur = "blur"
operation_rotate = "rotate"
operation_crop = "crop"
operation_move = "move"


class Augmentation:
    def __init__(
            self,
            output_directory,

            min_rotation_angle=0,
            max_rotation_angle=0,

            min_move_offset_y=0,
            max_move_offset_y=0,

            min_move_offset_x=0,
            max_move_offset_x=0,

            max_blur_size=1,
            min_blur_size=1,

            # crop is under development.
            # crop_offset_x=0,
            # crop_offset_y=0,

            iterations_length=100,
    ):
        self.min_rotation_angle = min_rotation_angle
        self.max_rotation_angle = max_rotation_angle

        self.min_blur_size = min_blur_size
        self.max_blur_size = max_blur_size

        crop_offset_x = 0
        crop_offset_y = 0
        self.crop_offset_x = crop_offset_x
        self.crop_offset_y = crop_offset_y        

        self.min_move_offset_y = min_move_offset_y
        self.max_move_offset_y = max_move_offset_y
        self.min_move_offset_x = min_move_offset_x
        self.max_move_offset_x = max_move_offset_x

        self.iterations_length = iterations_length

        self._operations = []
        if max_blur_size - min_blur_size:
            self._operations.append(operation_blur)
        if crop_offset_x + crop_offset_y:
            self._operations.append(operation_crop)
        if max_rotation_angle - min_rotation_angle:
            self._operations.append(operation_rotate)
        if (max_move_offset_x - min_move_offset_x > 0) or (max_move_offset_y - min_move_offset_y > 0):
            self._operations.append(operation_move)

        self.xml_file = XMLFile(name="imglab dataset",
                                comment="Generated by imglabaug")
        self.output_directory = output_directory
        self.images_directory = os.path.join(output_directory, "images")
        self.output_file = os.path.join(self.output_directory, "output.xml")

        os.mkdir(self.output_directory)
        os.mkdir(self.images_directory)

    def _handle_move(self, item, image):
        offset_x = randrange(self.min_move_offset_x, self.max_move_offset_x)
        offset_y = randrange(self.min_move_offset_y, self.max_move_offset_y)
        shifted = imutils.translate(image, offset_x, offset_y)
        output_file = os.path.join(
            self.images_directory, random_string() + ".jpg")
        cv2.imwrite(output_file, shifted)

        image_element = Image(output_file)
        for box_item in item.boxes:
            x, y = box_item.left, box_item.top
            cx = x + offset_x
            cy = y + offset_y

            if cx < 0 or cy < 0:
                continue

            x = cx
            y = cy

            box = Box()
            box.left = x
            box.top = y
            box.width = box_item.width
            box.height = box_item.height

            for part_item in box_item.parts:
                part = Part()
                part.x = part_item.x + offset_x
                part.y = part_item.y + offset_y
                part.name = part_item.name
                box.parts.append(part)

            image_element.boxes.append(box)

        self.xml_file.append_image(image_element)

    def _handle_rotate(self, item, image):
        height, width = image.shape[:2]

        angle = randrange(self.min_rotation_angle, self.max_rotation_angle)
        output_file = os.path.join(
            self.images_directory, random_string() + ".jpg")
        rotated = imutils.rotate(image, angle)
        cv2.imwrite(output_file, rotated)

        origin = (width/2, height/2)

        image_element = Image(output_file)
        for box_item in item.boxes:
            x, y, w, h = box_item.left, box_item.top, box_item.width, box_item.height

            cx, cy = x + w/2, y+h/2
            cx, cy = rotate(origin, (cx, cy), angle)

            box = Box()
            box.left = cx - w/2
            box.top = cy - h/2
            box.width = w
            box.height = h

            for part_item in box_item.parts:
                part = Part()
                part.x, part.y = rotate(
                    origin, (part_item.x, part_item.y), angle)
                part.name = part_item.name
                box.parts.append(part)

            image_element.boxes.append(box)

        self.xml_file.append_image(image_element)

    def _handle_blur(self, item, image):
        blur_size = randrange(self.min_blur_size, self.max_blur_size)
        output_file = os.path.join(
            self.images_directory, random_string() + ".jpg")
        blurred = cv2.blur(image, (blur_size, blur_size))
        cv2.imwrite(output_file, blurred)

        image_element = Image(output_file)
        for box_item in item.boxes:
            x, y = box_item.left, box_item.top

            box = Box()
            box.left = x
            box.top = y
            box.width = box_item.width
            box.height = box_item.height

            for part_item in box_item.parts:
                part = Part()
                part.x = part_item.x
                part.y = part_item.y
                part.name = part_item.name
                box.parts.append(part)

            image_element.boxes.append(box)

        self.xml_file.append_image(image_element)

    def _process(self, item, image):
        for _ in range(self.iterations_length):
            selector = self._operations[randrange(0, len(self._operations))]

            if selector == operation_rotate:
                self._handle_rotate(item, image)
            elif selector == operation_move:
                self._handle_move(item, image)
            elif selector == operation_crop:
                pass
            elif selector == operation_blur:
                self._handle_blur(item, image)

    def generate(self, input_xml_file):
        directory = os.path.dirname(input_xml_file)
        image_items = parse_xml_file(input_xml_file)

        for image_item in image_items:
            image_file = os.path.join(directory, image_item.image_file)
            image = cv2.imread(image_file)

            self._process(image_item, image)

    def __str__(self):
        return self.xml_file.__str__()

    def save(self):
        self.xml_file.save(self.output_file)
