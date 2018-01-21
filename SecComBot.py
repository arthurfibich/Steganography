import cv2
import numpy as np
import string
from random import *


class SecComBot:

    def get_string(self):
        characters = string.ascii_letters + string.punctuation + string.digits
        return "".join(choice(characters) for x in range(6000))

    def encode_chararray(self, string):
        chararray = []
        for char in string:
            chararray.append(char)

        return chararray

    def encode_unicode(self, chararray):
        unicodes = []
        for char in chararray:
            unicodes.append(ord(char))

        return unicodes

    def encode_binary(self, unicode):
        encode_bin = lambda x: format(x, 'b')
        binaries = []
        for number in unicode:
            binaries.append(int(encode_bin(number)))

        return binaries

    def encode_adding_binary(self, binarray):
        abins = []
        for bin in binarray:
            abin = bin + 1111111111111111
            abins.append(abin)
        return abins

    def encode_encrypted_string(self, abinarray):
        string = ""
        for abin in abinarray:
            string += str(abin)
        return string

    def divide_encrypted_string(self, encrypted_string):
        array = []
        while len(encrypted_string) > 0:
            array.append(int(encrypted_string[:16]))
            encrypted_string = encrypted_string[16:]
        return array

    def decode_to_binary(self, abinarray):
        bins = []
        for abin in abinarray:
            bin = abin - 1111111111111111
            bins.append(bin)
        return bins

    def decode_to_unicode(self, binarray):
        decode_bin = lambda x: int(str(x), 2)
        unicodes = []
        for number in binarray:
            unicodes.append(int(decode_bin(number)))

        return unicodes

    def decode_to_string(self, unicodearray):
        string = ""
        for unicode in unicodearray:
            string += chr(unicode)

        return string

    def wait_key(self, delay=None):
        if delay:
            cv2.waitKey(delay)
        else:
            cv2.waitKey()

    def encode_text(self, text):
        print(text)
        chararray = self.encode_chararray(text)
        print(chararray)
        unicodearray = self.encode_unicode(chararray)
        print(unicodearray)
        binarray = self.encode_binary(unicodearray)
        print(binarray)
        abinarray = self.encode_adding_binary(binarray)
        print(abinarray)
        encrypted_text = self.encode_encrypted_string(abinarray)
        print(encrypted_text)
        return encrypted_text

    def decode_to_text(self, encrypted_code):
        decabinarray = self.divide_encrypted_string(encrypted_code)
        print(decabinarray)
        decbinarray = self.decode_to_binary(decabinarray)
        print(decbinarray)
        decunicodearray = self.decode_to_unicode(decbinarray)
        print(decunicodearray)
        dectext = self.decode_to_string(decunicodearray)
        print(dectext)
        return dectext

if __name__ == "__main__":
    bot = SecComBot()
    enc_text = bot.encode_text(input("Text to encrypt: "))
    print("your text was: " + bot.decode_to_text(enc_text))
