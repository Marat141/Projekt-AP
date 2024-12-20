import random
 
# Definice rolí a jejich statistik
roles = {
    "Elektrikář": {"HP": 125, "Money": 50, "Strength": 10, "Dexterity": 8, "Charisma": 10, "Intelligence": 8},
    "IT specialista": {"HP": 100, "Money": 50, "Strength": 8, "Dexterity": 6, "Charisma": 10, "Intelligence": 12},
    "Telekomunikační technik": {"HP": 75, "Money": 50, "Strength": 6, "Dexterity": 8, "Charisma": 12, "Intelligence": 10},
    "Zahradník": {"HP": 150, "Money": 50, "Strength": 12, "Dexterity": 10, "Charisma": 8, "Intelligence": 6}
}
 
player = {}
player_inventory = []  # Seznam hráčových předmětů
 
# Funkce pro výběr postavy
def select_role():
    print("\n*** Začíná dobrodružství ***\n")
    print("Jsi student na střední škole, která skrývá mnoho tajemství. Povídá se, že někde ve škole je ukrytý **Tajný deník**, obsahující odpovědi na testy, přezdívky učitelů a další tajnosti.")
    print("Nejprve si vyber svou roli, která určí tvé schopnosti:\n")
    for idx, role in enumerate(roles.keys(), 1):
        print(f"{idx}. {role}")
    while True:
        try:
            choice = int(input("\nZadej číslo své volby: "))
            if 1 <= choice <= len(roles):
                selected_role = list(roles.keys())[choice - 1]
                print(f"\nVybral/a jsi: {selected_role}\n")
                return selected_role
            else:
                print("Neplatná volba. Zkus to znovu.")
        except ValueError:
            print("Zadej platné číslo.")
 
# Funkce pro hody kostkou
def roll_dice(skill_bonus=0):
    return random.randint(1, 20) + skill_bonus
 
# Funkce pro zobrazení inventáře
def show_inventory():
    print("\n*** Inventář ***")
    print(f"Role: {player['Role']}")
    print(f"HP: {player['HP']}")
    print(f"Peníze: {player['Money']} KČ")
    print("Předměty:")
    if player_inventory:
        for idx, item in enumerate(player_inventory, 1):
            print(f"  {idx}. {item}")
    else:
        print("  (Inventář je prázdný.)")
    print("\n")
 
# Funkce pro obchodníka
def obchodnik():
    print("\n*** Příchod obchodníka ***")
    print("Mistr Šifrant se zjeví s tajemným úsměvem. Nabízí své zboží za peníze.")
    items = [
        {"name": "Malá nápověda", "cost": 100, "effect": "Snižuje obtížnost jednoho skill-checku o 2."},
        {"name": "Zlatý klíč", "cost": 200, "effect": "Otevře jednu část šifry automaticky."},
        {"name": "Amulet síly", "cost": 150, "effect": "Přidává +2 k hodům na sílu do dalšího encounteru."},
        {"name": "Tajemný kompas", "cost": 150, "effect": "Odhalí lokaci další části šifry."}
    ]
    
    while True:
        print("\nNabídka obchodníka:")
        for idx, item in enumerate(items, 1):
            print(f"{idx}. {item['name']} - {item['cost']} KČ ({item['effect']})")
        print(f"{len(items)+1}. Pokračovat bez nákupu.")
        
        try:
            choice = int(input(f"\nVyber položku k nákupu (nebo zadej {len(items)+1} pro pokračování): ")) - 1
            
            if choice == len(items):
                print("Pokračuješ bez nákupu.")
                break
            elif 0 <= choice < len(items):
                item = items[choice]
                if player["Money"] >= item["cost"]:
                    player["Money"] -= item["cost"]
                    player_inventory.append(item["name"])
                    print(f"Koupil/a jsi {item['name']}. {item['effect']}")
                else:
                    print("Nemáš dost peněz na tento předmět.")
            else:
                print("Neplatná volba. Zkus to znovu.")
        except ValueError:
            print("Zadej platné číslo.")
 
