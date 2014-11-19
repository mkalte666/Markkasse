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
def addProduct(getArgs):
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
        dbConnection.row_factory = sqlite3.Row
	try:	
                name = getArgs("name")
                price = float(getArgs("price"))
                hasParent = False
                if getArgs("hasParent")=="true":
                    hasParent = True
                buyable = False
                if getArgs("isBuyable")=="true":
                    buyable = True;
                parent = int(getArgs("parent"))
		cursor = dbConnection.cursor()
		cursor.execute('''insert into products(name, price, amoutInStock, image, IsSubproduct, parent, isBuyable) values (?, ?, -1, 'invalid', ?, ?, ?) ''', (name, price, hasParent, parent, buyable))
		dbConnection.commit()
		cursor.close()
	except:
		return False
	finally:
		dbConnection.close()
	return True	

#changes product with id pid. to delete, set isDeleted to true
def changeProduct(getArgs):
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
        dbConnection.row_factory = sqlite3.Row
	try:
                pId = int(getArgs("pId"))
                name = getArgs("name")
                price = float(getArgs("price"))
		cursor = dbConnection.cursor()
		if getArgs("isDeleted")=="true":
			cursor.execute('''delete from products where id = ? ''', (pId, ))
		else:
			cursor.execute('''update products set name=?, price=? where id = ?''', (name, price, pId))
	        dbConnection.commit()
                cursor.close()
        except:
		return False;
	finally:
		dbConnection.close()
	
	return True

#this ~thing~ generates the javascript that the fronend uses to make the users happy...
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
        #pending orders
        pendingOrderIds = "var pendingOrderIds = ["
        pendingOrderUIds = "var pendingOrderUIds = ["
        pendingOrderProducts = "var pendingOrderProducts = ["
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
	
        #the user-stuffi
	cursor.execute('''select * from user_info''')
	rows = cursor.fetchall() 
	for row in rows:
		uIds +=str(row['id'])+","
		RawUsers += "\""+str(row['name'])+"\","
		debts_current = 0.0
		canBuy = True;
		#meashure ows and calculate if user can buy stuff
		cursor.execute('''select transactionId from debtTransactions where userID=? and isPaied=0 ''', (row['id'],))
		rows2 = cursor.fetchall()
		for row2 in rows2:
			cursor.execute('''select outflow, inflow, date from transactions where id=?''', (row2['transactionId'], ))
			rows3 = cursor.fetchall()
			for row3 in rows3:
				debts_current += row3['inflow'];
				maxDate = datetime.datetime.strptime(row3['date'], '%y/%m/%d/%H/%M/%S')+datetime.timedelta(days=generated.maxdays)
				today = datetime.date.today
				if datetime.datetime.now() < maxDate:
					canBuy = False
		debts+=str(debts_current)+","
		uAbleToBuy += str(canBuy).lower()+","
	
	#all orders that are currently pending will be written, too
	cursor.execute('''select * from pending_orders''')
        rows = cursor.fetchall()
        for row in rows:
            pendingOrderIds += str(row['transactionId'])+","
            cursor.execute('''select * from transactions where id = ? LIMIT 1''', (row['transactionId'],))
            rows2 = cursor.fetchall()
            for row2 in rows2:
                pendingOrderUIds+= str(row2['userID'])+","
                #to parse the pending products we have to split the product ids in the transaction.
                #these are seperated by '+'s
                pendingOrderProductsRaw = row2['productIds'].split('+')
                pendingOrderProducts+="["
                for singleProductId in pendingOrderProductsRaw:
                    if singleProductId == "" or singleProductId == " ":
                        continue
                    pendingOrderProducts+=singleProductId+","
                pendingOrderProducts+="],"
        #note: we dont have to put actual product names etc. in the pending orders - the javascript can parse them by asking the arrays generated above.

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
        pendingOrderIds+=endlist;
        pendingOrderUIds+=endlist;
        pendingOrderProducts+=endlist;
	outstring += pids+names+prices+pHasParent+parents+pShouldOutput+RawUsers+uIds+uAbleToBuy+debts+pendingOrderIds+pendingOrderUIds+pendingOrderProducts

	#except:
