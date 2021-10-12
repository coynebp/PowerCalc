import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkfont
import tkinter.messagebox as tkmessagebox


class PowerError(Exception):
    '''Error when provided incorrect values for power calculations'''
    
    def __init__(self, message):
        self.message = message

class FLACalculator(object):
    def __init__(self):
        self._hp = 0
        self._amps = 0
        self._powerFactor = 1
        self._volts = 480
        self._kva = 0
        self._kw = 0
        self._efficiency = 1
        self._threephase = 1

    @property
    def volts(self):
        return self._volts
    @volts.setter
    def volts(self, value):
        if value < 0:
            raise PowerError("RMS voltage cannot be negative")
        self._volts = value
    
    @property
    def powerFactor(self):
        return self._powerFactor
    @powerFactor.setter
    def powerFactor(self, value):
        if value < -1 or value > 1:
            raise PowerError("Power factor must be between -1 and 1")
        self._powerFactor = value
    
    @property
    def efficiency(self):
        return self._efficiency
    @efficiency.setter
    def efficiency(self, value):
        if value < 0 or value > 1:
            raise PowerError("Efficiency must be between 0 and 1")
        self._efficiency = value
    
    @property
    def kw(self):
        return self._kw
    @kw.setter
    def kw(self, value):
        if value < 0:
            raise PowerError("KW cannot be negative")
        self._kw = value

    @property
    def hp(self):
        return self._hp
    @hp.setter
    def hp(self, value):
        if value < 0:
            raise PowerError("Horsepower cannot be negative")
        self._hp = value

    @property
    def amps(self):
        return self._amps
    @amps.setter
    def amps(self, value):
        if value < 0:
            raise PowerError("RMS current cannot be negative")
        self._amps = value

    @property
    def kva(self):
        return self._kva
    @kva.setter
    def kva(self, value):
        if value < 0:
            raise PowerError("KVA cannot be negative")
        self._kva = value
    
    @property
    def threephase(self):
        return self._threephase
    @threephase.setter
    def threephase(self, value):
        if value != 0 and value != 1:
            raise PowerError("Must be three phase or single phase")
        self._threephase = value

    def __str__(self):
        return "Volts: " + str(self.volts) + \
        "\nPF   : " + str(self.powerFactor) + \
        "\nEff  : " + str(self.efficiency) + \
        "\nkW   : " + str(self.kw) + \
        "\nhp   : " + str(self.hp) + \
        "\nAmps : " + str(self.amps) + \
        "\nkVA  : " + str(self.kva)
    
    def fromAmps(self):
        try:
            self.kva = self.volts * self.amps * (1 + 0.73 * self._threephase) / 1000
            self.kw = self.kva * self.powerFactor
            self.hp = self.volts * self.amps * self.efficiency * self.powerFactor * (1 + 0.73 * self._threephase) / 746
        except ZeroDivisionError:
            tkmessagebox.showerror(title="Error", message="Cannot divide by zero")
        
    def fromKva(self):
        try:
            self.amps = self.kva * 1000 / (self.volts * (1 + 0.73 * self._threephase))
            self.kw = self.kva * self.powerFactor
            self.hp = self.volts * self.amps * self.efficiency * self.powerFactor * (1 + 0.73 * self._threephase) / 746
        except ZeroDivisionError:
            tkmessagebox.showerror(title="Error", message="Cannot divide by zero")

    def fromKw(self):
        try:
            self.amps = self.kw * 1000 / (self.volts * self.powerFactor * (1 + 0.73 * self._threephase))
            self.kva = self.kw / self.powerFactor
            self.hp = self.volts * self.amps * self.efficiency * self.powerFactor * (1 + 0.73 * self._threephase) / 746
        except ZeroDivisionError:
            tkmessagebox.showerror(title="Error", message="Cannot divide by zero")

    def fromHp(self):
        try:
            self.amps = self.hp * 746 / (self.volts * self.efficiency * self.powerFactor * (1 + 0.73 * self._threephase))
            self.kva = self.volts * self.amps * (1 + 0.73 * self._threephase) / 1000
            self.kw = self.kva * self.powerFactor
        except ZeroDivisionError:
            tkmessagebox.showerror(title="Error", message="Cannot divide by zero")

