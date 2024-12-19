import warnings as w
from random import choice
import os
import numpy as np

class SifrovaciStrojEnigma:
    """
    Třída simulující šifrovací stroj Enigma s funkcionalitou pro zpracování textových souborů.
    """

    def __init__(self, propojovaci_deska=None, rotory=None, reflektor=None):
        """
        Inicializuje šifrovací stroj Enigma s propojovací deskou, rotory a reflektorem.

        :param propojovaci_deska: Slovník reprezentující propojení na propojovací desce.
        :param rotory: Seznam slovníků reprezentujících rotory.
        :param reflektor: Slovník reprezentující reflektor.
        """
        self.abeceda = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.propojovaci_deska = propojovaci_deska or {
            'A': 'M', 'B': 'C', 'C': 'B', 'D': 'F', 'E': 'Z', 'F': 'D', 'G': 'J', 'H': 'O',
            'I': 'L', 'J': 'G', 'K': 'W', 'L': 'I', 'M': 'A', 'N': 'S', 'O': 'H', 'P': 'U',
            'Q': 'V', 'R': 'X', 'S': 'N', 'T': 'Y', 'U': 'P', 'V': 'Q', 'W': 'K', 'X': 'R',
            'Y': 'T', 'Z': 'E'
        }
        self.rotory = rotory or [
            {'A': 'A', 'B': 'J', 'C': 'D', 'D': 'K', 'E': 'S', 'F': 'I', 'G': 'R', 'H': 'U',
             'I': 'X', 'J': 'B', 'K': 'L', 'L': 'H', 'M': 'W', 'N': 'T', 'O': 'M', 'P': 'C',
             'Q': 'Q', 'R': 'G', 'S': 'Z', 'T': 'N', 'U': 'P', 'V': 'Y', 'W': 'F', 'X': 'V',
             'Y': 'O', 'Z': 'E'}
        ]
        self.reflektor = reflektor or {
            'A': 'Y', 'B': 'R', 'C': 'U', 'D': 'H', 'E': 'Q', 'F': 'S', 'G': 'L', 'H': 'D',
            'I': 'P', 'J': 'X', 'K': 'N', 'L': 'G', 'M': 'O', 'N': 'K', 'O': 'M', 'P': 'I',
            'Q': 'E', 'R': 'B', 'S': 'F', 'T': 'Z', 'U': 'C', 'V': 'W', 'W': 'V', 'X': 'J',
            'Y': 'A', 'Z': 'T'
        }
        self.otoceni_rotoru = [0] * len(self.rotory)
        self.desifrovana_slova = set()

    def spustit_propojovaci_desku(self, znak: str, obracene: bool = False) -> str:
        """
        Zpracuje znak přes propojovací desku.

        :param znak: Znak k zpracování.
        :param obracene: True, pokud se má zpracování provést obráceně.
        :return: Zpracovaný znak.
        """
        if not obracene:
            return self.propojovaci_deska.get(znak, znak)
        else:
            return list(self.propojovaci_deska.keys())[list(self.propojovaci_deska.values()).index(znak)] if znak in self.propojovaci_deska.values() else znak

    def spustit_rotory(self, znak: str) -> str:
        """
        Zpracuje znak přes rotory a reflektor.

        :param znak: Znak k zpracování.
        :return: Zpracovaný znak.
        """
        for rotor in self.rotory:
            znak = rotor.get(znak, znak)
        znak = self.reflektor.get(znak, znak)
        for rotor in reversed(self.rotory):
            znak = list(rotor.keys())[list(rotor.values()).index(znak)] if znak in rotor.values() else znak
        return znak

    def zasifrovat_znak(self, znak: str, obracene: bool = False) -> str:
        """
        Zašifruje nebo dešifruje jeden znak.

        :param znak: Znak k šifrování/dešifrování.
        :param obracene: True, pokud se má znak dešifrovat.
        :return: Zašifrovaný nebo dešifrovaný znak.
        """
        znak = self.spustit_propojovaci_desku(znak, obracene)
        znak = self.spustit_rotory(znak)
        znak = self.spustit_propojovaci_desku(znak, obracene)
        return znak

    def desifrovat_slovo(self, slovo: str) -> str:
        """
        Dešifruje jedno slovo.

        :param slovo: Slovo k dešifrování.
        :return: Dešifrované slovo.
        """
        desifrovane_slovo = ""
        for znak in slovo:
            if znak in self.abeceda:
                desifrovany_znak = self.zasifrovat_znak(znak, obracene=True)
                desifrovane_slovo += desifrovany_znak
            else:
                desifrovane_slovo += znak
        return desifrovane_slovo.lower()

    def zpracovat_textovy_soubor(self, cesta_souboru: str, procento: int, vystupni_cesta: str) -> None:
        """
        Zpracuje textový soubor, částečně dešifruje zadané procento slov a uloží výstup.

        :param cesta_souboru: Cesta k vstupnímu souboru.
        :param procento: Procento velkých slov, která mají být dešifrována.
        :param vystupni_cesta: Cesta k výstupnímu souboru.
        """
        if not os.path.isfile(cesta_souboru):
            raise FileNotFoundError(f"Soubor '{cesta_souboru}' neexistuje!")

        with open(cesta_souboru, "r", encoding="utf-8") as soubor:
            text = soubor.read()

        slova = text.split()

        zasifrovana_slova = [slovo for slovo in slova if slovo.isupper()]
        pocet_desifrovat = int(len(zasifrovana_slova) * (procento / 100))
        slova_k_desifrovani = [slovo for slovo in zasifrovana_slova if slovo not in self.desifrovana_slova]
        vybrana_slova = np.random.choice(slova_k_desifrovani, min(len(slova_k_desifrovani), pocet_desifrovat), replace=False)

        for slovo in vybrana_slova:
            desifrovane_slovo = self.desifrovat_slovo(slovo)
            text = text.replace(slovo, desifrovane_slovo, 1)
            self.desifrovana_slova.add(slovo)

        with open(vystupni_cesta, "w", encoding="utf-8") as soubor:
            soubor.write(text)

        print(f"Částečně dešifrovaný text uložen do '{vystupni_cesta}'.")