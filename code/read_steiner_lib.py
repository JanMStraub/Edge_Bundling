# -*- coding: utf-8 -*-

"""
This file reads the Steiner lib data
@author: Jan Straub
"""

from steinlib.instance import SteinlibInstance
from steinlib.parser import SteinlibParser

class MySteinlibInstance(SteinlibInstance):
    """
    This is my first steinlib parser!
    """

    def comment(self, raw_args, list_args):
        print ("Comment section found")

    def comment__end(self, raw_args, list_args):
        print ("Comment section end")

    def coordinates(self, raw_args, list_args):
        print ("Coordinates section found")

    def eof(self, raw_args, list_args):
        print ("End of file found")

    def graph(self, raw_args, list_args):
        print ("Graph section found")

    def header(self, raw_args, list_args):
        print ("Header found")

    def terminals(self, raw_args, list_args):
        print ("Terminals section found")

if __name__ == "__main__":
    PATH = "/Users/jan/Documents/code/gitlab_BA/2023-jan-straub/data/I080/"
    STP_FILE_NAME = "i080-001"
    STP_FILE_PATH = PATH + STP_FILE_NAME + ".stp"
    
    my_class = MySteinlibInstance()
    with open(STP_FILE_PATH) as my_file:
        my_parser = SteinlibParser(my_file, my_class)
        my_parser.parse()
        print(my_parser._state)