import json
import tkinter as tk
from tkinter import messagebox

# Ladda ingredienser och sallader från filer
def load_data():
    with open("ingredienser.json", "r", encoding="utf-8") as f:
        ingredienser = json.load(f)
    with open("sallader.json", "r", encoding="utf-8") as f:
        sallader = json.load(f)
    return ingredienser, sallader

ingredienser, sallader = load_data()

# GUI-applikation
class SalladsbarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Salladsbaren")
        
        self.valda_ingredienser = []
        self.extra_ingredienser = []
        self.vald_sallad = None
        
        tk.Label(root, text="Välj dina ingredienser:").pack()
        
        self.ingredienser_vars = {}
        for ingr in ingredienser.keys():
            var = tk.IntVar()
            chk = tk.Checkbutton(root, text=f"{ingr} ({ingredienser[ingr]} kr)", variable=var)
            chk.pack(anchor='w')
            self.ingredienser_vars[ingr] = var
        
        self.sok_button = tk.Button(root, text="Sök sallad", command=self.sok_sallad)
        self.sok_button.pack()
        
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        
        self.extra_button = tk.Button(root, text="Lägg till extra ingredienser", command=self.lagg_till_extra, state=tk.DISABLED)
        self.extra_button.pack()
        
        self.bekrafta_button = tk.Button(root, text="Bekräfta val och skriv ut kvitto", command=self.skriv_kvitto, state=tk.DISABLED)
        self.bekrafta_button.pack()
    
    def sok_sallad(self):
        self.valda_ingredienser = [ingr for ingr, var in self.ingredienser_vars.items() if var.get() == 1]
        
        print("Valda ingredienser:", self.valda_ingredienser)  # Debugging

        if not self.valda_ingredienser:
            self.result_label.config(text="Välj minst en ingrediens.")
            print("Inga ingredienser valda.")  # Debugging
            return

        best_match = None
        max_match_count = 0
        for sallad, data in sallader.items():
            match_count = len(set(data["ingredienser"]) & set(self.valda_ingredienser))
            print(f"Kontrollerar sallad: {sallad}, Matchning: {match_count}")  # Debugging
            if match_count > max_match_count:
                best_match = sallad
                max_match_count = match_count

        if best_match:
            saknade = set(sallader[best_match]['ingredienser']) - set(self.valda_ingredienser)
            self.vald_sallad = best_match
            self.result_label.config(text=f"Rekommenderad sallad: {best_match} ({sallader[best_match]['pris']} kr). Saknade: {', '.join(saknade)}")
            self.extra_button.config(state=tk.NORMAL)
            self.bekrafta_button.config(state=tk.NORMAL)
            print(f"Rekommenderad sallad: {best_match}, Saknade: {saknade}")  # Debugging
        else:
            self.result_label.config(text="Ingen sallad kan föreslås, välj fler ingredienser.")
            print("Ingen matchande sallad hittades.")  # Debugging
    
    def lagg_till_extra(self):
        self.extra_window = tk.Toplevel(self.root)
        self.extra_window.title("Lägg till extra ingredienser")
        
        self.extra_vars = {}
        for ingr, pris in ingredienser.items():
            var = tk.IntVar()
            chk = tk.Checkbutton(self.extra_window, text=f"{ingr} ({pris} kr)", variable=var)
            chk.pack(anchor='w')
            self.extra_vars[ingr] = var
        
        tk.Button(self.extra_window, text="Bekräfta", command=self.bekräfta_extra).pack()
    
    def bekräfta_extra(self):
        self.extra_ingredienser = [ingr for ingr, var in self.extra_vars.items() if var.get() == 1]
        self.extra_window.destroy()
    
    def skriv_kvitto(self):
        totalpris = sallader[self.vald_sallad]['pris'] + sum(ingredienser[ingr] for ingr in self.extra_ingredienser)
        
        with open("kvitto.txt", "w", encoding="utf-8") as f:
            f.write(f"Kvitto\n-------------------\n")
            f.write(f"Sallad: {self.vald_sallad} ({sallader[self.vald_sallad]['pris']} kr)\n")
            if self.extra_ingredienser:
                f.write(f"Extra ingredienser: {', '.join(self.extra_ingredienser)}\n")
            f.write(f"Totalpris: {totalpris} kr\n")
        
        messagebox.showinfo("Kvitto", f"Kvitto sparat! Totalpris: {totalpris} kr")

if __name__ == "__main__":
    root = tk.Tk()
    app = SalladsbarApp(root)
    root.mainloop()
