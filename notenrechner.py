#Notenrechner

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


def namensliste():
    namen = []
    while True:
        name = input("Gib einen Namen der du einer Note zuordnen willst (oder 'stop' zum Beenden): ")
        if name.lower() == 'stop':
            break
        namen.append(name)
        print("Notenberechnung für:", name)

        Notenrechnechner()

    return namen

def main():
    print("Willkommen zum Notenrechner!")
    print("Was möchtest du tun?")
    print("1. Noten für eine Person berechnen")
    print("2. Personen mit Note anzeigen")
    wahl = input("Gib 1 oder 2 ein: ")
    if wahl == '1':
        Notenrechnechner()
    elif wahl == '2':
        namen = namensliste()
        print("Namen der Personen, für die Noten berechnet wurden:")
        for name in namen:
            print(name)

main()
    
