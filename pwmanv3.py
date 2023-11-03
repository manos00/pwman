#!/bin/env python3

import sqlite3
from cryptography.fernet import Fernet
from os import getenv
from os import path
from os import mkdir
from time import sleep
import subprocess
from pwgen import pwgen
# import hashlib

# def detectDrive():
# 	return True
# 	while True:
# 		try:
# 			mountcheck = subprocess.run(('blkid | grep 0079dadd-a0a8-4441-9bc6-ed0627ce39c6'), shell=True, check=True)
# 			return True
# 		except subprocess.CalledProcessError:
# 			print('Please insert and mount USB drive.')
# 			for i in range(10):
# 				print(f'Trying again in {10-i} seconds...')
# 				sleep(1)
	


def encrypt(file, key):
	if path.exists(key):
		with open(key, 'rb') as passwdkey:
			keyraw = passwdkey.read()
	else:
		keyraw = str.encode(key)
	key = Fernet(keyraw)
	with open(file, 'rb') as passfile:
		dec = passfile.read()	
	enc = key.encrypt(dec)
	with open(file, 'wb') as passfile:
		passfile.write(enc)


def decrypt(file, key):
	if path.exists(key):
		with open(key, 'rb') as passwdkey:
			keyraw = passwdkey.read()
	else:
		keyraw = str.encode(key)
	key = Fernet(keyraw)
	with open(file, 'rb') as passfile:
		enc = passfile.read()
	dec = key.decrypt(enc)
	with open(file, 'wb') as passfile:
		passfile.write(dec)


def setup():
	if not path.exists(keypath): # detectDrive() and 
		if not path.exists(confdir):
			mkdir(confdir)
		key = Fernet.generate_key()
		with open(keypath, 'wb') as keyfile:
			keyfile.write(key)
		# while True:
		# 	password = input('Enter a secure master password: ')
		# 	pcheck = input('Please repeat your password: ')
		# 	if password == pcheck:
		# 		break
		# 	else:
		# 		print('Passwords do not match! Please repeat the process.')
		# 		sleep(2)
		# encrypt(keypath, password)
		subprocess.run(['chmod', '-wx', keypath])

	if not path.exists(f):
		conn = sqlite3.connect(f)
		c = conn.cursor()
		c.execute("""CREATE TABLE accountdata (
			service text,
			username text,
			email text,
			password text,
			link text
		)""")
		conn.commit()
		# decrypt(keypath, password)
		encrypt(f, keypath)



def add(service):
	while True:
		if service == True:
			service = input('Service: ')
		decrypt(f, keypath)
		conn = sqlite3.connect(f)
		c = conn.cursor()
		c.execute("SELECT service FROM accountdata WHERE service LIKE :service",{'service': service})
		options = c.fetchone()
		encrypt(f, keypath)
		if options != None:
			print('Service with the same name already exists!')
			service = None
		else:
			break
	username = input('Username: ')
	if username.strip() == '':
		username = None
	email = input('Email: ')
	if email.strip() == '':
		email = None
	password = input('Password: ')
	if password == 'random':
		password = pwgen()
		pccopy(password)
		print(f'Your password is {password}')
	link = input('Link: ')
	if link.strip() == '':
		link = None
	decrypt(f, keypath)
	conn = sqlite3.connect(f)
	c = conn.cursor()
	c.execute("INSERT INTO accountdata VALUES (?, ?, ?, ?, ?)", (service, username, email, password, link))
	conn.commit()
	encrypt(f, keypath)


def read(service):
	if service == True:
		service = input('')
	decrypt(f, keypath)
	conn = sqlite3.connect(f)
	c = conn.cursor()
	c.execute("SELECT * FROM accountdata WHERE service LIKE ?", (f'%{service}%',))
	options = c.fetchall()
	encrypt(f, keypath)
	i = 0
	if len(options) > 1:
		for i, option in enumerate(options):
			print(f'{i}: {option[0]}')
		while True:
			i = input('Which of the options above is the account you are looking for? ')
			try:
				i = int(i)
				break
			except ValueError:
				# for j, option in enumerate(options):
				# 	if option[0] == i:
				# 		i = j
				# 		break
				print('Input unvalid')
	elif len(options) == 0:
		return service
	return options[i]


def mod(service):
	if service == True:
		service = read(service)[0]
	password = input()
	decrypt(f, keypath)
	conn = sqlite3.connect(f)
	c = conn.cursor()
	c.execute("UPDATE accountdata SET password = :password WHERE service = :service", {'password': password, 'service':service})
	conn.commit()
	encrypt(f, keypath)


def delete(service):
	if service == True:
		service = read(service)[0]
	confirm = input(f'Are you sure you want to delete your saved {service} account information?')
	if confirm.lower() not in ['y', 'yes', '']:
		print('cancelling...')
		return
	decrypt(f, keypath)
	conn = sqlite3.connect(f)
	c = conn.cursor()
	c.execute("DELETE from accountdata WHERE service = ?", (service,))
	conn.commit()
	encrypt(f, keypath)

def main():
	parser = argparse.ArgumentParser('Store and read passwords from a locally stored, encrypted database.')
	actionG = parser.add_mutually_exclusive_group(required=True)
	actionG.add_argument('-r', '--read', nargs='?', const=True, help='Copy and/or print out a saved password.')
	actionG.add_argument('-a', '--add', nargs='?', const=True, help='Save a new account/password. When asked for a password, enter "random" to generate a secure password.')
	actionG.add_argument('-d', '--delete', nargs='?', const=True, help='Delete a saved password.')
	parser.add_argument('-m', '--mail', action='store_true', help='Copy not only the password, but also the associated email address to the clipboard.', default=False)
	parser.add_argument('-q', '--quiet', action='store_true', help='Supress output (-> password only gets saved to clipboard).', default=False)
	args = parser.parse_args()
	
	if args.read:
		accexists = False
		acc = read(args.read)
		while not accexists:
			if isinstance(acc, str):
				print(f'No login data for {acc} saved.\nPlease enter another service.')
				acc = read(True)
			else:
				accexists = True
		if not args.quiet:
			print(acc)
		if args.mail:
			pccopy(acc[2])
			sleep(3)	
		pccopy(acc[3])
	elif args.add:
		add(args.add)
	elif args.delete:
		delete(args.delete)
	elif args.mod:
		mod(args.mod)


if __name__ == '__main__':
	import argparse
	from pyperclip import copy as pccopy
	confdir = path.join(getenv('HOME'), '.config', 'pwmanv3')
	f = path.join(confdir, 'pass.db')
	keypath = path.join(confdir, 'pass.key')
	#encrypt(f, keypath)
	#exit()
	setup()
	main()
	# decrypt(f, keypath)
