import random

class Role:
    def __init__(self, name, hp, money, strength, dexterity, charisma, intelligence):
        self.name = name
        self.hp = hp
        self.money = money
        self.stats = {
            "Strength": strength,
            "Dexterity": dexterity,
            "Charisma": charisma,
            "Intelligence": intelligence
        }

class Character:
    def __init__(self, role):
        self.role = role
        self.hp = role.hp
        self.money = role.money
        self.inventory = []

    def display_stats(self):
        print(f"Role: {self.role.name}")
        print(f"HP: {self.hp}")
        print(f"Money: {self.money} KČ")
        print("Stats:")
        for stat, value in self.role.stats.items():
            print(f"  {stat}: {value}")
        print("Inventory:")
        if self.inventory:
            for idx, item in enumerate(self.inventory, 1):
                print(f"  {idx}. {item}")
        else:
            print("  (Inventory is empty)")

    def add_item(self, item):
        self.inventory.append(item)
        print(f"Item added to inventory: {item}")

    def modify_money(self, amount):
        self.money += amount
        print(f"Money updated. Current balance: {self.money} KČ")

    def modify_hp(self, amount):
        self.hp = max(self.hp + amount, 0)
        print(f"HP updated. Current HP: {self.hp}")

class Encounter:
    def __init__(self, description, choices, required_role, success_story, fail_story):
        self.description = description
        self.choices = choices
        self.required_role = required_role
        self.success_story = success_story
        self.fail_story = fail_story

    def play(self, character):
        print(self.description)
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice['text']}")

        while True:
            action = input("\nChoose an action (or type 'inventory' to view your inventory): ").strip().lower()
            if action == "inventory":
                character.display_stats()
                continue
            try:
                choice = int(action) - 1
                if 0 <= choice < len(self.choices):
                    role_bonus = -2 if character.role.name == self.required_role else 2
                    result = random.randint(1, 20) + self.choices[choice]["bonus"] - role_bonus
                    
                    print(f"\nYou rolled: {result} (after bonuses)")

                    if result >= self.choices[choice]["success_roll"]:
                        print(self.choices[choice]["success_text"])
                        character.modify_hp(self.choices[choice].get("hp_change", 0))
                        character.modify_money(self.choices[choice].get("money_change", 0))
                        if "item" in self.choices[choice]:
                            character.add_item(self.choices[choice]["item"])
                        print(f"\n{self.success_story}\n")
                        return True
                    else:
                        print(self.choices[choice]["fail_text"])
                        character.modify_hp(self.choices[choice].get("hp_change_fail", 0))
                        character.modify_money(self.choices[choice].get("money_change_fail", 0))
                        print(f"\n{self.fail_story}\n")
                        return False
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Enter a valid number or type 'inventory'.")

# Define roles
roles = {
    "Elektrikář": Role("Elektrikář", 125, 50, 10, 8, 10, 8),
    "IT specialista": Role("IT specialista", 100, 50, 8, 6, 10, 12),
    "Telekomunikační technik": Role("Telekomunikační technik", 75, 50, 6, 8, 12, 10),
    "Zahradník": Role("Zahradník", 150, 50, 12, 10, 8, 6)
}

# Example Encounters
def encounter_1():
    description = """
    *** Encounter 1: Měděné dráty ***

    Procházíš chodbou a vidíš měděné dráty visící ze stropu.
    Co uděláš?
    """
    choices = [
        {
            "text": "Rozebereš dráty a prodáš je.",
            "bonus": 3,
            "success_roll": 10,
            "success_text": "Úspěšně jsi prodal dráty a získal 100 KČ.",
            "fail_text": "Dostal jsi ránu elektrickým proudem. -5 HP.",
            "money_change": 100,
            "hp_change_fail": -5
        },
        {
            "text": "Zavoláš Lakatoše, aby je rozebral.",
            "bonus": 0,
            "success_roll": 15,
            "success_text": "Lakatoš ti zaplatil 30 KČ.",
            "fail_text": "Lakatoš tě okradl. Nic jsi nezískal.",
            "money_change": 30
        },
        {
            "text": "Necháš dráty být.",
            "bonus": 0,
            "success_roll": 0,
            "success_text": "Neudělal jsi nic, ale jsi v bezpečí.",
            "fail_text": "Nic jsi nezískal.",
        }
    ]
    return Encounter(description, choices, "Elektrikář", "Získal jsi další stopu k deníku.", "Ztratil jsi čas, ale pokračuješ dál.")

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
    return Encounter(description, choices, required_role, success_story, fail_story)

# Main Function
def main():
    print("Welcome to the Adventure Game!")
    print("Choose your role:")

    for idx, role_name in enumerate(roles.keys(), 1):
        print(f"{idx}. {role_name}")

    while True:
        try:
            choice = int(input("\nEnter the number of your choice: ")) - 1
            if 0 <= choice < len(roles):
                selected_role = list(roles.values())[choice]
                break
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Enter a valid number.")

    player = Character(selected_role)
    player.display_stats()

    # Play encounters
    encounter = encounter_1()
    encounter.play(player)

    print("\nGame Over. Thank you for playing!")

if __name__ == "__main__":
    main()