#		pass
#	finally:
	dbConnection.close()
	outstring += "//Generated Javascript end\n\n"
	#python uses 'True', javascript uses 'true'. lets do a quick replace
	return outstring


def addRawUser(name):
	dbConnection = sqlite3.connect("./marksystem/db/mark.db")
	dbConnection.row_factory = sqlite3.Row
	cursor = dbConnection.cursor()
	#test if the user already exists
	try:
		cursor.execute('''select * from user_info where name = ?''', (name,))
		rows = cursor.fetchall()
		if len(rows)!=0:
			#user already exits, go away
			dbConnection.close()
			return False
		#add the new user
		print "Adding new user: "+name
		cursor.execute('''insert into user_info (name, hash, session, userlevel) VALUES (?, 'none', 'none', 0)''', (name,))
		dbConnection.commit()
                uId = cursor.lastrowid
		cursor.close()
	
		return uId
	except:
		print "error while adding user - exeption"
		return False
	finally:
		dbConnection.close()	

def placeOrder(getArgs):
	#check if we should add a user
	uId = 0
        if(getArgs("newUser")=="true"):
		#add the new user and maybe return (if unsuccessfull)
		uId = addRawUser(getArgs("name"))
                if uId == False:
			return False
        else:
            try:
                uId = int(getArgs("uid"))
            except:
                return False
        
	#split my string into pices
        rawProducts = getArgs("products")
        if rawProducts[0]==' ':
            rawProducts = rawProducts[1:]
        rawSplits = rawProducts.split(' ')
        productIds = list()
        for rawId in rawSplits:
            productIds.append(int(rawId))
                
        #create the transaction
        dbConnection = sqlite3.connect("./marksystem/db/mark.db")
        dbConnection.row_factory = sqlite3.Row
        try:
            cursor = dbConnection.cursor()
            
            transactionInflow = 0
            #check if all products are valid and get thier price. if not, DON'T PLACE orders
            for pId in productIds:
                cursor.execute('''select price, id from products where id = ?''', (pId,))
                row = cursor.fetchone()
                transactionInflow+=row['price']
                        
            #the ids are split and then rejoined cause then noone can put sql-inject asshole stuff in it!
            productString = ""
            for pId in productIds:
                productString+=str(pId)+"+"
            
            
            currentDate = datetime.datetime.strftime(datetime.datetime.now(), "%y/%m/%d/%H/%M/%S")
            
            #the raw transactionId
            cursor.execute('''insert into transactions (description, inflow, outflow, userID, productIDs, isGenerated, date) values ('Order', ?, 0.0, ?, ?, 1, ?)''', (transactionInflow, uId, productString, currentDate))
            
            transactionId = cursor.lastrowid
            
            #pending orders
            cursor.execute(''' insert into pending_orders (transactionId) values (?)''', (transactionId, ))
            #if not paid, add to the debt_transactions
            if getArgs("wasPaied") == "false":
                cursor.execute('''insert into debtTransactions (transactionId, isPaied, userId) values (?, 0, ?)''', (transactionId, uId))
            
            dbConnection.commit()
        except:
            return False
        finally:
            dbConnection.close()
        
        #were done here :D
        return True	

def removePending(getArgs):
    dbConnection = sqlite3.connect("./marksystem/db/mark.db")
    dbConnection.row_factory = sqlite3.Row
    try:
        orderId = int(getArgs("orderId"))
        cursor = dbConnection.cursor()
        cursor.execute(''' delete from pending_orders where transactionId = ?''', (orderId, ))
        dbConnection.commit()
        cursor.close()
    except:
        return False
    finally:
        dbConnection.close()
    return True
