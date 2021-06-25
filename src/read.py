import word
import pytesseract
import word
import constant
import cv2
import errno
import os
import pdf2image
from PIL import Image
import numpy as np
from io import BytesIO



class PDFReader:
    def __init__(self, file_name):
        self.file_name = file_name


    def __convert_pdf_to_image(self, dpi):
        """
        Converts our pdf in as a list of images so that pyesseract can work.

        dpi is a measure of the image quality. Its value should be >300
        """
        images = []
        images.extend(
                        list(
                            map(
                                lambda image: cv2.cvtColor(
                                    np.asarray(image), code=cv2.COLOR_RGB2BGR
                                ),
                                pdf2image.convert_from_path(self.file_name, dpi=dpi),
                            )
                        )
                    )
        return images

    def read(self):
        # TODO: add a try catch here.
        # convert_from path converts pdf into images
        page_images = self.__convert_pdf_to_image(500)
        if page_images == None:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.file_name)

        #cv2.imshow('bla', gray_pages[0])
        return PDFFile(page_images)

class PDFFile:
    def __init__(self, page_images):
        self.page_images = page_images

    def read_words(self):
        """
        read_words reads the pdf image and splits it into words. Each word has
        string location and page number.
        """
        words = []
        for page_number, page in enumerate(self.page_images):
            words.extend(self.__read_words_on_page(page_number))
        return words

    def page(self, page_number):
        # TODO: throw exception.
        return self.page_images[page_number]

    def __read_words_on_page(self, page_number):
        boxes = pytesseract.image_to_data(self.page(page_number))
        words = []
        headers = []
        for i, line in enumerate(boxes.splitlines()):
            line = line.split()
            if i == 0:
                headers = line
                continue

            # If no text value is present, the number of values in the line
            # will be smaller than the number of headers. We use that as our
            # method for deciding what to avoid.
            if len(line) < len(headers):
                continue

            # Some messy text will slip through with no alphanumeric characters.
            # We don't care about these elements.
            text = line[constant.WORD_INDEX]
            if not any(c.isalnum() for c in text):
                continue

            # TODO: it might not be best to rely on indexing here, but we are going to say
            # for now that this optimziation is worth it. I find it hard to believe that the
            # pacakge will change the indexing.
            x,y,width,height = int(line[constant.X_VALUE_INDEX]), int(line[constant.Y_VALUE_INDEX]), int(line[constant.WIDTH_INDEX]), int(line[constant.HEIGHT_INDEX])

            w = word.Word(text, x,y,width, height, page_number)
            words.append(w)

        return words


    def write(self, out_fname):
        pdf_images = []
        for page in self.page_images:
            pdf_images.append(cv2.cvtColor(np.asarray(page), code=cv2.COLOR_BGR2RGB))

        pdf_images[0].save(out_fname, save_all = True, quality=100, append_images = pdf_images[1:])
        return
