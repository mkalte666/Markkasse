import sqlite3
import io
import os
import generated
import hashlib
import time
import datetime



#sqlite3 uses integers for booleans, so a converter from int to bool would be good for output-stuff
def itob(i):
	if i == 1:
		return True
	return False


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

#priduct and sell managemenrt API

#adds a product and returns true if successfull
def addProduct(name, price, hasParent, parent):
	dbConnectoin = sqlite3.connect("./marksystem/db/mark.db")
	try:	
		cursor = dbConnection.cursor()
		cursor.execute('''insert into products(name, price, amoutInStock, image, IsSubproduct, parent) values (?, ?, -1, 'invalid', ?, ?) ''', (name, price, hasParent, parent))
		dbConnection.commit()
		cursor.close()
	except:
		return False
	finally:
		dbConnection.close()
	return True	

#changes product with id pid. to delete, set isDeleted to true
def changeProduct(pId, name, price, isDeleted=False):
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
	try:
		cursor = dbConnection.cursor()
		if isDeleted==True:
			cursor.execute('''delete from products where id = ? ''', (pId, ))
		else:
			cursor.execute('''update products set name=?, price=? where id = ?''', (name, price, pId))
	except:
		return False;
	finally:
		dbConnection.close()
	
	return True

def generatedJavascript():
	outstring = ""
	outstring += "\n\n//Generated Javascript begin\n"
	#temp containers for writing the product- and userlist
	#product 
	pids = "var pIds = ["
	names = "var names = ["
	prices = "var prices = ["
	pHasParent = "var pHasParent = ["
	parents = "var parents = ["
	pShouldOutput = "var pShouldOutput = ["
	#users
	RawUsers = "var RawUsers = ["
	uIds = "var uIds = ["
	uAbleToBuy = "var uAbleToBuy = ["
	debts = "var debts = ["
	#try:
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
	dbConnection.row_factory = sqlite3.Row
	cursor = dbConnection.cursor()
	#fill the product-specific arrays
	for row in cursor.execute('''select * from products'''):
		pids +=str(row['id'])+","
		names += "\""+str(row['name'])+"\","
		prices +=str(row['price'])+","
		pHasParent +=str(itob(row['isSubproduct'])).lower()+","
		pShouldOutput += str(itob(row['isBuyable'])).lower()+","
		parents += str(row['parent'])+","
	#the user-stuff
	for row in cursor.execute('''select * from user_info'''):
		uIds +=str(row['id'])+","
		RawUsers += "\""+str(row['name'])+"\","
		debts_current = 0.0
		canBuy = True;
		#meashure ows and calculate if user can buy stuff
		for row2 in cursor.execute('''select transactionId from debtTransactions where userID=? and isPayed=0 ''', (row['id'],)):
			for row3 in cursor.execute('''select outflow, inflow from transactions where id=?''', (row2['transactionId'], )):
				debts_current += row3['inflow'];
				maxDate = datetime.datetime.strptime(row3['data'])+datetime.timedelta(days=generated.maxdays)
				today = datetime.date.today
				if today < maxData:
					canBuy = False
		debts+=str(debts_current)+","
		uAbleToBuy += str(canBuy).lower()+","
	
	#all orders that are currently pending will be written, too
		
	endlist = "];\n"
	pids+= endlist
	names+=endlist
	prices+=endlist
	pHasParent+=endlist
	parents+=endlist
	pShouldOutput+=endlist
	RawUsers+=endlist
	uIds +=endlist;
	uAbleToBuy+=endlist;
	debts+=endlist;
	outstring += pids+names+prices+pHasParent+parents+pShouldOutput+RawUsers+uIds+uAbleToBuy+debts

	#except:
#		pass
#	finally:
	dbConnection.close()
	outstring += "//Generated Javascript end\n\n"
	#python uses 'True', javascript uses 'true'. lets do a quick replace
	return outstring





