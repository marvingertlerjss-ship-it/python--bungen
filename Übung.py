liter_desinfektionmittel = float(input("Geben Sie die Menge des Desinfektionsmittels in Litern ein: "))
preis_pro_liter = 7.50
Flaschen_groesse = float(input("Geben sie deine Flaschengroese in Litern an: "))

gesamtkosten = liter_desinfektionmittel * preis_pro_liter
print(f"Gesamtkosten für Desinfektionsmittel: {gesamtkosten} Euro")

anzahl_flaschen = liter_desinfektionmittel // Flaschen_groesse
print(f"Anzahl der {Flaschen_groesse}L Flaschen:", anzahl_flaschen)

rest = liter_desinfektionmittel % Flaschen_groesse
print(f"Restmenge in Litern: {rest}")

if rest == 0:
    print("Du hast ausgenutzt braaaaaaa!")
else:
    print("Unweltsünder!")
