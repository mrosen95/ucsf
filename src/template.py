import re
import numpy as np

class Template():
    def extract_regions(self, text):
        """
        extract_regions pulls certain regions from a string to indicate that it
        is a specific data element that we care about.

        Each template type will implement this to pull the data appropriately.
        """
        pass

    def clean(self, text):
        """
        clean is a function that is going to remove the PHI in extracted
        regions.

        The method for removing will be specific to the type of template element.
        """
        pass


class ShippingAddress(Template):
    def __init__(self):
        self.pattern = 'Shipping Address: ([\s\S]*) Shipping Speed'

    def extract_regions(self, text):
        matches = re.findall(self.pattern, text)
        return matches

    def clean(self, text):
        matches = self.extract_regions(text)
        if matches == None:
            return text

        # Iterate over the extracted regions and removed the PHI containing
        # pieces in between the two values.
        for match in matches:
            words = match.split(' ')
            # Skip over the beginning and the last pieces.
            for i in range(len(words)):
                words[i] = '{{PHI}}'
            text = text.replace(match, ' '.join(words))
        return text

class GiftCard(Template):
    def __init__(self):
        self.pattern = 'E-mail gift card to: ([\S]*@[\S]*\.[\S]*) \$[\d]*\.\d\d From: ([a-zA-Z]+[\s][a-zA-Z]+) Message'

    def extract_regions(self, text):
        """
        extract_regions is going to only pull out the PHI information.
        """
        return re.findall(self.pattern, text)

    def clean(self, text):
        matches = self.extract_regions(text)
        if matches == None:
            return text
        matches = np.array(self.extract_regions(text)).flatten()

        for match in matches:
            # This empty space will occur in instances where there is no second
            # match.
            if match == ' ':
                continue

            words = match.split(' ')
            for i in range(len(words)):
                words[i] = '{{PHI}}'
            text = text.replace(match, ' '.join(words))
        return text

class BillingAddress(Template):
    def __init__(self):
        """
        Billing address Total before tax: $108.00

        Hermione Granger :
        Estimated tax to be collected:
        Diagon Alley #10

        London, England 27475
        United Kingdom
        Grand Total:"""
        self.pattern = 'Billing address Total before tax: \$[\d]*\.\d\d([\s\S]*)Estimated tax to be collected:([\s\S]*)Grand Total:'

    def extract_regions(self, text):
        """
        extract_regions is going to only pull out the PHI information.
        """
        return re.findall(self.pattern, text)

    def clean(self, text):
        matches = self.extract_regions(text)
        if matches == None:
            return text

        for match in matches[0]:
            # This empty space will occur in instances where there is no second
            # match.
            if match == ' ':
                continue

            words = match.split(' ')
            for i in range(len(words)):
                words[i] = '{{PHI}}'
            text = text.replace(match, ' '.join(words))
        return text
