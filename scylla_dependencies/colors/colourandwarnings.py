#!/usr/bin/python3

class colours:  # for printing colored text in terminal
    def __init__(self):
        self.red = "\033[1;31m"
        self.yellow = "\033[93m"
        self.end = "\033[0m"


colourful = colours()


class errors:  # class with common errors
    def __init__(self):
        self.exit = colourful.red + '[-]' + colourful.end + ' Should scylla exit?'
        self.proxy = colourful.red + '[-]' + colourful.end + ' Error starting proxy'


class alerts:
    def __init__(self):
        self.unknown = colourful.yellow + '[-]' + colourful.end + ' Unknown error'
