# Notenrechner – Einfachste Version mit Erklärungen

# Alle möglichen Notenstufen in einer Liste.
# Listen = Sammlung von Werten in Reihenfolge.
STUFEN = ["1.0", "1.7", "2.3", "3.0", "3.7", "5.0"]


def note(points, late, cheated, bonus):
    # Wenn betrogen wurde → automatisch 5.0, egal wie viele Punkte
    if cheated:
        return "5.0"

    # Grundnote nach Punkten bestimmen
    if points >= 92:
        i = 0   # Index 0 → "1.0"
    elif points >= 85:
        i = 1   # Index 1 → "1.7"
    elif points >= 78:
        i = 2   # Index 2 → "2.3"
    elif points >= 70:
        i = 3   # Index 3 → "3.0"
    elif points >= 60:
        i = 4   # Index 4 → "3.7"
    else:
        i = 5   # Index 5 → "5.0"

    # Zu spät? → eine Stufe schlechter (Index +1)
    if late:
        i += 1

    # Bonusaufgabe bestanden und Punkte >= 70? → eine Stufe besser (Index -1)
    if bonus and points >= 70:
        i -= 1

    # Absicherung: Index darf nicht kleiner als 0 oder größer als letzte Stufe sein
    if i < 0:
        i = 0
    if i >= len(STUFEN):  # len(x) gibt die Länge zurück (hier: wie viele Noten in STUFEN sind)
        i = len(STUFEN) - 1  # letzter Index = Länge - 1

    return STUFEN[i]


def main():
    ergebnisse = {}  # Dictionary: Name → Note
    noten = []       # Liste aller Noten (als Zahl, z. B. 1.0 oder 3.7)

    while True:
        # Namen abfragen
        name = input("Name (stop zum Beenden): ").strip()
        if name.lower() == "stop":
            break  # Schleife beenden

        # Punkte abfragen (ohne Fehlerprüfung für Anfänger)
        p = float(input("Punkte (0-100): "))

        # Eingaben zu ja/nein Fragen
        late = input("Zu spät? (ja/nein): ").strip().lower() == "ja"
        cheated = input("Betrogen? (ja/nein): ").strip().lower() == "ja"
        bonus = input("Bonus bestanden? (ja/nein): ").strip().lower() == "ja"

        # Note berechnen
        n = note(p, late, cheated, bonus)

        # Ergebnis speichern
        ergebnisse[name] = n
        noten.append(float(n))  # Noten als Zahl für Statistik (z. B. "1.7" → 1.7)

        print(f"=> {name}: {n}\n")

    # Wenn keine Noten eingegeben wurden → abbrechen
    if not noten:
        print("Keine Daten.")
        return

    # Übersicht aller Ergebnisse
    print("\n--- Übersicht ---")
    for k in sorted(ergebnisse):  # sorted() = alphabetisch sortieren
        print(f"{k}: {ergebnisse[k]}")

    # Statistik
    print("\n--- Statistik ---")
    print(f"Beste: {min(noten):.1f}")        # min() = kleinster Wert in der Liste (beste Note)
    print(f"Schlechteste: {max(noten):.1f}") # max() = größter Wert in der Liste (schlechteste Note)
    print(f"Durchschnitt: {sum(noten)/len(noten):.2f}") 
    # sum() = alle Werte addieren
    # len() = Anzahl der Elemente in der Liste
    # → Durchschnitt = Summe / Anzahl

    print(f"Bestanden: {sum(1 for x in noten if x != 5.0)} von {len(noten)}")
    # sum(1 for x in noten if x != 5.0) = zählt, wie viele Noten nicht 5.0 sind


if __name__ == "__main__":
    main()
