def bmi_rechner():
    gewicht = float(input("Gib dein Gewicht in kg an: "))
    groesse = float(input("Gib deine Größe in cm an: "))
    bmi = gewicht / ((groesse / 100) ** 2)
    print("Dein BMI ist:", bmi)

    if bmi < 18.5:
        return 'Das kritisch bro!'
    elif 18.5 <= bmi < 25:
        return 'Allet jut bro!'
    elif bmi >= 25:
        return 'Viel zu fett bro!'
    
    menu()

def BMR_Rechner_m():
    gewicht = float(input("Gib dein Gewicht in kg an: "))
    groesse = float(input("Gib deine Groesse in cm an: "))
    alter = int(input("Gib dein Alter in Jahren an:  "))
    bmr = 88.36 + (13.34 * gewicht) + (4.8 * groesse) - (5.7 * alter)
    print("Dein BMR ist: ", bmr, "\n")
    return bmr

def BMR_Rechner_w():
    gewicht = float(input("Gib dein Gewicht in kg an: "))
    groesse = float(input("Gib deine Groesse in cm an: "))
    alter = int(input("Gib dein Alter in Jahren an:  "))
    bmr = 447.6 + (9.2 * gewicht) + (3.1 * groesse) - (4.3 * alter)
    print("Dein BMR ist: ", bmr, "\n")
    return bmr

def cardio_fitness_m():
    Max_heart_rate = int(input("Gib deine maximale Herzfrequenz an: "))
    resting_heart_rate = int(input("Gib deine Ruheherzfrequenz an: "))
    VO2_max = 15.3 * (Max_heart_rate / resting_heart_rate)
    print(f"Deine cardiorespirary fittness ist: {VO2_max}\n")

    wahl = input("Bist du ein Mann oder eine Frau? (m/w): ")
    if wahl == "m":
        if VO2_max >= 42 and VO2_max <= 60:
            print("Du bist Fit bro!\n")
        elif VO2_max < 42:
            print("Kritisch bra, such bitte einen Arzt auf!\n")
        elif VO2_max > 60:
            print("Du bist eine Maschine!\n")
    elif wahl == "w":
        if VO2_max >= 38 and VO2_max <= 56:
            print("Du bist eine Maschine!\n")
        elif VO2_max < 38:
            print("Kritisch bra, such bitte einen Arzt auf!\n")
        elif VO2_max > 56:
            print("Du bist eine Maschine!\n")
    menu()


def menu():
    print("Willkommen zum Gesundheitsrechner!")
    print("Drücke 1 für BMI Rechner")
    print("Drücke 2 für BMR Rechner")
    print("Drücke 3 für Cardio Fitness Rechner")
    print("Drücke q um zu beenden")

    while True:
        wahl = input("Deine Wahl: ")
        if wahl == "1":
            ergebnis = bmi_rechner()
            print(ergebnis)
        elif wahl == "2":
            geschlecht = input("Bist du männlich oder weiblich? (m/w): ")
            if geschlecht == "m":
                bmr_erg = BMR_Rechner_m()
                print("Du kannst deinen BMR weiterverwenden:", bmr_erg)
            elif geschlecht == "w":
                bmr_erg = BMR_Rechner_w()
                print("Du kannst deinen BMR weiterverwenden:", bmr_erg)
            else:
                print("Ungültige Eingabe. Bitte 'm' für männlich oder 'w' für weiblich eingeben.")
        elif wahl == "3":
            cardio_fitness_m()
        elif wahl == "q":
            print("Rechner wird beendet. Auf Wiedersehen!")
            break
        else:
            print("Ungültige Eingabe.")




menu()