class CalculatorApp(object):
    def __init__(self):
        #create calculator instance
        self.calculator = FLACalculator()
        #create tk instance
        self.root = tk.Tk()
        #set title and icon
        self.root.title("PowerCalc")
        directory = os.path.dirname(__file__)
        iconpath = os.path.join(directory, 'power_icon.ico')
        self.root.iconbitmap(iconpath)
        #create fonts
        title = tkfont.Font(self.root, size=28, weight=tkfont.BOLD, underline=True)
        entry = tkfont.Font(self.root, size=14)
        result = tkfont.Font(self.root, size=20, weight=tkfont.BOLD)
        #create tkinter variables
        self.titleLabel = tk.Label(self.root, text='PowerCalc', font=title)
        self.phases = tk.IntVar(value = 1)
        self.phaseButton1 = tk.Radiobutton(self.root, text='Single-Phase', variable=self.phases, value=0, font=entry)
        self.phaseButton2 = tk.Radiobutton(self.root, text='Three-Phase', variable=self.phases, value=1, font=entry)
        self.voltsStr = tk.StringVar(value='480')
        self.voltsEntry = tk.Entry(self.root, textvariable=self.voltsStr, font=entry)
        self.voltsLabel = tk.Label(self.root, text='Volts', font=entry)
        self.powerFactorStr = tk.StringVar(value='1')
        self.powerFactorEntry = tk.Entry(self.root, textvariable=self.powerFactorStr, font=entry)
        self.powerFactorLabel = tk.Label(self.root, text='P.F.', font=entry)
        self.efficiencyStr = tk.StringVar(value='1')
        self.efficiencyEntry = tk.Entry(self.root, textvariable=self.efficiencyStr, font=entry)
        self.efficiencyLabel = tk.Label(self.root, text='Efficiency', font=entry)
        self.powerStr = tk.StringVar(value='0')
        self.powerEntry = tk.Entry(self.root, textvariable=self.powerStr, font=entry)
        self.powerBoxStr = tk.StringVar(value='kVA')
        self.powerBox = ttk.Combobox(self.root, textvariable=self.powerBoxStr, values=['kVA', 'kW', 'hp', 'Amps'], font=entry)
        self.calculateButton = tk.Button(self.root, text='Calculate', command = self.calculate, font=entry)
        self.result1 = tk.Label(self.root, text='0', font=result)
        self.result1Label = tk.Label(self.root, text='--', font=result)
        self.result2 = tk.Label(self.root, text='0', font=result)
        self.result2Label = tk.Label(self.root, text='--', font=result)
        self.result3 = tk.Label(self.root, text='0', font=result)
        self.result3Label = tk.Label(self.root, text='--', font=result)
        #bind enter key
        self.root.bind('<Return>', self.calculate)
        
        self.runApp()

    def calculate(self, event=None):
        try:
            self.calculator.volts = float(self.voltsStr.get())
            self.calculator.powerFactor = float(self.powerFactorStr.get())
            self.calculator.efficiency = float(self.efficiencyStr.get())
            self.calculator.threephase = self.phases.get()
        except ValueError:
            tkmessagebox.showerror(title="Error", message="Please provide only decimal numbers")
        except PowerError as error:
            tkmessagebox.showerror(title="Error", message=error.message)

        if self.powerBoxStr.get() == 'kVA':
            try:
                self.calculator.kva = float(self.powerStr.get())
            except PowerError as error:
                tkmessagebox.showerror(title="Error", message=error.message)
            self.calculator.fromKva()
            self.result1.config(text=str(round(self.calculator.kw, 2)))
            self.result1Label.config(text = 'kW')
            self.result2.config(text=str(round(self.calculator.hp, 2)))
            self.result2Label.config(text = 'hp')
            self.result3.config(text=str(round(self.calculator.amps, 2)))
            self.result3Label.config(text = 'Amps')
        elif self.powerBoxStr.get() == 'kW':
            try:
                self.calculator.kw = float(self.powerStr.get())
            except PowerError as error:
                tkmessagebox.showerror(title="Error", message=error.message)
            self.calculator.fromKw()
            self.result1.config(text=str(round(self.calculator.kva, 2)))
            self.result1Label.config(text = 'kVA')
            self.result2.config(text=str(round(self.calculator.hp, 2)))
            self.result2Label.config(text = 'hp')
            self.result3.config(text=str(round(self.calculator.amps, 2)))
            self.result3Label.config(text = 'Amps')
        elif self.powerBoxStr.get() == 'hp':
            try:
                self.calculator.hp = float(self.powerStr.get())
            except PowerError as error:
                tkmessagebox.showerror(title="Error", message=error.message)
            self.calculator.fromHp()
            self.result1.config(text=str(round(self.calculator.kva, 2)))
            self.result1Label.config(text = 'kVA')
            self.result2.config(text=str(round(self.calculator.kw, 2)))
            self.result2Label.config(text = 'kW')
            self.result3.config(text=str(round(self.calculator.amps, 2)))
            self.result3Label.config(text = 'Amps')
        else:
            try:
                self.calculator.amps = float(self.powerStr.get())
            except PowerError as error:
                tkmessagebox.showerror(title="Error", message=error.message)
            self.calculator.fromAmps()
            self.result1.config(text=str(round(self.calculator.kva, 2)))
            self.result1Label.config(text = 'kVA')
            self.result2.config(text=str(round(self.calculator.kw, 2)))
            self.result2Label.config(text = 'kW')
            self.result3.config(text=str(round(self.calculator.hp, 2)))
            self.result3Label.config(text = 'hp')
    
    def runApp(self):
        #build window
        self.root.grid()
        self.titleLabel.grid(row=0, column=0, pady=15, columnspan=2)
        self.phaseButton1.grid(row=1, column=0, sticky='w')
        self.phaseButton2.grid(row=1, column=1, sticky='w')
        self.voltsEntry.grid(row=2, column=0, pady=2)
        self.voltsLabel.grid(row=2, column=1, pady=2, sticky='w')
        self.powerFactorEntry.grid(row=3, column=0, pady=2)
        self.powerFactorLabel.grid(row=3, column=1, pady=2, sticky='w')
        self.efficiencyEntry.grid(row=4, column=0, pady=2)
        self.efficiencyLabel.grid(row=4, column=1, pady=2, sticky='w')
        self.powerEntry.grid(row=5, column=0, pady=2)
        self.powerBox.grid(row=5, column=1, pady=2, sticky='w')
        self.calculateButton.grid(row=6,column=0, columnspan=2, pady=15, ipadx=80)
        self.result1.grid(row=7, column=0, sticky='w')
        self.result1Label.grid(row=7, column=1, sticky='w')
        self.result2.grid(row=8, column=0, sticky='w')
        self.result2Label.grid(row=8, column=1, sticky='w')
        self.result3.grid(row=9, column=0, sticky='w')
        self.result3Label.grid(row=9, column=1, sticky='w')
        #run app
        self.root.mainloop()

def main():
    CalculatorApp()  

if __name__ == "__main__":
    main()

