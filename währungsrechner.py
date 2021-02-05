# App, die mit Hilfe von Echtzeit-Wechselkursen Währungen umrechnet
# Basis hierfür ist die folgende kostenlose API: https://www.exchangerate-api.com/

# Für uns wichtige Daten des JSON Objects:
# - base_code: Ausgangsbasis von welcher jeder Wechselkurs bestimmt wird.
# - time_last_update_utc: zeigt wann Daten letzte mal geupdated wurden
# - conversion_rates: Wechselkurs von Währungen mit der Basiswährung EUR.

import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk

# Klasse, um den Umrechnungsprozess zu beschreiben
class WaehrungsRechner():
    # Abfrage des Wechselkurses
    def __init__(self, url):
            # Laden der Seite und konvertieren in JSON Object
            self.data = requests.get(url).json()
            self.currencies = self.data['conversion_rates'] # speichern der gesamten Wechselkurse in ein dict
    # Methode, die die eingegebene Währung ggf. umrechnet und den Betrag ausgibt
    def convert(self, from_currency, to_currency, amount):
        # from_currency: Währung, welche man umrechnen möchte
        # to_currency: Währung, in die umgerechnet werden soll
        # amount: Menge/Anzahl der Währung

        # Eingegebene Währung umrechnen in EUR, falls nicht der Fall, da Ausgangsbasis der EUR ist
        if from_currency != 'EUR' :
            amount = amount / self.currencies[from_currency]
        # Runden auf 2 Nachkommastellen
        amount = round(amount * self.currencies[to_currency], 2)

        return amount

# Klasse, die das UI für den Währungsrechner erstellt.
# Hierfür wird das Modul tkinter genutzt
class App(tk.Tk):

    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.currency_converter = converter
        
        # Größe der App
        self.geometry("500x200")

        # Überschrift + styling
        self.intro_label = Label(self, text = 'Realtime Währungsrechner',  fg = 'black', relief = tk.RIDGE, borderwidth = 3)
        self.intro_label.config(font = ('Arial', 10, 'bold'))
        self.intro_label.place(x = 170 , y = 5)

        # Label für die Anzeige des aktuellen Umrechnungskurses EUR <-> USD
        self.date_label = Label(self, text = f"1 EUR = {self.currency_converter.convert('EUR','USD',1)} USD", relief = tk.RIDGE, borderwidth = 3)
        self.date_label.place(x = 80, y= 50)

        # Label für die Anzeige des Datums von wann der Umrechnungskurs ist
        self.date_updated_label = Label(self, text = f"Kurs vom: {self.currency_converter.data['time_last_update_utc']}", relief = tk.RIDGE, borderwidth = 3)
        self.date_updated_label.place(x = 200, y = 50)

        # Variable speichert den eingegebenen Wert.
        currencie_amount = tk.StringVar()

        # Eingabefeld (links) und Ausgabefeld (rechts)
        self.amount_field = Entry(self, bd = 3, relief = tk.RIDGE, justify = tk.CENTER, textvariable=currencie_amount)
        self.converted_amount_field_label = Label(self, text = '', fg = 'black', bg = 'white', relief = tk.RIDGE, justify = tk.CENTER, width = 17, borderwidth = 3)
        
        # Hinweis zur Eingabe 
        self.intro_label = Label(self, text = 'Eingabe bitte mit Punkt statt Komma trennen',  fg = 'black')
        self.intro_label.config(font = ('Arial', 7, 'bold'))
        self.intro_label.place(x = 15 , y = 150) 
        
        # Dropdowns
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("EUR") # setze EUR als default links
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD") # setze USD als default rechts

        font = ("Courier", 12, "bold")
        # Generieren der dropdowns mit den keys aus dem dict conversion_rates als values
        self.from_currency_dropdown = ttk.Combobox(self, textvariable=self.from_currency_variable,
                                                   values=list(self.currency_converter.currencies.keys()), font = font, 
                                                   state = 'readonly', width = 12, justify = tk.CENTER)
        self.to_currency_dropdown = ttk.Combobox(self, textvariable=self.to_currency_variable,
                                                 values=list(self.currency_converter.currencies.keys()), font = font,
                                                 state = 'readonly', width = 12, justify = tk.CENTER)

        # Positioning der dropdowns und des Ein- und Ausgabefelds
        self.from_currency_dropdown.place(x = 30, y= 90)
        self.amount_field.place(x = 36, y = 120)
        self.to_currency_dropdown.place(x = 340, y= 90)
        self.converted_amount_field_label.place(x = 346, y = 120)

        # Button Umrechnung
        # self.perfom -> Bei klick des Buttons: Ausführung der Methode perfom()
        self.convert_button = Button(self, text = "Umrechnung", fg = "black", command = self.perform)
        self.convert_button.config(font=('Courier', 10, 'bold'))
        self.convert_button.place(x = 205, y = 115)

    def perform(self):
        # Methode nimmt die Benutzereingabe und rechnet den Betrag in die gewünschte Währung um
        # Anzeige im Ausgabefeld converted_amount_field_label.
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        # Umrechnung mit der convert() Methode
        converted_amount = self.currency_converter.convert(from_curr,to_curr,amount)
        converted_amount = round(converted_amount, 2)

        # Ausgabe in das leere Feld (erwartet string)
        self.converted_amount_field_label.config(text = str(converted_amount))

if __name__ == '__main__':
    #API
    url = 'https://v6.exchangerate-api.com/v6/d481e4df571f55dafd6bcffa/latest/EUR'

    converter = WaehrungsRechner(url)
    App(converter)
    mainloop()
