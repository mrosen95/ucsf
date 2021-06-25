import unittest
from template import ShippingAddress, GiftCard

class TestCleanTemplates(unittest.TestCase):
    def test_shipping_address(self):
        match = 'Shipping Address: bla bla bla Shipping Speed:'
        result = ShippingAddress().clean(match)
        self.assertEqual(result, 'Shipping Address: {{PHI}} {{PHI}} {{PHI}} Shipping Speed:')

        missing_end = 'Shipping Address: bla bla bla Shipping '
        self.assertEqual(ShippingAddress().clean(missing_end), missing_end)

        missing_beginning = 'Shipping: bla bla bla Shipping Speed'
        self.assertEqual(ShippingAddress().clean(missing_beginning), missing_beginning)

    def test_billing_address(self):
        match = """Billing address Total before tax: $108.00

        Hermione Granger :
        Estimated tax to be collected:
        Diagon Alley #10

        London, England 27475
        United Kingdom
        Grand Total:"""
        result = ShippingAddress().clean(match)
        self.assertEqual(result, 'Billing address Total before tax: $108.00\n\n        Hermione Granger :\n        Estimated tax to be collected:\n        Diagon Alley #10\n\n        London, England 27475\n        United Kingdom\n        Grand Total:')

        missing_end = match[:-20]
        self.assertEqual(ShippingAddress().clean(missing_end), missing_end)

        missing_beginning = match[10:]
        self.assertEqual(ShippingAddress().clean(missing_beginning), missing_beginning)

    def test_gift_card(self):
        match =  'Order Total: $200.00 Sent Amount E-mail gift card to: dumbledore@gmail.com $100.00 From: Harry Potter Message:'
        self.assertEqual(GiftCard().clean(match), 'Order Total: $200.00 Sent Amount E-mail gift card to: {{PHI}} $100.00 From: {{PHI}} {{PHI}} Message:')

        missing_end = 'Order Total: $200.00 Sent Amount E-mail gift card to: dumbledore@gmail.com $100.00 From: Harry Potter'
        self.assertEqual(GiftCard().clean(missing_end), missing_end)

        missing_beginning = 'gift card to: dumbledore@gmail.com $100.00 From: Harry Potter Message:'
        self.assertEqual(GiftCard().clean(missing_beginning), missing_beginning)


if __name__ == '__main__':
    unittest.main()