# Funkce pro encounter
def encounter(description, choices, required_role, success_story, fail_story):
    print(description)
    for idx, choice in enumerate(choices, 1):
        print(f"{idx}. {choice['text']}")
    
    while True:
        action = input("\nVyber akci (zadej číslo nebo napiš 'inventář' pro zobrazení inventáře): ").strip().lower()
        if action == "inventář":
            show_inventory()
            continue
        try:
            choice = int(action) - 1
            if 0 <= choice < len(choices):
                role_bonus = -2 if player["Role"] == required_role else 2
                result = roll_dice(choices[choice]["bonus"] - role_bonus)
                
                print(f"\nHodil jsi: {result} (po bonusu)")
                
                if result >= choices[choice]["success_roll"]:
                    print(choices[choice]["success_text"])
                    player["HP"] += choices[choice].get("hp_change", 0)
                    player["Money"] += choices[choice].get("money_change", 0)
                    if "item" in choices[choice]:
                        player_inventory.append(choices[choice]["item"])
                        print(f"Do inventáře přidán předmět: {choices[choice]['item']}")
                    print(f"\n{success_story}\n")
                    obchodnik()
                    return True
                else:
                    print(choices[choice]["fail_text"])
                    player["HP"] += choices[choice].get("hp_change_fail", 0)
                    player["Money"] += choices[choice].get("money_change_fail", 0)
                    print(f"\n{fail_story}\n")
                    obchodnik()
                    return False
            else:
                print("Neplatná volba. Zkus to znovu.")
        except ValueError:
            print("Zadej platné číslo nebo 'inventář'.")
 
# Kapitoly a encountery
def encounter_1():
    description = """
*** Kapitola 1: Tajemné dráty ***
 
Procházíš chodbou, když si všimneš visících měděných drátů ze stropu.
Nikde není žádný školník, a tak tě napadá, že bys mohl situaci využít.
Co uděláš?
    """
    required_role = "Elektrikář"
    choices = [
        {
            "text": "Rozebereš dráty a prodáš je na bleším trhu.",
            "bonus": 3,
            "success_roll": 10,
            "success_text": "Dráty jsi bezpečně odmontoval a prodal za 100 KČ.",
            "fail_text": "Při pokusu jsi dostal ránu proudem, -5 HP.",
            "money_change": 100,
            "hp_change_fail": -5
        },
        {
            "text": "Zavoláš Lakatošovi, aby je rozebral místo tebe.",
            "bonus": 0,
            "success_roll": 15,
            "success_text": "Lakatoš ti zaplatil 30 KČ.",
            "fail_text": "Lakatoš tě okradl, nezískal jsi nic.",
            "money_change": 30,
            "money_change_fail": 0
        },
        {
            "text": "Odejdi bez pokusu a pokračuj dál.",
            "bonus": 0,
            "success_roll": 0,
            "success_text": "Dráty jsi nechal na místě, nic se nestalo.",
            "fail_text": "Nic jsi nezískal, ale jsi v bezpečí."
        }
    ]
    success_story = "Využil jsi situaci na maximum a získal jsi další stopu, která tě vede do IT učebny."
    fail_story = "Tvé selhání způsobilo ztrátu času, ale rozhodl ses pokračovat dál s nadějí na lepší příležitosti."
    encounter(description, choices, required_role, success_story, fail_story)
 
def encounter_2():
    description = """
*** Kapitola 2: Zamčená učebna IT ***
 
Dorazil/a jsi do učebny IT, která je zamčená. Potřebuješ se dostat dovnitř, protože další stopa se nachází právě tady.
    """
    required_role = "IT specialista"
    choices = [
        {
            "text": "Pokoušíš se hacknout elektronický zámek.",
            "bonus": 3,
            "success_roll": 12,
            "success_text": "Zámek se otevřel a dostal/a ses dovnitř!",
            "fail_text": "Zámek jsi zablokoval/a. Přijde školník!",
            "money_change_fail": -10
        },
        {
            "text": "Hledáš klíč v kabinetu učitelů.",
            "bonus": 2,
            "success_roll": 10,
            "success_text": "Našel/a jsi klíč a odemkl/a učebnu.",
            "fail_text": "Klíč nebyl nikde k nalezení. Ztratil/a jsi drahocenný čas."
        },
        {
            "text": "Vykašleš se na to a zkusíš to později.",
            "bonus": 0,
            "success_roll": 0,
            "success_text": "Rozhodl/a ses, že to zkusíš později.",
            "fail_text": "Nic se nestalo. Ztrácíš čas."
        }
    ]
    success_story = "Dostal/a ses do učebny IT a našel/a další vodítko!"
    fail_story = "Nepodařilo se ti dostat dovnitř. Ztratil/a jsi čas, ale musíš pokračovat dál."
    encounter(description, choices, required_role, success_story, fail_story)
 
