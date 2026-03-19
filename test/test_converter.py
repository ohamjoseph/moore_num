import unittest
import sys
import os

# Ensure the parent directory is in the path for testing the local package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from moore_num.converter import convert_to_text, text_to_num

class TestMooreConverter(unittest.TestCase):

    def test_units(self):
        cases = {
            0: "zaalem",
            1: "ye",
            2: "yiibu",
            5: "nu",
            10: "piiga"
        }
        for n, text in cases.items():
            self.assertEqual(convert_to_text(n), text)
            self.assertEqual(text_to_num(text), n)

    def test_tens(self):
        cases = {
            20: "pisi",
            21: "pisi la a ye",
            45: "pis-naase la a nu"
        }
        for n, text in cases.items():
            self.assertEqual(convert_to_text(n), text)
            self.assertEqual(text_to_num(text), n)

    def test_hundreds(self):
        cases = {
            100: "koabga",
            101: "koabg la a ye",
            200: "kobsi",
            300: "kobs-tã",
            500: "kobs-nu"
        }
        for n, text in cases.items():
            self.assertEqual(convert_to_text(n), text)
            self.assertEqual(text_to_num(text), n)

    def test_thousands(self):
        cases = {
            1000: "tusri",
            1001: "tusr la a ye",
            1100: "tusr la koabga",
            1999: "tusr la kobs-wɛ la pis-wɛ la a wɛ",
            2000: "tus a yi",
            2001: "tus a yi la a ye",
            10000: "tus piiga",
            145500: "tus koabg la pis-naase la a nu la kobs-nu"
        }
        for n, text in cases.items():
            self.assertEqual(convert_to_text(n), text)
            self.assertEqual(text_to_num(text), n)

    def test_large_numbers(self):
        cases = {
            1000000: "milyõ a ye",
            2000000: "milyõ a yiibu",
            1000000000: "milyar a ye",
            2000000000: "milyar a yiibu"
        }
        for n, text in cases.items():
            self.assertEqual(convert_to_text(n), text)
            self.assertEqual(text_to_num(text), n)

    def test_money(self):
        cases = {
            0: "zaalem",
            1: "tãmb a ye",
            3: "tãmb a tãabo",
            5: "ye",
            7: "ye la tãmb a yiibu",
            24: "naase la tãmb a naase",
            100: "pisi",
            102: "pisi la tãmb a yiibu"
        }
        for n, text in cases.items():
            self.assertEqual(convert_to_text(n, is_money=True), text)
            self.assertEqual(text_to_num(text, is_money=True), n)

if __name__ == '__main__':
    unittest.main()
