import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os

class Salladsbar:
    def __init__(self, master):
        self.master = master
        self.master.title("Salladsbaren")

        # Initiering av data
        self.sallader = {}
        self.ingredienser = {}
        self.valda_extra_ingredienser = []

        # Ladda data från filer
        self.ladda_data()

        # Visa huvudmeny
        self.huvudmeny()

    def ladda_data(self):
        """ Läser in sallads- och ingrediensdata från filer och hanterar eventuella fel. """
        try:
            with open("sallader.json", "r") as f:
                self.sallader = json.load(f)
            with open("ingredienser.json", "r") as f:
                self.ingredienser = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Fel", "Datafiler saknas!")
            self.master.quit()

    def huvudmeny(self):
        """ Skapar huvudmenyn där användaren kan välja att beställa en sallad eller avsluta. """
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Välkommen till Salladsbaren!", font=("Helvetica", 16)).pack(pady=10)
        tk.Button(self.master, text="Välj sallad", command=self.valj_sallad).pack(pady=5)
        tk.Button(self.master, text="Avsluta", command=self.master.quit).pack(pady=5)

    def valj_sallad(self):
        """ GUI där användaren kan välja ingredienser för sin sallad. """
        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Välj ingredienser till din sallad:", font=("Helvetica", 14)).pack(pady=10)

        self.valda_ingredienser = []
        self.ingrediens_vars = []

        for ingr, pris in self.ingredienser.items():
            var = tk.IntVar()
            cb = tk.Checkbutton(self.master, text=f"{ingr} ({pris} kr)", variable=var)
            cb.pack(anchor="w")
            self.ingrediens_vars.append((ingr, var))

        tk.Button(self.master, text="Hitta sallad", command=self.hitta_sallad).pack(pady=10)
        tk.Button(self.master, text="Tillbaka", command=self.huvudmeny).pack(pady=5)

    def hitta_sallad(self):
        """ Jämför valda ingredienser med tillgängliga sallader och föreslår bästa match. """
        valda = [ingr for ingr, var in self.ingrediens_vars if var.get() == 1]

        if not valda:
            messagebox.showinfo("Info", "Du har inte valt några ingredienser.")
            return

        matchande_sallader = []
        for namn, data in self.sallader.items():
            if all(ingr in data["ingredienser"] for ingr in valda):
                matchande_sallader.append((namn, data))

        if matchande_sallader:
            resultat = "\n".join([f"{namn} ({data['pris']} kr)" for namn, data in matchande_sallader])
            val = messagebox.askyesno("Matchande sallader", f"Följande sallader matchar:\n{resultat}\nVill du välja den första?")
            if val:
                self.extra_val(matchande_sallader[0][0])
        else:
            self.forslag_sallad(valda)

    def forslag_sallad(self, valda):
        """ Om ingen sallad matchar exakt föreslås den närmast matchande. """
        bast_match = None
        max_match = 0
        billigast = float('inf')

        for namn, data in self.sallader.items():
            gemensamma = set(valda) & set(data["ingredienser"])
            if len(gemensamma) > max_match or (len(gemensamma) == max_match and data["pris"] < billigast):
                bast_match = (namn, data)
                max_match = len(gemensamma)
                billigast = data["pris"]

        if bast_match:
            namn, data = bast_match
            saknade = set(data["ingredienser"]) - set(valda)
            saknade_ingredienser = ", ".join(saknade)
            val = messagebox.askyesno(
                "Förslag", 
                f"Ingen sallad matchade helt.\nVi föreslår: {namn} ({data['pris']} kr)\nSaknade ingredienser: {saknade_ingredienser}\nVill du välja denna?"
            )
            if val:
                self.extra_val(namn)

    def extra_val(self, vald_sallad):
        """ Meny där användaren kan välja extra ingredienser. """
        self.vald_sallad = vald_sallad
        self.valda_extra_ingredienser = []

        for widget in self.master.winfo_children():
            widget.destroy()

        tk.Label(self.master, text="Lägg till extra ingredienser:", font=("Helvetica", 14)).pack(pady=10)

        self.extra_vars = []
        for ingr, pris in self.ingredienser.items():
            var = tk.IntVar()
            cb = tk.Checkbutton(self.master, text=f"{ingr} ({pris} kr)", variable=var)
            cb.pack(anchor="w")
            self.extra_vars.append((ingr, var))

        tk.Button(self.master, text="Skapa Kvitto", command=self.spara_kvitto).pack(pady=10)
        tk.Button(self.master, text="Tillbaka", command=self.huvudmeny).pack(pady=5)

    def spara_kvitto(self):
        """ Beräknar totalpris och sparar kvitto till fil. """
        extra_valda = [ingr for ingr, var in self.extra_vars if var.get() == 1]
        total_pris = self.sallader[self.vald_sallad]["pris"] + sum(self.ingredienser[ingr] for ingr in extra_valda)

        kvitto_text = f"Kvitto\nSallad: {self.vald_sallad}\nPris: {self.sallader[self.vald_sallad]['pris']} kr\n"
        if extra_valda:
            kvitto_text += "Extra ingredienser:\n"
            for ingr in extra_valda:
                kvitto_text += f" - {ingr}: {self.ingredienser[ingr]} kr\n"
        kvitto_text += f"Totalt pris: {total_pris} kr"

        with open("kvitto.txt", "w") as f:
            f.write(kvitto_text)

        messagebox.showinfo("Kvitto", "Kvitto sparat till fil: kvitto.txt")
        self.huvudmeny()

if __name__ == "__main__":
    root = tk.Tk()
    app = Salladsbar(root)
    root.mainloop()# Uppdatering för ny commit