def encounter_3():
    description = """
*** Kapitola 3: Knihovna a tajný kód ***
 
Knihovna skrývá tajný kód, který tě přivede blíže k deníku. Musíš najít správnou knihu nebo sebrat odvahu a prohledat místnost.
    """
    required_role = "Telekomunikační technik"
    choices = [
        {
            "text": "Prohledáš všechny knihy.",
            "bonus": 3,
            "success_roll": 12,
            "success_text": "Našel/a jsi tajný kód zapsaný na okraji jedné z knih!",
            "fail_text": "Knihy byly příliš mnohé. Nic jsi nenašel/a.",
        },
        {
            "text": "Hledáš pomoc od knihovníka.",
            "bonus": 2,
            "success_roll": 10,
            "success_text": "Knihovník ti ukázal správnou knihu. Našel/a jsi kód!",
            "fail_text": "Knihovník tě ignoroval. Ztratil/a jsi čas."
        },
        {
            "text": "Prozkoumáš místnost a hledáš jiná vodítka.",
            "bonus": 0,
            "success_roll": 8,
            "success_text": "Našel/a jsi tajný sejf, ale potřebuješ ho otevřít.",
            "fail_text": "Nic jsi nenašel/a a jen ztrácíš čas."
        }
    ]
    success_story = "Podařilo se ti najít tajný kód a posunout se blíže k deníku!"
    fail_story = "Nenašel/a jsi nic užitečného, ale neztrácíš naději."
    encounter(description, choices, required_role, success_story, fail_story)
 
def encounter_4():
    description = """
*** Kapitola 4: Deník na dosah ***
 
Dorazil/a jsi k tajné místnosti, kde je ukrytý deník. Musíš překonat finální překážky, abys získal/a svůj cíl.
    """
    required_role = "Zahradník"
    choices = [
        {
            "text": "Zkusíš odemknout tajnou místnost pomocí šifry.",
            "bonus": 3,
            "success_roll": 15,
            "success_text": "Šifra byla úspěšně prolomena! Deník je tvůj!",
            "fail_text": "Šifra byla příliš složitá. Nepodařilo se ti otevřít místnost."
        },
        {
            "text": "Zkusíš najít jiný způsob, jak místnost otevřít.",
            "bonus": 2,
            "success_roll": 12,
            "success_text": "Našel/a jsi tajný mechanismus. Místnost se otevřela!",
            "fail_text": "Nic jsi nenašel/a. Místnost zůstává zavřená."
        },
        {
            "text": "Hledáš pomoc od ostatních studentů.",
            "bonus": 1,
            "success_roll": 10,
            "success_text": "Studenti ti pomohli a společně jste získali deník!",
            "fail_text": "Nikdo ti nepomohl. Zůstáváš v pasti."
        }
    ]
    success_story = "Získal/a jsi deník a odhalil/a všechny jeho tajemství!"
    fail_story = "Nepodařilo se ti získat deník. Tajemství školy zůstává neodhalené."
    encounter(description, choices, required_role, success_story, fail_story)
 
# Hlavní funkce
def main():
    print("Vítejte v textextové adventuře!")
    selected_role = select_role()
    player.update({"Role": selected_role, **roles[selected_role]})
    print(f"\nVybral/a jsi roli: {player['Role']}.\n")
    
    # Kapitoly
    encounter_1()
    encounter_2()
    encounter_3()
    encounter_4()
    
    print("\n*** Konec hry ***")
    print("Děkujeme za hraní. Doufáme, že sis hru užil/a!")
 
if __name__ == "__main__":
    main()