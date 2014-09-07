import sqlite3
import io
import os
import generated
import hashlib



def checkLogin(username, password):
	try:	
		dbConnection = sqlite3.connect("./marksystem/db/mark.db")
		dbConnection.row_factory = sqlite3.Row
		hashPassword = hashlib.sha256(password).hexdigest()
		cursor = dbConnection.cursor()
		cursor.execute('select name from user_info where hash = ?', (hashPassword, ))
		row = cursor.fetchone()
		dbConnection.commit()
		cursor.close()
		dbConnection.close()
		
		if(row['name'] == username):
			#print "ok dragon"
			return True
	except:
			pass
	return False

def checkSession(session):
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
	dbConnection.row_factory = sqlite3.Row
	if 'loginsession' in session:
		try:
			rawSession = session['loginsession']
			paramList = rawSession.split('.', 1)
			print "a"
			print rawSession
			if len(paramList) != 2:
				dbConnection.close()
				return False
			cursor = dbConnection.cursor()
			print "b"
        	        cursor.execute('select session from user_info where name = ?', (paramList[0],))
			row = cursor.fetchone()
			dbConnection.commit()
			cursor.close()
			print row['session']
			if row['session'] == paramList[1]:
				dbConnection.close()
				return True
		except:
			pass
	dbConnection.close()
	return False

def createSessionForUser(username, session):
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
	sessionRandom = os.urandom(16).encode('hex')
	try:
		cursor = dbConnection.cursor()
		cursor.execute('update user_info set session=? where name == ?', (sessionRandom, username))
		dbConnection.commit()
		cursor.close()
	except:
		return False
	finally: 
		dbConnection.close()
	session['loginsession'] = username+"."+sessionRandom
	return True


