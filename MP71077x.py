import socket
import ipaddress
import re
import colorama
from colorama import Fore
from colorama import Style

class MP71077x:
    _target_ip = ""
    _source_ip = ""
    _port = 0
    _timeout = 0

    _udp_socket = None

    _verbose = False

    def __init__(self, source_ip: ipaddress.IPv4Address, target_ip: ipaddress.IPv4Address, port: int = 18190, timeout: float = 0.2, verbosity: bool = False):
        self._target_ip = target_ip
        self._source_ip = source_ip
        self._port = port
        self._timeout = timeout
        self._verbose = verbosity
        colorama.init()

    def openSocket(self):
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_socket.bind((self._source_ip, self._port))
        self._udp_socket.settimeout(self._timeout)

    def closeSocket(self):
        self._udp_socket.close()

    def sendCommand(self, command: str, waitForResponse: bool = False):
        self._udp_socket.sendto((command + "\n").encode(), (self._target_ip, self._port))

        response = None
        sender_address = None
        if waitForResponse == True:
            try:
                response, sender_address = self._udp_socket.recvfrom(1024)
            except socket.error as e:
                raise ConnectionError("Command response timeout!")

            return response.decode()
    
    def _printMessage(self, message):
        if self._verbose:
            print(f"{Fore.YELLOW}MP71077x{Fore.BLUE}({self._target_ip}): {Style.RESET_ALL}{message}")

    def turnInputON(self, verify: bool = False):
        self.sendCommand(":INP 1")

        if verify == True:
            response = self.sendCommand(":INP?", True)
            if "ON" not in response:
                raise ConnectionError("Can not verify if load was turned on properly!")
            self._printMessage("Load input has been turned off")
            return
        self._printMessage("Load turn on command has been send.")

    def turnInputOFF(self, verify: bool = False):
        self.sendCommand(":INP 0")

        if verify == True:
            response = self.sendCommand(":INP?", True)
            if "OFF" not in response:
                raise ConnectionError("Can not verify if load was turned off properly!")
            self._printMessage("Load input has been turned off")
            return
        self._printMessage("Load turn off command has been send.")

    #MP71077x uses only 5 valid digits of floating point number
    def roundTo5ValidDigits(self, x: float):
        if self._verbose == True:
            if len(str(x).replace(".", "")) > 5:
                self._printMessage("Entered value will be rounded to 5 valid digits")
        if (x < 10.0):
            return round(x, 4)
        if (x < 100.0):
            return round(x, 3)        
        return round (x, 2)
    
    ################################################################################################################################################################
    # VOLTAGE SETTINGS
    ################################################################################################################################################################

    def getUpperVoltageLimit(self):
        if self._verbose:
            self._printMessage("Asking for upper voltage limit")
        limit = self.sendCommand(":VOLT:UPP?", True)
        return float(re.sub(r"[^\d\.]", "", limit))
    
    def setUpperVoltageLimit(self, limit: float, verify: bool = False):
        limit = self.roundTo5ValidDigits(limit)
        self._printMessage(f"Setting upper voltage limit to {limit}V")
        self.sendCommand(":VOLT:UPP " + str(limit) + "V")

        if verify == True:
            response = self.getUpperVoltageLimit()
            if response != limit:
                raise ConnectionError(f"Can not confirm that upper voltage limit was properly set!: SET: {limit}V, but GET: {response}V")

    def getLowerVoltageLimit(self):
        self._printMessage("Asking for lower voltage limit")
        limit = self.sendCommand(":VOLT:LOW?", True)
        return float(re.sub(r"[^\d\.]", "", limit))
  
    def getVoltageLimits(self):
        self._printMessage("Asking for both voltage limits")
        return (self.getLowerVoltageLimit(), self.getUpperVoltageLimit())
    
    def getCVvoltage(self):
        self._printMessage("Asking for CV voltage")
        cv = self.sendCommand(":VOLT?", True)
        return float(re.sub(r"[^\d\.]", "", cv))

    def setCVvoltage(self, voltage: float, verify: bool = False):
        voltage = self.roundTo5ValidDigits(voltage)
        self._printMessage(f"Setting CV voltage to {voltage}")
        self.sendCommand(":VOLT " + str(voltage) + "V")
        
        if verify == True:
            response = self.getCVvoltage()
            if response != voltage:
                raise ConnectionError(f"Can not confirm that CV voltage was properly set!: SET: {voltage}V, but GET: {response}V")
       
    ################################################################################################################################################################
    # CURRENT SETTINGS
    ################################################################################################################################################################

    def getUpperCurrentLimit(self):
        if self._verbose:
            self._printMessage("Asking for upper current limit")
        limit = self.sendCommand(":CURR:UPP?", True)
        return float(re.sub(r"[^\d\.]", "", limit))
    
    def setUpperCurrentLimit(self, limit: float, verify: bool = False):
        limit = self.roundTo5ValidDigits(limit)
        self._printMessage(f"Setting upper current limit to {limit}A")
        self.sendCommand(":CURR:UPP " + str(limit) + "A")

        if verify == True:
            response = self.getUpperCurrentLimit()
            if response != limit:
                raise ConnectionError(f"Can not confirm that upper current limit was properly set!: SET: {limit}A, but GET: {response}A")

    def getLowerCurrentLimit(self):
        self._printMessage("Asking for lower current limit")
        limit = self.sendCommand(":CURR:LOW?", True)
        return float(re.sub(r"[^\d\.]", "", limit))
  
    def getCurrentLimits(self):
        self._printMessage("Asking for both current limits")
        return (self.getLowerCurrentLimit(), self.getUpperCurrentLimit())
    
    def getCIcurrent(self):
        self._printMessage("Asking for CI current")
        cv = self.sendCommand(":CURR?", True)
        return float(re.sub(r"[^\d\.]", "", cv))

    def setCIcurrent(self, current: float, verify: bool = False):
        current = self.roundTo5ValidDigits(current)
        self._printMessage(f"Setting CI current to {current}")
        self.sendCommand(":CURR " + str(current) + "A")
        
        if verify == True:
            response = self.getCIcurrent()
            if response != current:
                raise ConnectionError(f"Can not confirm that CI current was properly set!: SET: {current}A, but GET: {response}A")
       
    ################################################################################################################################################################
    # POWER SETTINGS
    ################################################################################################################################################################

    def getUpperPowerLimit(self):
        if self._verbose:
            self._printMessage("Asking for upper power limit")
        limit = self.sendCommand(":POW:UPP?", True)
        return float(re.sub(r"[^\d\.]", "", limit))
    
    def setUpperPowerLimit(self, limit: float, verify: bool = False):
        limit = self.roundTo5ValidDigits(limit)
        self._printMessage(f"Setting upper power limit to {limit}W")
        self.sendCommand(":POW:UPP " + str(limit) + "W")

        if verify == True:
            response = self.getUpperPowerLimit()
            if response != limit:
                raise ConnectionError(f"Can not confirm that upper power limit was properly set!: SET: {limit}W, but GET: {response}W")

    def getLowerPowerLimit(self):
        self._printMessage("Asking for lower power limit")
        limit = self.sendCommand(":POW:LOW?", True)
        return float(re.sub(r"[^\d\.]", "", limit))
  
    def getPowerLimits(self):
        self._printMessage("Asking for both power limits")
        return (self.getLowerPowerLimit(), self.getUpperPowerLimit())
    
    def getCPpower(self):
        self._printMessage("Asking for CP power")
        cv = self.sendCommand(":POW?", True)
        return float(re.sub(r"[^\d\.]", "", cv))

    def setCPpower(self, power: float, verify: bool = False):
        power = self.roundTo5ValidDigits(power)
        self._printMessage(f"Setting CP power to {power}")
        self.sendCommand(":POW " + str(power) + "W")
        
        if verify == True:
            response = self.getCPpower()
            if response != power:
                raise ConnectionError(f"Can not confirm that CP power was properly set!: SET: {power}W, but GET: {response}W")
