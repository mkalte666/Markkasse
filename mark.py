#!/usr/bin/env python
# -*- coding: utf-8 -*-
import marksystem.db
import marksystem.util
from marksystem.logger import Logger
from marksystem.web import StartWeb

marksystem.logger.GlobalLogger = Logger("./log/mark.log", True)

try:
	marksystem.logger.GlobalLogger.log().info("Starting System etc.!")
	StartWeb(True)
finally:
	pass
#	marksystem.logger.GlobalLogger.Close()


