#Notenrechner

from unicodedata import name


def Notenrechnechner():

    Betrug = input("Hast du betrogen? (ja): ").lower() == "ja"
    if Betrug == True:
        print("Du hast eine 5.0")
        return
    punkte = int(input("Gib die Anzahl der erreichten Punkte an (max 100pkt): "))
    late = input("Warst du zu spät? (ja): ").lower() == "ja"
    if late == True:
        punkte -= 8
        if punkte < 0:
            punkte = 0
    bonus = input("Hast du Bonuspunkte? (ja): ").lower() == "ja"
    if bonus == True:
        punkte += 10
        if punkte > 100:
            punkte = 100
    if punkte >= 92:
        print("Du hast eine 1.0")
    elif punkte >= 85:
        print("Du hast eine 1.7")
    elif punkte >= 78:
        print("Du hast eine 2.3")
    elif punkte >= 70:
        print("Du hast eine 3.0")
    elif punkte >= 60:
        print("Du hast eine 3.7")
    else:
        print("Du hast eine 5.0")
    return


def namenerstellen():
    namen = {}
    while True:
        name = input("Gib den Namen des Schülers ein:")
        if name == "stop":
            break
        note = Notenrechnechner()
        namen[name] = note
    return namen

def namenliste(namen):
    for name, note in namen.items():
        print(name, "hat die Note", note)
    return namenliste

def menu():
    feqf = 10
    

menu()