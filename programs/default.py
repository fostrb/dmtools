from programs.program import DMProgram
import sys
import random
import os
import time


__all__ = ['Clear', 'WeirdPrinter']


hacktable = [
    "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", "~",
    ".", "/", ":", ";", "<", "=", ">", "?", "[", "\\", "]", "_", "{", "}",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ", "྾"
]


class Clear(DMProgram):
    def __init__(self):
        super(Clear, self).__init__()
        self.name = 'clear'
        self.aliases = ['cls']

    def run(self, line):
        os.system('clear')


class WeirdPrinter(DMProgram):
    def __init__(self):
        super(WeirdPrinter, self).__init__()
        self.name = 'wp'
        self.aliases = []

    def run(self, line):
        self.multi_eval(line)

    def single_eval(self, line):
        solved = ''
        for linechar in line:
            while True:
                for each in range(len(solved) + 1):
                    print('\b', end='', flush=True)
                time.sleep(.007)
                solvechar = chr(random.randint(32, 177))
                print(solved + solvechar, end='', flush=True)
                if solvechar == linechar:
                    solved += solvechar
                    break
        print()

    def multi_eval(self, line):
        numchars = len(line)
        newsolved = ['_'] * numchars

        for pos in range(numchars):
            print("྾", end='', flush=True)
        time.sleep(1)

        while True:
            time.sleep(.01)
            #bcksp = '\b' * numchars
            print('\b' * numchars, end='', flush=True)
            #for pos in range(numchars):
            #    print('\b', end='', flush=True)
            for pos in range(numchars):
                if newsolved[pos] != line[pos]:
                    thischar = random.choice(hacktable)
                    # print(''.join(newsolved), end='', flush=True)
                    print(thischar, end='', flush=True)
                    if thischar == line[pos]:
                        newsolved[pos] = thischar
                else:
                    # print('here')
                    print(newsolved[pos], end='', flush=True)

            if ''.join(newsolved) == line:
                print()
                break
        return ''.join(newsolved)
