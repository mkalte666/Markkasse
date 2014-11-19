import io
import sys
import os
import logger
import generated
import util
from flask import Flask, render_template, session, redirect, url_for, escape, request
app = Flask(__name__)

Mediatypes = [ 'png', 'jpeg', 'jpg', 'gif',]

#visitors of the system
@app.route('/')
def home():
	return render_template('homepage.html')

#logout 
@app.route('/system/logout.html')
def systemLogout():
	if 'loginsession' in session:
		session.pop('loginsession', None)
	return redirect(url_for('home'))

#login
@app.route('/system/login.html', methods=['GET', 'POST'])
def systemAccess():
	if request.method == 'POST':
		if 'username' in request.form and 'password' in request.form:
			if util.checkLogin(request.form['username'], request.form['password']) == True:
				util.createSessionForUser(request.form['username'], session)
				return redirect(url_for('systemHome'))
			else:
				app.logger.info('failed login atempt')
				return  render_template('login.html', failed=True)
	
	return render_template('login.html', failed=False)

#systemHome
@app.route('/system/home.html')
def systemHome():
	#securety check
	if util.checkSession(session) == False:
		return redirect(url_for('systemAccess'))
	return render_template('sysHome.html', generated_javascript = util.generatedJavascript())
	
#selling page
@app.route('/system/selling.html')
def systemSelling():
	#securety check
	if util.checkSession(session) == False:
		return redirect(url_for('systemAccess'))
	return render_template('selling.html', generated_javascript = util.generatedJavascript())

@app.route('/system/orderlist.html')
def orderlist():
        #sec checkSession
        if util.checkSession(session) == False:
                return redirect(url_for('systemAccess'))
        return render_template('orderlist.html', generated_javascript = util.generatedJavascript())

#start if the web-application
def StartWeb(shouldDebug=False):
	#util.setupDb()
	app.logger.addHandler(logger.GlobalLogger.Handler())
	app.debug=shouldDebug
	app.secret_key = generated.secretKey
	app.run(host='0.0.0.0')


#api commands
@app.route('/system/api/placeOrder.html', methods=['GET', 'POST'])
def apiPlaceOrder():
	if util.checkSession(session) == True:
		#we give the get infos to to util function. no pain here :D
		util.placeOrder(request.args.get)
	return redirect(url_for('systemHome'))

@app.route('/system/api/finishOrder.html', methods=['GET', 'POST'])
def apiFinishOrder():
        if util.checkSession(session) == True:
                util.removePending(request.args.get)
        return redirect(url_for('systemHome'))

@app.route('/system/api/addProduct.html', methods=['GET', 'POST'])
def apiAddProduct():
        if util.checkSession(session) == True:
                util.addProduct(request.args.get)
        return redirect(url_for('systemHome'))

@app.route('/system/api/changeProduct.html', methods=['GET', 'POST'])
def apiChangeProduct():
        if util.checkSession(session) == True:
                util.changeProduct(request.args.get)
        return redirect(url_for('systemHome'))
