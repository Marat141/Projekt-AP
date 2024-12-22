import random

class Role:
    def __init__(self, name, hp, money, strength, dexterity, charisma, intelligence):
        self.name = name
        self.hp = hp
        self.money = money
        self.strength = strength
        self.dexterity = dexterity
        self.charisma = charisma
        self.intelligence = intelligence

class Player:
    def __init__(self, role):
        self.role = role
        self.hp = role.hp
        self.money = role.money
        self.inventory = []

    def show_inventory(self):
        print("\n*** Inventář ***")
        print(f"Role: {self.role.name}")
        print(f"HP: {self.hp}")
        print(f"Peníze: {self.money} KČ")
        print("Předměty:")
        if self.inventory:
            for idx, item in enumerate(self.inventory, 1):
                print(f"  {idx}. {item}")
        else:
            print("  (Inventář je prázdný.)")
        print("\n")

    def adjust_hp(self, amount):
        self.hp += amount

    def adjust_money(self, amount):
        self.money += amount

    def add_item(self, item):
        self.inventory.append(item)

class Encounter:
    def __init__(self, description, choices, required_role, success_story, fail_story):
        self.description = description
        self.choices = choices
        self.required_role = required_role
        self.success_story = success_story
        self.fail_story = fail_story

    def execute(self, player):
        print(self.description)
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice['text']}")

        while True:
            action = input("\nVyber akci (zadej číslo nebo napiš 'inventář' pro zobrazení inventáře): ").strip().lower()
            if action == "inventář":
                player.show_inventory()
                continue

            try:
                choice = int(action) - 1
                if 0 <= choice < len(self.choices):
                    role_bonus = -2 if player.role.name == self.required_role else 2
                    result = random.randint(1, 20) + self.choices[choice]["bonus"] - role_bonus

                    print(f"\nHodil jsi: {result} (po bonusu)")

                    if result >= self.choices[choice]["success_roll"]:
                        print(self.choices[choice]["success_text"])
                        player.adjust_hp(self.choices[choice].get("hp_change", 0))
                        player.adjust_money(self.choices[choice].get("money_change", 0))
                        if "item" in self.choices[choice]:
                            player.add_item(self.choices[choice]["item"])
                            print(f"Do inventáře přidán předmět: {self.choices[choice]['item']}")
                        print(f"\n{self.success_story}\n")
                        return True
                    else:
                        print(self.choices[choice]["fail_text"])
                        player.adjust_hp(self.choices[choice].get("hp_change_fail", 0))
                        player.adjust_money(self.choices[choice].get("money_change_fail", 0))
                        print(f"\n{self.fail_story}\n")
                        return False
                else:
                    print("Neplatná volba. Zkus to znovu.")
            except ValueError:
                print("Zadej platné číslo nebo 'inventář'.")

class Kviz:
    def __init__(self):
        self.kvizy = [
            [
                ("Jaký žák ze třídy IT3B nejvíce spí?", ["Jan Kirpal", "Martin Brunclík", "Adam Lavrikov"], "Jan Kirpal"),
                ("Kolik budov má hlavní budova SOUE?", ["1", "2", "3"], "3"),
                ("Kdo je zástupce ředitele?", ["Jaroslav Černý", "Martin Jurák", "Petr Breit"], "Martin Jurák")
            ],
            [
                ("Kdo učí matematiku?", ["Šárka Kůsová", "Jan Bezděka", "Ivan Gemela"], "Šárka Kůsová"),
                ("Jaké číslo má kabinet učitele Petra Breita?", ["B113", "6309", "B202"], "B202"),
                ("Kolik je tříd v hlavní budově?", ["10", "12", "15"], "15")
            ],
            [
                ("Který předmět je v učebně 305?", ["Fyzika", "Matematika", "Biologie"], "Fyzika"),
                ("Kdo je vedoucí školního klubu?", ["Jan Novák", "Petr Malý", "Eva Černá"], "Eva Černá"),
                ("Jaký je hlavní školní sport?", ["Fotbal", "Basketbal", "Volejbal"], "Fotbal")
            ],
            [
                ("Kolik studentů je ve třídě IT3B?", ["25", "30", "28"], "28"),
                ("Kdo je třídní učitel IT3B?", ["Paní Kovářová", "Pan Dvořák", "Paní Malá"], "Pan Dvořák"),
                ("Která třída má nejlepší docházku?", ["IT3A", "IT3B", "IT2C"], "IT3B")
            ]
        ]
        self.spravne_odpovedi = 0

    def spustit(self, index):
        print(f"\n*** Kvíz {index + 1} ***")
        for otazka_obj in self.kvizy[index]:
            otazka, odpovedi, spravna_odpoved = otazka_obj
            print(otazka)

            for idx, odpoved in enumerate(odpovedi, 1):
                print(f"{idx}. {odpoved}")

            try:
                vyber = int(input("Vyber odpověď: ")) - 1
                if 0 <= vyber < len(odpovedi) and odpovedi[vyber] == spravna_odpoved:
                    print("Správně!")
                    self.spravne_odpovedi += 1
                else:
                    print("Špatně.")
            except (ValueError, IndexError):
                print("Neplatný výběr.")

        print(f"\nSprávné odpovědi: {self.spravne_odpovedi}/{len(self.kvizy[index])}")

