# bmi_rechner.py
def berechne_bmi(gewicht_kg, groesse_m):
    """Berechnet den Body Mass Index"""  # Bezug: 4.1 - Docstring
    bmi = gewicht_kg / (groesse_m ** 2)  # Bezug: 1.3 - Arithmetik
    return round(bmi, 1)  # Bezug: 4.2 - return

def bmi_kategorie(bmi):
    """Bestimmt die BMI-Kategorie"""
    if bmi < 18.5:  # Bezug: 2.1 - Verzweigung
        return "Untergewicht"
    elif bmi < 25:
        return "Normalgewicht"
    elif bmi < 30:
        return "Übergewicht"
    else:
        return "Adipositas"

# Testberechnung
patient_gewicht = 75  # Bezug: 1.1 - int
patient_groesse = 1.75  # Bezug: 1.1 - float
ergebnis = berechne_bmi(patient_gewicht, patient_groesse)
print(f"BMI: {ergebnis}")  # Bezug: 3.2 - f-String
print(f"Kategorie: {bmi_kategorie(ergebnis)}")
