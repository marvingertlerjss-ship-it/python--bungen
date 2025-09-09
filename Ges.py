# Geschwindigkeit = (Dateigröße in Bytes) / (Zeit in Sekunden)
#try-except else finally Block

def geschwindigkeitsrechner():
    try:
        dateigroesse = float(input("Gib die Dateigröße in MB an: "))
        zeit = float(input("Gib die Zeit in Sekunden an: "))
        geschwindigkeit = (dateigroesse * 8) / zeit 
    except ValueError:
        print("Das war keine Zahl! ")
    else:
        print(f"Die Geschwindigkeit beträgt: {geschwindigkeit} Mbit/s")
    finally:
        print("Ende! ")

geschwindigkeitsrechner()






