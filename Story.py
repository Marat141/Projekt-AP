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

class Merchant:
    def __init__(self):
        self.items = [
            {"name": "Malá nápověda", "cost": 100, "effect": "Snižuje obtížnost jednoho skill-checku o 2."},
            {"name": "Zlatý klíč", "cost": 200, "effect": "Otevře jednu část šifry automaticky."},
            {"name": "Amulet síly", "cost": 150, "effect": "Přidává +2 k hodům na sílu do dalšího encounteru."},
            {"name": "Tajemný kompas", "cost": 150, "effect": "Odhalí lokaci další části šifry."}
        ]

    def trade(self, player):
        print("\n*** Příchod obchodníka ***")
        print("Mistr Šifrant se zjeví s tajemným úsměvem. Nabízí své zboží za peníze.")
        while True:
            print("\nNabídka obchodníka:")
            for idx, item in enumerate(self.items, 1):
                print(f"{idx}. {item['name']} - {item['cost']} KČ ({item['effect']})")
            print(f"{len(self.items) + 1}. Pokračovat bez nákupu.")

            try:
                choice = int(input(f"\nVyber položku k nákupu (nebo zadej {len(self.items) + 1} pro pokračování): ")) - 1

                if choice == len(self.items):
                    print("Pokračuješ bez nákupu.")
                    break
                elif 0 <= choice < len(self.items):
                    item = self.items[choice]
                    if player.money >= item["cost"]:
                        player.adjust_money(-item["cost"])
                        player.add_item(item["name"])
                        print(f"Koupil/a jsi {item['name']}. {item['effect']}")
                    else:
                        print("Nemáš dost peněz na tento předmět.")
                else:
                    print("Neplatná volba. Zkus to znovu.")
            except ValueError:
                print("Zadej platné číslo.")

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

class Game:
    def __init__(self):
        self.roles = {
            "Elektrikář": Role("Elektrikář", 125, 50, 10, 8, 10, 8),
            "IT specialista": Role("IT specialista", 100, 50, 8, 6, 10, 12),
            "Telekomunikační technik": Role("Telekomunikační technik", 75, 50, 6, 8, 12, 10),
            "Zahradník": Role("Zahradník", 150, 50, 12, 10, 8, 6)
        }
        self.player = None
        self.merchant = Merchant()

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

    def play(self):
        print("Vítejte v textové adventuře!")
        self.select_role()

        # Definování encounterů
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
*** Kapitola 2: Zamčená učebna IT ***

Dorazil/a jsi do učebny IT, která je zamčená. Potřebuješ se dostat dovnitř, protože další stopa se nachází právě tady.
                """,
                [
                    {"text": "Pokoušíš se hacknout elektronický zámek.", "bonus": 3, "success_roll": 12, "success_text": "Zámek se otevřel a dostal/a ses dovnitř!", "fail_text": "Zámek jsi zablokoval/a. Přijde školník!", "money_change_fail": -10},
                    {"text": "Hledáš klíč v kabinetu učitelů.", "bonus": 2, "success_roll": 10, "success_text": "Našel/a jsi klíč a odemkl/a učebnu.", "fail_text": "Klíč nebyl nikde k nalezení. Ztratil/a jsi drahocenný čas."},
                    {"text": "Vykašleš se na to a zkusíš to později.", "bonus": 0, "success_roll": 0, "success_text": "Rozhodl/a ses, že to zkusíš později.", "fail_text": "Nic se nestalo. Ztrácíš čas."}
                ],
                "IT specialista",
                "Dostal/a ses do učebny IT a našel/a další vodítko!",
                "Nepodařilo se ti dostat dovnitř. Ztratil/a jsi čas, ale musíš pokračovat dál."
            ),
            Encounter(
                """
*** Kapitola 3: Knihovna a tajný kód ***

Knihovna skrývá tajný kód, který tě přivede blíže k deníku. Musíš najít správnou knihu nebo sebrat odvahu a prohledat místnost.
                """,
                [
                    {"text": "Prohledáš všechny knihy.", "bonus": 3, "success_roll": 12, "success_text": "Našel/a jsi tajný kód zapsaný na okraji jedné z knih!", "fail_text": "Knihy byly příliš mnohé. Nic jsi nenašel/a."},
                    {"text": "Hledáš pomoc od knihovníka.", "bonus": 2, "success_roll": 10, "success_text": "Knihovník ti ukázal správnou knihu. Našel/a jsi kód!", "fail_text": "Knihovník tě ignoroval. Ztratil/a jsi čas."},
                    {"text": "Prozkoumáš místnost a hledáš jiná vodítka.", "bonus": 0, "success_roll": 8, "success_text": "Našel/a jsi tajný sejf, ale potřebuješ ho otevřít.", "fail_text": "Nic jsi nenašel/a a jen ztrácíš čas."}
                ],
                "Telekomunikační technik",
                "Podařilo se ti najít tajný kód a posunout se blíže k deníku!",
                "Nenašel/a jsi nic užitečného, ale neztrácíš naději."
            ),
            Encounter(
                """
*** Kapitola 4: Deník na dosah ***

Dorazil/a jsi k tajné místnosti, kde je ukrytý deník. Musíš překonat finální překážky, abys získal/a svůj cíl.
                """,
                [
                    {"text": "Zkusíš odemknout tajnou místnost pomocí šifry.", "bonus": 3, "success_roll": 15, "success_text": "Šifra byla úspěšně prolomena! Deník je tvůj!", "fail_text": "Šifra byla příliš složitá. Nepodařilo se ti otevřít místnost."},
                    {"text": "Zkusíš najít jiný způsob, jak místnost otevřít.", "bonus": 2, "success_roll": 12, "success_text": "Našel/a jsi tajný mechanismus. Místnost se otevřela!", "fail_text": "Nic jsi nenašel/a. Místnost zůstává zavřená."},
                    {"text": "Hledáš pomoc od ostatních studentů.", "bonus": 1, "success_roll": 10, "success_text": "Studenti ti pomohli a společně jste získali deník!", "fail_text": "Nikdo ti nepomohl. Zůstáváš v pasti."}
                ],
                "Zahradník",
                "Získal/a jsi deník a odhalil/a všechny jeho tajemství!",
                "Nepodařilo se ti získat deník. Tajemství školy zůstává neodhalené."
            )
        ]

        for encounter in encounters:
            encounter.execute(self.player)
            self.merchant.trade(self.player)

        print("\n*** Konec hry ***")
        print("Děkujeme za hraní. Doufáme, že sis hru užil/a!")

if __name__ == "__main__":
    game = Game()
    game.play()
