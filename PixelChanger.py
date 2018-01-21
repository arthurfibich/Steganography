import cv2
import numpy as np
import string
from random import *

from SecComBot import SecComBot


class PixelChanger:
    def __init__(self):
        self.img = None
        self.window_name = None
        self.src = None

    def open_img(self, src="icon2.png"):
        self.src = src
        img = cv2.imread(src)
        self.img = img
        return img

    def new_window(self, name):
        cv2.namedWindow(name)
        self.window_name = name

    def show_img(self):
        cv2.imshow(self.window_name, self.img)

    def modify_pixel(self, w, h, col, value):
        px = self.img[w, h]
        # print(px)
        if col != 'x':  #  and px[col] <= 253:
            px[col] += value
        else:
            for val in range(len(px)):

                # if px[val] <= 253:
                    px[val] += value

        self.img[w, h] = px
        # print(self.img[w, h])

    def wait_key(self, delay=None):
        if delay:
            cv2.waitKey(delay)
        else:
            cv2.waitKey()


class ImageSaver:
    def __init__(self, file_name):
        self.file_name = file_name

    def save(self, img):
        cv2.imwrite(self.file_name, img)

    def read(self):
        return cv2.imread(self.file_name)


class Position:
    def __init__(self, pxc: PixelChanger):
        self.x = 0
        self.y = 0
        self.col = 0
        self.pxc = pxc

    def change(self, new_x, new_y, new_col):
        self.x = new_x
        self.y = new_y
        self.col = new_col

    def next(self):
        if self.col < self.pxc.img.shape[2] - 1:
            self.col += 1
        elif self.x < self.pxc.img.shape[1] - 1:
            self.x += 1
            self.col = 0
        elif self.y < self.pxc.img.shape[0] - 1:
            self.x = 0
            self.col = 0
            self.y += 1
        else:
            print(self.x)
            print(self.y)
            print(self.col)
            return None

        return self.x, self.y, self.col

class Differenciator:
    def __init__(self, pxc:PixelChanger, src):
        self.pxc = pxc
        self.enc_img = cv2.imread(src)
        self.clr_img = cv2.imread(self.pxc.src)
        self.dif_img = None

    def make_dif(self, show=None):
        self.dif_img = (self.enc_img - self.clr_img) * 1
        if show:
            cv2.imshow(show, self.dif_img * 100)
            self.pxc.wait_key()
        return self.dif_img

    def append(self):
        binarray = ""
        for value in self.dif_img.flat:
            if value > 0:
                binarray += str(value)
        return binarray

class Main:
    def __init__(self, pxc:PixelChanger, bot: SecComBot, pos: Position, window_name, image_src, image_save):
        self.pxc = pxc
        self.bot = bot
        self.pos = pos
        self.window_name = window_name
        self.image_src = image_src
        self.img_save = image_save
        self.image = self.pxc.open_img(self.image_src)

    def encrypt(self, new_text):
        self.pxc.new_window(self.window_name)
        text = self.bot.encode_text(new_text)
        index = 0
        while self.pos.next() and index < len(text):
            self.pxc.modify_pixel(self.pos.y, self.pos.x, self.pos.col, int(text[index]))
            index += 1
        self.pxc.show_img()
        self.pxc.wait_key()
        self.img_save.save(self.image)

    def decrypt(self, src):
        dif = Differenciator(self.pxc, src)
        dif.make_dif(self.window_name)
        text = dif.append()
        print(text)
        decoded_text = self.bot.decode_to_text(text)
        print("Your Text was: " + decoded_text)

        return decoded_text


if __name__ == "__main__":
    count_true = 0
    while True:
        try:
            print("start")
            pxc = PixelChanger()
            bot = SecComBot()
            pos = Position(pxc)
            img_save = ImageSaver("Test.png")
            main = Main(pxc, bot, pos, "Test", "icon2.png", img_save)
            start_text = bot.get_string()
            start_text = bot.get_string()
            img_save = ImageSaver("Test.png")
            main.encrypt(start_text)
            end_text = main.decrypt("Test.png")
            print(start_text == end_text)
            if start_text == end_text:
                count_true += 0
            else:
                count_true -= 1
        except:
            print("failed")
            count_true -= 1
        print(count_true)
