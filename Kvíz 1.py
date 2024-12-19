class Kviz:
    def __init__(self):
        self.otazky = [
            ("Jaký žák ze třídy IT3B nejvíce spí", ["Jan Kirpal", "Martin Brunclík", "Adam Lavrikov"], "Jan Kirpal"),
            ("Kolik budov má hlavní budova SOUE?", ["1", "2", "3"], "3"),
            ("Kdo je zástupce ředitele?", ["Jaroslav Černý", "Martin Jurák", "Petr Breit"], "Martin Jurák"),
            ("Kdo učí matematiku?", ["Šárka Kůsová", "Jan Bezděka", "Ivan Gemela"], "Šárka Kůsová"),
            ("Jaké číslo má kabinet učitele Petra Breita", ["B113", "6309", "B202"], "B202"),
  
        ]
        self.spravne_odpovedi = 0
    
    def spustit(self):
        # Dynamicky se vypočítá počet otázek
        pocet_otazek = len(self.otazky)
        # Umožní uživateli vybrat otázku od 1 do počtu otázek
        while True:
            try:
                cislo_otazky = int(input(f"Vyber číslo otázky (1 až {pocet_otazek}): ")) - 1
                if 0 <= cislo_otazky < pocet_otazek:
                    break  # Pokud je číslo otázky platné, přejdeme k dalšímu kroku
                else:
                    print(f"Vyber číslo otázky mezi 1 a {pocet_otazek}.")
            except ValueError:
                print("Neplatný výběr, zadejte číslo.")
        
        otazka_obj = self.otazky[cislo_otazky]
        otazka = otazka_obj[0]
        odpovedi = otazka_obj[1]
        spravna_odpoved = otazka_obj[2]
        self.vyhodnoceni(otazka, odpovedi, spravna_odpoved)

    def vyhodnoceni(self, otazka, odpovedi, spravna_odpoved):
        print(otazka)

        for index, odpoved in enumerate(odpovedi, 1):
            print(f"{index}. {odpoved}")
        
        try:
            vyber = int(input("Vyber odpověď: ")) - 1
            if odpovedi[vyber] == spravna_odpoved:
                print("Správně")
            else:
                print("Špatně")
        except (ValueError, IndexError):
            print("Neplatný výběr")
            pass      


kviz = Kviz()
kviz.spustit()
