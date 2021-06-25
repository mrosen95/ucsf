from typing import List
import re
from word import Word
from read import PDFFile
import scrubadub
import cleantext
from template import ShippingAddress, BillingAddress, GiftCard

# List of identifiers that we mark as clean
CLEAN_IDENTIFIERS = {"{{EMAIL}}", "{{NAME}}","{{ADDRESS}}", "{{PHI}}"}
TEMPLATE_PLACEHOLDER = "{{TEMPLATE}}"
# default the list of templates to check for to this list.
TEMPLATES = [ShippingAddress(), BillingAddress(), GiftCard()]


class Redactor:
    def __init__(self, words: List[Word], templates=TEMPLATES):
        self.words = words
        text_list = []
        for w in words:
            text_list.append(w.text)

        self.full_text = ' '.join(text_list)
        self.templates = templates

    def __remove_template_words(self):
        """
        Remove template words understands that we are using a common amazon
        template. We are going to iterate through and find the places in the
        template whre those words are used to avoid removing any PII.

        It relies on the ordering
        """
        return

    def redact_regex(self, pdf: PDFFile) -> PDFFile:
        """
        redact_regex relies on a series of regex templates that have been created
        with regards to the amazon templates we see.
        """

        cleaned_text = self.full_text
        for template in self.templates:
            cleaned_text = template.clean(cleaned_text)

        cleaned_list = cleaned_text.split(' ')
        for i, w in enumerate(self.words):
            if cleaned_list[i] in CLEAN_IDENTIFIERS:
                w.redact(pdf)
        return pdf

    def redact_scrubadub(self, pdf: PDFFile) -> PDFFile:
        """
        redact is going to clean the text in the file and return
        a pdf with the file with blocked out words.
        """
        cleaned_text = scrubadub.clean(self.full_text).split(' ')
        for i, w in enumerate(self.words):
            if cleaned_text[i] in CLEAN_IDENTIFIERS:
                w.redact(pdf)
        return pdf
