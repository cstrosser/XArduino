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

class ArduinoMalformedLine(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)

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
    KEY_SWITCH13 = "switch13"
    KEY_SWITCH14 = "switch14"
    KEY_SWITCH15 = "switch15"
    KEY_SWITCH16 = "switch16"
    OFFSET_BUTTON1 = 0
    OFFSET_BUTTON2 = 1
    OFFSET_BUTTON3 = 2
    OFFSET_BUTTON4 = 3
    OFFSET_SWITCH1 = 4
    OFFSET_SWITCH2 = 5
    OFFSET_SWITCH3 = 6
    OFFSET_SWITCH4 = 7
    OFFSET_SWITCH5 = 8
    OFFSET_SWITCH6 = 9
    OFFSET_SWITCH7 = 10
    OFFSET_SWITCH8 = 11
    OFFSET_SWITCH9 = 16
    OFFSET_SWITCH10 = 17
    OFFSET_SWITCH11 = 18
    OFFSET_SWITCH12 = 19
    OFFSET_SWITCH13 = 12
    OFFSET_SWITCH14 = 13
    OFFSET_SWITCH15 = 14
    OFFSET_SWITCH16 = 15

    def XPluginStart(self):
        self.Name = "XArduino"
        self.Sig =  "strosser.usb.xarduino"
        self.Desc = "Interfaces Arduino with X-Plane"
        
        self.configFile = "xarduino.ini"
        self.systemPath = XPLMGetSystemPath("")
        self.interval = -1

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
            self.KEY_SWITCH13 : self.OFFSET_SWITCH13,
            self.KEY_SWITCH14 : self.OFFSET_SWITCH14,
            self.KEY_SWITCH15 : self.OFFSET_SWITCH15,
            self.KEY_SWITCH16 : self.OFFSET_SWITCH16,
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
        
        config = ConfigParser.ConfigParser()
        config.read(self.systemPath + "Resources/plugins/PythonScripts/" + self.configFile)
        
        if ('main' in config.sections()):
            try:
                self.s = serial.Serial(config.get('main', 'port'), config.get('main', 'baud'), timeout = 0)

                self.bufferA = 0
                self.bufferB = 0
                
                self.FlightLoopCB = self.FlightLoopCallback
                XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, self.interval, 0)
            except serial.SerialException:
                self.s = None
        
        return self.Name, self.Sig, self.Desc
    
    def config(self):
        plane, planePath = XPLMGetNthAircraftModel(0)
        
        config = ConfigParser.RawConfigParser()
        if (not config.read(planePath.replace(plane, self.configFile))):
            config.read(self.systemPath + "Resources/plugins/PythonScripts/" + self.configFile)
                     
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
                    definitions[section][0] = int(definitions[section]['0'])
                    definitions[section][1] = int(definitions[section]['1'])
                    
                    position2 = definitions[section].get('2')
                    if (position2 != None):
                        definitions[section][2] = int(definitions[section]['2'])
                elif (type == 'float'):
                    definitions[section][0] = float(definitions[section]['0'])
                    definitions[section][1] = float(definitions[section]['1'])
                    
                    position2 = definitions[section].get('2')
                    if (position2 != None):
                        definitions[section][2] = float(definitions[section]['2'])
        
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
        if self.s:
            # Unregister the callback
            XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)
            self.s.close()
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
        try:
            line = self.s.readline()
            
            if (len(line) <= 2):
                return self.interval
            
            if (line[0:2] == "A,"):
                buffer = int(line[2:])
                if (buffer == self.bufferA):
                    return self.interval
            
                self.bufferA = buffer
                bufferRange = range(16)
            elif (line[0:2] == "B,"):
                buffer = int(line[2:])
                if (buffer == self.bufferB):
                    return self.interval
                    
                self.bufferB = buffer
                bufferRange = range(16, 20)
            else:
                raise ArduinoMalformedLine(line)
            
            offset = 0
            for offset in bufferRange:
                self.processArduinoResult(buffer, offset)
        except serial.SerialException:
            print "Exception: No connection found"
            return 1
        except serial.SerialTimeoutException:
            print "Exception: Connection timed out"
            return 1
        except ArduinoMalformedLine as e:
            print 'Malformed line detected: ' + e.value
        except:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            print "Unexpected error: %s" % exc_obj
            print "Output: %s" % buffer
            print "Bit: %s" % offset
            print "Line #: %s" % exc_tb.tb_lineno
        
        return self.interval
    
    def processArduinoResult(self, buffer, offset):
            if (buffer & (1 << (offset if offset < 16 else (offset - 16)))):
                value = "1"
            else:
                value = "0"
            '''
            elif (buffer & (2 << offset)):
                #print "setting value 2 for %s" % offset
                #value = "2"
            '''
            
            state = int(value)
            
            key = self.offsetToButton.get(offset)
            if (key == None):
                print "Cannot find button for offset :: " + key
                return
            
            definition = self.definitions.get(key)
            mode = definition.get('mode')
            if (mode == 'command'):
                commandString = definition.get('command')
                if (commandString == None):
                    return
                    
                command = self.getCommand(commandString)
                if (command == None):
                    return
                    
                if state == 1:
                    XPLMCommandOnce(command)
            elif (mode == 'command-toggle'):
                if state == 0:
                    commandString0 = definition.get('command_0')
                    if commandString0 == None:
                        return
                    
                    if '("' in commandString0:
                        evalCommands = eval(commandString0)
                        for evalCommand in evalCommands:
                            command = self.getCommand(evalCommand)
                            if command == None:
                                return
                            
                            XPLMCommandOnce(command)
                    else:
                        command0 = self.getCommand(commandString0)
                        if command0 == None:
                            return
                            
                        XPLMCommandOnce(command0)
                elif state == 1:
                    commandString1 = definition.get('command_1')
                    if commandString1 == None:
                        return
                    
                    if '("' in commandString1:
                        evalCommands = eval(commandString1)
                        for evalCommand in evalCommands:
                            command = self.getCommand(evalCommand)
                            if command == None:
                                return
                            
                            XPLMCommandOnce(command)
                    else:
                        command1 = self.getCommand(commandString1)
                        if command1 == None:
                            return
                            
                        XPLMCommandOnce(command1)
                elif state == 2:
                    commandString2 = definition.get('command_2')
                    if commandString2 == None:
                        return
                    
                    if '("' in commandString2:
                        evalCommands = eval(commandString2)
                        for evalCommand in evalCommands:
                            command = self.getCommand(evalCommand)
                            if command == None:
                                return
                            
                            XPLMCommandOnce(command)
                    else:
                        command2 = self.getCommand(commandString2)
                        if command2 == None:
                            return
                            
                        XPLMCommandOnce(command2)
            else:
                datarefString = definition.get('dataref')
                if (datarefString == None):
                    return
                
                dataref = self.getDataref(datarefString)
                if (dataref == None):
                    return
                
                type = definition.get('type')
                if (mode == 'loop'):
                    if state == 0:
                        self.lastState[offset] = 0
                        return
                    if self.lastState[offset] == 1:
                        return
                    self.lastState[offset] = 1

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
                        currentValue = XPLMGetDatai(dataref)
                    elif (type == 'float'):
                        currentValue = XPLMGetDataf(dataref)
                    
                    if (currentValue == value):
                        return
                        
                    

                if (type == 'int'):
                    XPLMSetDatai(dataref, value)
                elif (type == 'float'):
                    XPLMSetDataf(dataref, value)
    
    def MenuHandlerCallback(self, inMenuRef, inItemRef):
        if (inItemRef == reloadConfig):
            self.config()
        pass
