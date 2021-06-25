import pytesseract
import cv2
import constant
import numpy as np

class Word:
    def __init__(self, text, x, y, width, height, page_number):
        self.text = text
        self.dimensions = Position(x,y,width,height)
        self.page_number = page_number

    def redact(self, pdf):
        cv2.rectangle(pdf.page(self.page_number), self.dimensions.lower_left_corner(), self.dimensions.upper_right_corner(), constant.RECTANGLE_COLOR, constant.RECTANGLE_THICKNESS)

class Position:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def lower_left_corner(self):
        return (self.x,self.y)

    def upper_right_corner(self):
        return (self.x + self.width, self.y + self.height)