class SifrovaciStrojEnigma:
    def __init__(self, shift=3):
        self.shift = shift
        self.abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def zasifrovat(self, text):
        zasifrovany_text = ""
        for znak in text.upper():
            if znak in self.abeceda:
                index = (self.abeceda.index(znak) + self.shift) % len(self.abeceda)
                zasifrovany_text += self.abeceda[index]
            else:
                zasifrovany_text += znak
        return zasifrovany_text

    def desifrovat(self, text):
        desifrovany_text = ""
        for znak in text.upper():
            if znak in self.abeceda:
                index = (self.abeceda.index(znak) - self.shift) % len(self.abeceda)
                desifrovany_text += self.abeceda[index]
            else:
                desifrovany_text += znak
        return desifrovany_text

class Game:
    def __init__(self):
        self.roles = {
            "Elektrikář": Role("Elektrikář", 125, 50, 10, 8, 10, 8),
            "IT specialista": Role("IT specialista", 100, 50, 8, 6, 10, 12),
            "Telekomunikační technik": Role("Telekomunikační technik", 75, 50, 6, 8, 12, 10),
            "Zahradník": Role("Zahradník", 150, 50, 12, 10, 8, 6)
        }
        self.player = None
        self.kviz = Kviz()
        self.sifrovaci_stroj = SifrovaciStrojEnigma()

    def select_role(self):
        print("\n*** Začíná dobrodružství ***\n")
        print("Jsi student na střední škole, která skrývá mnoho tajemství.")
        print("Nejprve si vyber svou roli, která určí tvé schopnosti:\n")
        for idx, role in enumerate(self.roles.keys(), 1):
            print(f"{idx}. {role}")

        while True:
            try:
                choice = int(input("\nZadej číslo své volby: "))
                if 1 <= choice <= len(self.roles):
                    selected_role = list(self.roles.values())[choice - 1]
                    print(f"\nVybral/a jsi: {selected_role.name}\n")
                    self.player = Player(selected_role)
                    return
                else:
                    print("Neplatná volba. Zkus to znovu.")
            except ValueError:
                print("Zadej platné číslo.")

    def sifrovat_a_desifrovat(self, tajna_zprava):
        print("\n*** Šifrování zprávy ***")
        zasifrovana = self.sifrovaci_stroj.zasifrovat(tajna_zprava)
        print(f"Zasifrovaná zpráva: {zasifrovana}")

        print("\nNyní se pokus zprávu dešifrovat.")
        hracova_zprava = input("Zadej dešifrovanou zprávu: ").upper()

        if hracova_zprava == tajna_zprava:
            print("Správně! Úspěšně jsi dešifroval tajnou zprávu a odhalil její význam.")
        else:
            print("Špatně. Nepodařilo se ti správně dešifrovat zprávu.")

    def play(self):
        print("Vítejte v textové adventuře!")
        self.select_role()

        encounters = [
            Encounter(
                """
*** Kapitola 1: Tajemné dráty ***

Procházíš chodbou, když si všimneš visících měděných drátů ze stropu.
Nikde není žádný školník, a tak tě napadá, že bys mohl situaci využít.
Co uděláš?
                """,
                [
                    {"text": "Rozebereš dráty a prodáš je na bleším trhu.", "bonus": 3, "success_roll": 10, "success_text": "Dráty jsi bezpečně odmontoval a prodal za 100 KČ.", "fail_text": "Při pokusu jsi dostal ránu proudem, -5 HP.", "money_change": 100, "hp_change_fail": -5},
                    {"text": "Zavoláš Lakatošovi, aby je rozebral místo tebe.", "bonus": 0, "success_roll": 15, "success_text": "Lakatoš ti zaplatil 30 KČ.", "fail_text": "Lakatoš tě okradl, nezískal jsi nic.", "money_change": 30},
                    {"text": "Odejdi bez pokusu a pokračuj dál.", "bonus": 0, "success_roll": 0, "success_text": "Dráty jsi nechal na místě, nic se nestalo.", "fail_text": "Nic jsi nezískal, ale jsi v bezpečí."}
                ],
                "Elektrikář",
                "Využil jsi situaci na maximum a získal jsi další stopu, která tě vede do IT učebny.",
                "Tvé selhání způsobilo ztrátu času, ale rozhodl ses pokračovat dál s nadějí na lepší příležitosti."
            ),
            Encounter(
                """
*** Kapitola 2: Zamčená učebna ***

Dorazil/a jsi ke dveřím učebny IT. Potřebuješ se dostat dovnitř, protože další stopa je právě zde.
                """,
                [
                    {"text": "Zkusíš najít klíč.", "bonus": 2, "success_roll": 10, "success_text": "Našel/a jsi klíč a odemkl/a dveře.", "fail_text": "Klíč nebyl nikde k nalezení."},
                    {"text": "Pokoušíš se dveře vypáčit.", "bonus": 1, "success_roll": 12, "success_text": "Podařilo se! Dveře jsou otevřené.", "fail_text": "Páčidlo se zlomilo a dveře zůstaly zavřené."}
                ],
                "IT specialista",
                "Dostal/a jsi se do učebny a objevil/a další vodítko!",
                "Nepodařilo se ti otevřít dveře. Ztratil/a jsi čas."
            ),
            Encounter(
                """
*** Kapitola 3: Knihovna a tajný kód ***

Ve školní knihovně hledáš klíčový dokument ukrytý mezi knihami. Musíš se rozhodnout, jak postupovat.
                """,
                [
                    {"text": "Prohledáš všechny police.", "bonus": 3, "success_roll": 12, "success_text": "Našel/a jsi dokument ukrytý mezi knihami!", "fail_text": "Policie jsou příliš rozsáhlé a nic jsi nenašel/a."},
                    {"text": "Zkusíš hledat s pomocí knihovníka.", "bonus": 2, "success_roll": 10, "success_text": "Knihovník ti pomohl najít hledaný dokument.", "fail_text": "Knihovník neměl čas a nepomohl ti."}
                ],
                "Telekomunikační technik",
                "Dokument obsahuje stopu k tajnému sejfu ve škole!",
                "Nic jsi nenašel, ale musíš hledat dál."
            ),
            Encounter(
                """
*** Kapitola 4: Tajná místnost ***

Objevuješ tajnou místnost, kde je ukryto školní tajemství. Čekají tě poslední překážky.
                """,
                [
                    {"text": "Pokusíš se prolomit šifru na dveřích.", "bonus": 3, "success_roll": 15, "success_text": "Úspěšně jsi prolomil šifru a dveře se otevřely!", "fail_text": "Šifra je příliš složitá a dveře zůstávají zavřené."},
                    {"text": "Hledáš tajný mechanismus pro otevření.", "bonus": 2, "success_roll": 12, "success_text": "Našel/a jsi mechanismus a otevřel/a dveře.", "fail_text": "Nic jsi nenašel/a, dveře zůstávají zavřené."}
                ],
                "Zahradník",
                "Odhalil/a jsi školní tajemství a stal/a se hrdinou!",
                "Nepodařilo se ti otevřít dveře a tajemství zůstává skryto."
            )
        ]

        for i, encounter in enumerate(encounters):
            encounter.execute(self.player)
            print(f"\nPo encounteru {i + 1} následuje kvíz.")
            self.kviz.spustit(i)

        sifrovane_zpravy = [
            "TAJNA ZPRAVA VE SKRINI",
            "DALSI ZPRAVA U DRUHÝCH DVEŘÍ",
            "KLÍČ JE V KNIHOVNĚ",
            "TAJEMSTVÍ UKRYTO ZA OBRAZEM"
        ]

        for zprava in sifrovane_zpravy:
            self.sifrovat_a_desifrovat(zprava)

        print("\n*** Konec hry ***")
        print("Děkujeme za hraní. Doufáme, že se vám hra líbila a brzy si ji zahrajete znovu!")

if __name__ == "__main__":
    hra = Game()
    hra.play()