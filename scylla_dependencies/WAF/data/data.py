#!/usr/bin/python3

import sys, os
import math
import string

class DataEntry:

    charArray = list(string.ascii_lowercase)

    def percentMayus(self, string):  # percent of mayus in string
        total_lenght = len(string)
        n = 0
        for i in string:
            i = i.upper()
            if i in self.charArray:
                n += 1
        mayus = (100 * n) / total_lenght

        return mayus

    def percentMinus(self, string):  # percent of Minus in string
        total_lenght = len(string)
        n = 0
        for i in string:
            if i in self.charArray:
                n += 1
        minus = (100 * n) / total_lenght

        return minus

    def percentNumbers(self, string):  # percent of numbers in string
        total_lenght = len(string)
        n = 0
        for i in string:
            numStr = ''
            for n in range(1,11):
                numStr += str(n)
            if i in numStr:
                n += 1
        num = (100 * n) / total_lenght

        return num

    def percentSpecial(self, string):  # percent of special characters
        total_lenght = len(string)
        n = 0
        charStr = '' 
        for x in self.charArray:
            charStr += x.upper()
        for i in string:
            numStr = ''
            for n in range(1,11):
                numStr += str(n)
            if not i in charStr and not i in self.charArray and not i in numStr:
                n += 1
        special = (100 * n) / total_lenght

        return special

    def getEntropy(self, string):  # get entropy of string
        strSize = len(string)
        freqList = [0] * strSize
        for b in range(256):
            ctr = 0.0
            for byte in string:
                if ord(byte) == b:
                    ctr += 1
            freqList.append(float(ctr) / strSize)
        ent = 0.0
        for freq in freqList:
            if freq > 0:
                ent = ent + (freq * math.log(freq, 2))
        ent = -ent
        return ent
        
    def all(self, payload):
    
        mayus = self.percentMayus(payload)
        minus = self.percentMinus(payload)
        numbers = self.percentNumbers(payload)
        special = self.percentSpecial(payload)
        entropy = self.getEntropy(payload)
        
        point = [mayus, minus, numbers, special, entropy]
        
        return point
