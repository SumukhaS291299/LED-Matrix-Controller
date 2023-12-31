import time

import serial
from serial.tools import list_ports


class SerialProcessor:

    def __init__(self):
        print(self.AllComPortsDisplay())

    def ListAvailablePorts(self):
        ports = list_ports.comports()
        ComPorts = {}
        for port, desc, hwid in sorted(ports):
            ComPorts[port] = [desc, hwid]
        return ComPorts

    def AllComPortsDisplay(self):
        ComDef = self.ListAvailablePorts()
        ComPortsAll = ComDef.keys()
        DisplaySting = ''
        DisplaySting += "######################" + "\n"
        for com in ComPortsAll:
            DisplaySting += "COM port: " + str(com) + "\n"
            try:
                DisplaySting += "COM Description: " + ComDef[com][0] + "\n"
            except Exception as E:
                print(E)
            try:
                DisplaySting += "Hardware Identification: " + ComDef[com][1] + "\n"
            except Exception as E:
                print(E)
            DisplaySting += "######################" + "\n"
        return DisplaySting

    def CreateConnection(self, COM: str, BaudRate: int):
        Port = serial.Serial(port=COM, baudrate=BaudRate)
        time.sleep(3)
        Port.timeout = 5
        return Port

    def RecieveData(self, COM, BaudRate=9600):
        Port = self.CreateConnection(COM, BaudRate)
        # time.sleep(3)
        data = Port.readline()
        return data.decode()

    def SendData(self, COM, WriteData: str, BaudRate=9600):
        Port = self.CreateConnection(COM, BaudRate)
        # time.sleep(3)
        try:
            writtenBytes = Port.write(WriteData.encode('utf-8'))
            print(f"Written message of length: {writtenBytes} byte(s)")
        except Exception as e:
            print(f"Could not write data as Error:\n{e}")
        print(f"Data Received: {Port.readline().decode()}")


# SP = SerialProcessor()
# SP.SendData('COM8', "33#44#23#45#12#01#55#06#07")
# time.sleep(10)
# SP.SendData('COM8', "\n")

