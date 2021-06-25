from read import PDFReader
import word
import cv2
import numpy as np
from clean import Redactor
import argparse

def main(file_name):
    reader = PDFReader("files/" + file_name)
    pdf = reader.read()
    words = pdf.read_words()
    redactor = Redactor(words)
    pdf = redactor.redact_regex(pdf)

    out_file = "redacted/{fname}".format(fname=file_name).replace('.pdf', '.png')
    print("saved file to: " + out_file)
    cv2.imwrite(out_file, pdf.page(0))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--filename', type=str, default='example2.pdf', help='file location for the image')
    args = parser.parse_args()
    main(args.filename)
