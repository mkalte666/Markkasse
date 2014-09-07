import io
import time
import logging
import logging.handlers

GlobalLogger = {}

class Logger:
	def __init__(self, outfile, isDebug=False):
		self.isDebug = isDebug
		self.handler = logging.handlers.RotatingFileHandler(outfile, maxBytes=10000, backupCount=10)
		if isDebug == True:
			self.handler.setLevel(logging.DEBUG)
		else:
			self.handler.setLevel(logging.INFO)
		self.formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')
		self.logger = logging.getLogger(outfile)
		self.logger.setLevel(logging.DEBUG)
		self.handler.setFormatter(self.formatter)
		self.logger.addHandler(self.handler)
	def Close(self):
		pass

	def Handler(self):
		return self.handler
	
	def log(self):
		return self.logger
