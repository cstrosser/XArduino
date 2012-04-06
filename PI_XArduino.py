"""
PI_XArduino

Copyright (c) 2012 by Chris Strosser
"""

from XPLMDefs import *
from XPLMProcessing import *
from XPLMDataAccess import *
from XPLMUtilities import *
from XPLMPlanes import *
from XPLMPlugin import *

import serial
import sys

import ConfigParser
from os import path

class PythonInterface:
	KEY_BUTTON1 = "button1"
	KEY_BUTTON2 = "button2"
	KEY_BUTTON3 = "button3"
	KEY_BUTTON4 = "button4"
	KEY_SWITCH1 = "switch1"
	KEY_SWITCH2 = "switch2"
	KEY_SWITCH3 = "switch3"
	KEY_SWITCH4 = "switch4"
	KEY_SWITCH5 = "switch5"
	KEY_SWITCH6 = "switch6"
	KEY_SWITCH7 = "switch7"
	KEY_SWITCH8 = "switch8"
	OFFSET_BUTTON1 = 1
	OFFSET_BUTTON2 = 2
	OFFSET_BUTTON3 = 3
	OFFSET_BUTTON4 = 4
	OFFSET_SWITCH1 = 5
	OFFSET_SWITCH2 = 6
	OFFSET_SWITCH3 = 7
	OFFSET_SWITCH4 = 0
	OFFSET_SWITCH5 = 8
	OFFSET_SWITCH6 = 9
	OFFSET_SWITCH7 = 10
	OFFSET_SWITCH8 = 11

	def XPluginStart(self):
		self.Name = "XArduino"
		self.Sig =  "ChrisStrosser.XPlane.XArduino"
		self.Desc = ""
		
		self.configFile = 'xarduino.ini'
		self.systemPath = XPLMGetSystemPath("")

		self.buttonToOffset = {
			self.KEY_BUTTON1 : self.OFFSET_BUTTON1,
			self.KEY_BUTTON2 : self.OFFSET_BUTTON2,
			self.KEY_BUTTON3 : self.OFFSET_BUTTON3,
			self.KEY_BUTTON4 : self.OFFSET_BUTTON4,
			self.KEY_SWITCH1 : self.OFFSET_SWITCH1,
			self.KEY_SWITCH2 : self.OFFSET_SWITCH2,
			self.KEY_SWITCH3 : self.OFFSET_SWITCH3,
			self.KEY_SWITCH4 : self.OFFSET_SWITCH4,
			self.KEY_SWITCH5 : self.OFFSET_SWITCH5,
			self.KEY_SWITCH6 : self.OFFSET_SWITCH6,
			self.KEY_SWITCH7 : self.OFFSET_SWITCH7,
			self.KEY_SWITCH8 : self.OFFSET_SWITCH8,
		}
		
		self.commands = {}
		self.datarefs = {}
		self.offsetToButton = {}
		self.lastState = {}
		for i in self.buttonToOffset:
			self.offsetToButton[self.buttonToOffset[i]] = i
			self.lastState[self.buttonToOffset[i]] = 0

		try:
			self.s = serial.Serial(10, 9600, timeout=0)

			self.run = True;
			self.buffer = ''
			
			self.interval = -1
			self.FlightLoopCB = self.FlightLoopCallback
			XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, self.interval, 0)
		except serial.SerialException:
			self.run = False;
			
		return self.Name, self.Sig, self.Desc
	
	def config(self):
		plane, planePath = XPLMGetNthAircraftModel(0)
		
		config = ConfigParser.RawConfigParser()
		if (not config.read(planePath.replace(plane, self.configFile))):
			config.read(self.systemPath + 'Resources/plugins/PythonScripts/' + self.configFile)
				     
		definitions = {}
		for section in config.sections():		    
		    definitions[section] = {}
		    
		    for item in config.items(section):
				definitions[section][item[0]] = item[1]

		for section in definitions:
			type = definitions[section].get('type')
			if (type == 'command'):
				continue

			if (definitions[section].get('mode') == 'loop'):
				if (type == 'int'):
					definitions[section]['min'] = int(definitions[section]['min'])
					definitions[section]['max'] = int(definitions[section]['max'])
					definitions[section]['increment'] = int(definitions[section]['increment'])
				elif (type == 'float'):
					definitions[section]['min'] = float(definitions[section]['min'])
					definitions[section]['max'] = float(definitions[section]['max'])
					definitions[section]['increment'] = float(definitions[section]['increment'])
			else:
				if (type == 'int'):
					definitions[section]['on'] = int(definitions[section]['on'])
					definitions[section]['off'] = int(definitions[section]['off'])
				elif (type == 'float'):
					definitions[section]['on'] = float(definitions[section]['on'])
					definitions[section]['off'] = float(definitions[section]['off'])
		
		self.definitions = definitions
		pass

	def getCommand(self, commandString):
		if (self.commands.get(commandString) == None):
			self.commands[commandString] = XPLMFindCommand(commandString)
		return self.commands.get(commandString)
		
	def getDataref(self, datarefString):
		if (self.datarefs.get(datarefString) == None):
			self.datarefs[datarefString] = XPLMFindDataRef(datarefString)
		return self.datarefs.get(datarefString)

	def XPluginStop(self):
		# Unregister the callback
		XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)
		if self.run:
			self.s.close();
		pass

	def XPluginEnable(self):
		self.config()
		return 1

	def XPluginDisable(self):
		pass

	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		if (inFromWho == XPLM_PLUGIN_XPLANE):
			if (inParam == XPLM_PLUGIN_XPLANE and inMessage == XPLM_MSG_PLANE_LOADED):
				self.config()
		pass

	def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		if (True != self.run):
			print "Arduino not running";
			return 0;
		
		try:
			line = self.s.readline()
			if len(line) < 22:
				return self.interval;
			
			values = line.split(",")
			if (values[0] != "H"):
				return self.interval;
			
			i = -1
			for value in values:
				i += 1
				if i == 0:
					# Header - do nothing
					continue

				if (value == ''):
					continue
					
				state = int(value)
				
				key = self.offsetToButton.get(i)
				if (key == None):
					continue
				
				definition = self.definitions.get(key)
				type = definition.get('type')
				if (type == 'command'):
					commandString = definition.get('command')
					if (commandString == None):
						continue
						
					command = self.getCommand(commandString)
					if (command == None):
						continue
						
					if state == 1:
						XPLMCommandOnce(command)
				else:
					datarefString = definition.get('dataref')
					if (datarefString == None):
						continue
					
					dataref = self.getDataref(datarefString)
					if (dataref == None):
						continue
					
					type = definition.get('type')
					if (definition.get('mode') == 'loop'):
						if state == 0:
							self.lastState[i] = 0
							continue
						if self.lastState[i] == 1:
							continue
						self.lastState[i] = 1

						min = definition.get('min')
						max = definition.get('max')
						increment = definition.get('increment')

						if (type == 'int'):
							value = XPLMGetDatai(dataref)
						elif (type == 'float'):
							value = XPLMGetDataf(dataref)

						value = value + increment
						if (value > max or value < min):
							value = min
					else:
						value = definition.get('on') if state == 1 else definition.get('off')

					if (type == 'int'):
						XPLMSetDatai(dataref, value)
					elif (type == 'float'):
						XPLMSetDataf(dataref, value)
		except serial.SerialException:
			print "Exception: No connection found"
			return 1;
		except serial.SerialTimeoutException:
			print "Exception: Connection timed out"
		except:
			print "Unexpected error: %s" % sys.exc_info()[1]
		
		return self.interval;
