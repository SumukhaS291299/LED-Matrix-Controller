from tkinter import simpledialog, messagebox, colorchooser
from colorsysx import rgb_to_hsv
from SerialTransfer import SerialProcessor
import tkinter


class NeoPixelMatrixClient:

    def __init__(self):
        self.SP = SerialProcessor()
        self.SendCommandStr = ""
        self.Serial = SerialProcessor()
        Length, Breadth = self.SetlenBrea()
        self.COMPort = self.SelectCom()
        self.l = Length
        self.b = Breadth
        self.MainWindow()

    def ButtonCallBack(self, LEDno):
        self.LedButtons[LEDno]["state"] = "disabled"
        self.LedButtons[LEDno].configure(bg=self.ColorHex)
        self.SendCommandStr += str(self.Color[0][0]) + "|" + str(self.Color[0][1]) + "|" + str(self.Color[0][2]) + "$"
        self.SendCommandStr += str(LEDno) + "#"
        print("Button pressed", LEDno)
        print("Command", self.SendCommandStr)
        print("Limit Remaining", 8 - (len(self.SendCommandStr) / 11))

    def ClearCommand(self):
        print("Working on a fresh pallet now...")
        self.SP.SendData(self.COMPort, "\n")
        self.SendCommandStr = ""
        for LED in self.LedButtons:
            LED["state"] = "normal"
            LED.configure(bg='white')
            # "enable"

    def SendCommand(self):
        # Remove the last '#' present
        self.SendCommandStr = self.SendCommandStr[:-1]
        if len(self.SendCommandStr) > 88:
            print("The maximum send limit exceded for uno")
        self.SP.SendData(self.COMPort, self.SendCommandStr)

    def ChangeColor(self):
        self.Color = colorchooser.askcolor(title="Change Color")
        self.ColorHex = self.Color[1]

    def ResetCurrent(self):
        self.SendCommandStr = ""

    def MainWindow(self):
        self.mainWin = tkinter.Tk()
        self.mainWin.geometry("450x500")
        self.InitilizeMatrix()
        self.OK = tkinter.Button(self.mainWin, text="OK", command=self.SendCommand)
        self.Clear = tkinter.Button(self.mainWin, text="Clear", command=self.ClearCommand)
        self.ResetCurrent = tkinter.Button(self.mainWin, text="Clear Current", command=self.ResetCurrent)
        self.ChooseColor = tkinter.Button(self.mainWin, text="Change Color", command=self.ChangeColor)
        self.OK.grid(row=self.l + 1, column=0, pady=5)
        self.Clear.grid(row=self.l + 1, column=3, pady=5)
        self.ChooseColor.grid(row=self.l + 1, column=5, pady=5)
        self.ResetCurrent.grid(row=self.l + 1, column=6, pady=5)
        self.mainWin.mainloop()

    def InitilizeMatrix(self):
        itr = 0
        self.LedButtons = []
        for i in range(self.l):
            for j in range(self.b):
                B = tkinter.Button(self.mainWin, text=str(itr), command=lambda k=itr: self.ButtonCallBack(k))
                B.grid(row=i, column=j, pady=2)
                self.LedButtons.append(B)
                itr += 1

    def SetlenBrea(self):
        length = simpledialog.askstring(title="Dimensions Length", prompt="Number of LED's length wise")
        breadth = simpledialog.askstring(title="Dimensions Breadth", prompt="Number of LED's width wise")
        return int(length), int(breadth)

    def SelectCom(self):
        COM = simpledialog.askstring(title="Select Serial Port", prompt="Please Select COM Port (Ex: 'COM2')")
        return COM


NeoPixelMatrixClient()
