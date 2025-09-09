# Tower of Power - Pseudo OS Simulation

import time

# Liste der Befehle im Ablauf
commands = [
    "select (gerade mit Loch)",
    "move down",
    "grip",
    "move up",
    "move right (3)",
    "move down",
    "release",
    "status 2/3",
    "select (schräg mit Loch)",
    "move down",
    "grip",
    "move up",
    "move right (20)",
    "move forward (3)",
    "move down",
    "release",
    "status 3/3 – FINISH"
]

def execute_command(cmd):
    """Simuliert die Ausführung eines Befehls"""
    print(f"> {cmd}")
    time.sleep(0.5)  # kleine Pause, damit es nach "System" aussieht
    if cmd.startswith("status"):
        print(f"= {cmd}")  # Status wird direkt ausgegeben
    else:
        print("= ok")

def main():
    print("=== Tower of Power OS Simulation gestartet ===")
    for cmd in commands:
        execute_command(cmd)
    print("=== Ende des Protokolls ===")

if __name__ == "__main__":
    main()
