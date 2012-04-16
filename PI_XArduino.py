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
from XPLMMenus import *

import serial
import sys

import ConfigParser
from os import path

reloadConfig = 1

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
	KEY_SWITCH9 = "switch9"
	KEY_SWITCH10 = "switch10"
	KEY_SWITCH11 = "switch11"
	KEY_SWITCH12 = "switch12"
	OFFSET_BUTTON1 = 1
	OFFSET_BUTTON2 = 2
	OFFSET_BUTTON3 = 3
	OFFSET_BUTTON4 = 4
	OFFSET_SWITCH1 = 5
	OFFSET_SWITCH2 = 6
	OFFSET_SWITCH3 = 7
	OFFSET_SWITCH4 = 8
	OFFSET_SWITCH5 = 9
	OFFSET_SWITCH6 = 10
	OFFSET_SWITCH7 = 11
	OFFSET_SWITCH8 = 12
	OFFSET_SWITCH9 = 13
	OFFSET_SWITCH10 = 14
	OFFSET_SWITCH11 = 15
	OFFSET_SWITCH12 = 16

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
			self.KEY_SWITCH9 : self.OFFSET_SWITCH9,
			self.KEY_SWITCH10 : self.OFFSET_SWITCH10,
			self.KEY_SWITCH11 : self.OFFSET_SWITCH11,
			self.KEY_SWITCH12 : self.OFFSET_SWITCH12,
		}
		
		self.commands = {}
		self.datarefs = {}
		self.offsetToButton = {}
		self.lastState = {}
		for i in self.buttonToOffset:
			self.offsetToButton[self.buttonToOffset[i]] = i
			self.lastState[self.buttonToOffset[i]] = 0
		
		menu = XPLMAppendMenuItem(XPLMFindPluginsMenu(), "XArduino", 0, 1)
		self.menuHandlerCB = self.MenuHandlerCallback
		self.menu = XPLMCreateMenu(self, "XArduino", XPLMFindPluginsMenu(), menu, self.menuHandlerCB, 0)
		XPLMAppendMenuItem(self.menu, "Reload config", reloadConfig, 1)
		
		try:
			self.s = serial.Serial(11, 9600, timeout=0)

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
					print "cannot find button for offset :: " + key
					continue
				
				definition = self.definitions.get(key)
				mode = definition.get('mode')
				if (mode == 'command'):
					commandString = definition.get('command')
					if (commandString == None):
						continue
						
					command = self.getCommand(commandString)
					if (command == None):
						continue
						
					if state == 1:
						XPLMCommandOnce(command)
				elif (mode == 'command-toggle'):
					commandString0 = definition.get('command_0')
					commandString1 = definition.get('command_1')
					if (commandString0 == None or commandString1 == None):
						continue
						
					command0 = self.getCommand(commandString0)
					command1 = self.getCommand(commandString1)
					if (command0 == None or command1 == None):
						continue
					
					commandString2 = definition.get('command_2')
					if (commandString2 != None):
						command2 = self.getCommand(commandString2)
					
					if state == 2:
						if (command2 != None):
							XPLMCommandOnce(command2)
					elif state == 1:
						XPLMCommandOnce(command1)
					else:
						XPLMCommandOnce(command0)
				else:
					datarefString = definition.get('dataref')
					if (datarefString == None):
						continue
					
					dataref = self.getDataref(datarefString)
					if (dataref == None):
						continue
					
					type = definition.get('type')
					if (mode == 'loop'):
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
					elif (mode == 'dataref'):
						value = definition.get(state)

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
		
	def MenuHandlerCallback(self, inMenuRef, inItemRef):
		if (inItemRef == reloadConfig):
			self.config()
		pass
