#!/usr/bin/env python

import io
import sys
import os
import sqlite3
import hashlib
import binascii

print "Setting Up Mark System"
print "This will, delete all data but the ones in the backup-folder !"
print "If you are shure you want to continue, type \" YES \". yep, in capslock!\n"
ShouldInstall = unicode(raw_input("Shure? "))
if ShouldInstall != unicode("YES"):
	print "Quitting Installation...\n"
	sys.exit()

print "Cleaning Up..."
os.system("rm -rf ./marksystem")
os.system("rm -rf ./log")
print "Done!"

print "Beginning Installation. Creating folders...\n"
os.system("mkdir ./backup")
os.system("mkdir ./marksystem")
os.system("mkdir ./marksystem/db")
os.system("mkdir ./marksystem/templates")
os.system("mkdir ./marksystem/static/")
os.system("mkdir ./log/")
os.system("mkdir ./marksystem/static/css")
os.system("mkdir ./marksystem/static/uploads")
os.system("mkdir ./marksystem/static/img")
os.system("mkdir ./marksystem/static/font/")
os.system("mkdir ./marksystem/static/js/")
print "Done!\n"

print "Copying Files..."
os.system("cp ./installation/*.py ./marksystem/")
os.system("touch ./log/mark.log")
os.system("cp ./installation/templates/* ./marksystem/templates")
os.system("cp ./installation/media/img/* ./marksystem/static/img")
os.system("cp ./installation/media/css/* ./marksystem/static/css")
os.system("cp ./installation/media/font/* ./marksystem/static/font")
os.system("cp ./installation/js/* ./marksystem/static/js/")
#copys of files from the installation-files folder here
print "Done!\n"

print "Creating Database..."
#database creation
connection = sqlite3.connect("./marksystem/db/mark.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE user_info(id INTEGER PRIMARY KEY, name TEXT, hash TEXT, session TEXT, userlevel INTEGER)''')
cursor.execute('''CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT, price REAL, amoutInStock INTEGER, image TEXT, isSubproduct BOOLEAN, parent INTEGER, isBuyable INTEGER)''')
cursor.execute('''CREATE TABLE transactions(id INTEGER PRIMARY KEY, description TEXT, inflow REAL, outflow REAL, userID INTEGER, productIDs TEXT, isGenerated BOOLEAN, date TEXT)''')
cursor.execute('''CREATE TABLE pending_orders(id INTEGER PRIMARY KEY, transactionId INTEGER)''')
cursor.execute('''CREATE TABLE debtTransactions(id INTEGER PRIMARY KEY, transactionId INTEGER, isPaied BOOLEAN, userId INTEGER)''')
print "Setting basic information in Database"
cursor.execute('''insert into products(name, price, isSubproduct, parent, isBuyable) values ('remove me!', 3.0, 0, -1, 1)''')
print "Set Root User:"
username = unicode(raw_input("Username: "))
password = "not the"
passwordConfirm = "same"
while password != passwordConfirm:
	password = hashlib.sha256(unicode(raw_input("Password: "))).hexdigest()
	passwordConfirm = hashlib.sha256(unicode(raw_input("Confirm: "))).hexdigest()
print "Change Password after logging in for the first time!!!"
cursor.execute('''INSERT INTO user_info (name, hash, session, userlevel) VALUES (?, ?, 'invalid', 9001)''', (username, password, ))
connection.commit()
cursor.close()
connection.close()
print "Done!\n"

print "Genarating files"
sessionKey = os.urandom(24).encode('hex')
outfile = open('./marksystem/generated.py', 'w')
outfile.write("secretKey = '"+unicode(sessionKey)+"'\n")
maxdays = 6
maxdays = input("Input maximal time user can owe the system Money:")
outfile.write("maxdays = "+unicode(maxdays)+"\n")
outfile.close()
print "Done!"


print "Installation Compleated!"

