#!/bin/env python3

from random import choice as _choice
from random import randint as _randint
import string

def pwgen(lowerCount=4, upperCount=4, digitCount=4, symbolCount=4):
	chars = [] # list to store chosen characters
	password = '' # string to store generated password
	alphaL = string.ascii_lowercase # lowercase alphabet
	alphaU = string.ascii_uppercase # uppercase alphabet
	digits = string.digits # digits 0-9
	symbols = string.punctuation # punctuation (%,.;:-_ etc.)
	# append given count of random characters from different character groups to chars list
	for i in range(lowerCount):
		charL = _choice(alphaL)
		chars.append(charL)
	for i in range(upperCount):
		charU = _choice(alphaU)
		chars.append(charU)
	for i in range(digitCount):
		digit = _choice(digits)
		chars.append(digit)
	for i in range(symbolCount):
		symbol = _choice(symbols)
		chars.append(symbol)
	# loop through the chosen characters and rearrange them
	i = lowerCount+upperCount+digitCount+symbolCount-1 # loop index
	while i >= 0: 
		index = _randint(0, i) # random number between 0 and characters left
		password += chars[index] # append password string by character of the chars list randomly chosen by index
		del chars[index] # delete character to narrow down duplication
		i -= 1 # update loop index 
	return password # return final password string

if __name__ == '__main__':
	print(pwgen())
