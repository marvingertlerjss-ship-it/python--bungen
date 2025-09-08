import pygame
import sys
import random

# Pygame initialisieren
pygame.init()

# Bildschirmeinstellungen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Grundlagen Quiz")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (200, 200, 200)
DARK_BLUE = (0, 0, 139)
DARK_GREEN = (0, 100, 0)
DARK_RED = (139, 0, 0)

# Schriftarten
title_font = pygame.font.SysFont("Arial", 40, bold=True)
menu_font = pygame.font.SysFont("Arial", 30)
question_font = pygame.font.SysFont("Arial", 24)
answer_font = pygame.font.SysFont("Arial", 20)
explanation_font = pygame.font.SysFont("Arial", 18, italic=True)
small_font = pygame.font.SysFont("Arial", 16)
stats_font = pygame.font.SysFont("Arial", 22)

# Quiz-Fragen (40 Fragen)
all_questions = [
    {
        "category": "Datentypen und Operatoren",
        "question": "Welcher Datentyp wird durch 3.14 in Python repräsentiert?",
        "answers": ["int", "str", "float", "bool"],
        "correct": 2,
        "explanation": "Zahlen mit Dezimalpunkt werden als float (Fließkommazahl) repräsentiert."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Was ist das Ergebnis von 7 // 3?",
        "answers": ["2", "2.33", "3", "1"],
        "correct": 0,
        "explanation": "Der // Operator führt eine Ganzzahldivision durch und rundet dabei ab."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Welches Schlüsselwort prüft, ob ein Wert in einer Liste enthalten ist?",
        "answers": ["exist", "has", "in", "is"],
        "correct": 2,
        "explanation": "Der 'in' Operator prüft, ob ein Element in einer Sequenz enthalten ist."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Welche Operation verändert den Wert einer Variablen direkt?",
        "answers": ["==", "+=", "!=", ">="],
        "correct": 1,
        "explanation": "Der += Operator ist eine Zuweisungsoperation, die den Wert der Variablen verändert."
    },
    {
        "category": "Datentypen and Operatoren",
        "question": "Was liefert not True?",
        "answers": ["None", "False", "0", "Error"],
        "correct": 1,
        "explanation": "Der 'not' Operator kehrt den Wahrheitswert um. not True ergibt False."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Mit welchem Operator prüft man Identität (ob zwei Objekte gleich im Speicher sind)?",
        "answers": ["==", "!=", "is", "in"],
        "correct": 2,
        "explanation": "Der 'is' Operator prüft, ob zwei Variablen auf dasselbe Objekt im Speicher verweisen."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Welche Methode hängt ein Element an eine Liste an?",
        "answers": ["add", "extend", "append", "insert"],
        "correct": 2,
        "explanation": "Die append() Methode fügt ein Element am Ende einer Liste hinzu."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Welche Methode entfernt ein Element aus einer Liste?",
        "answers": ["pop", "remove", "cut", "del"],
        "correct": 1,
        "explanation": "Die remove() Methode entfernt das erste Vorkommen eines Elements aus einer Liste."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Welche Funktion gibt den größten Wert in einer Liste zurück?",
        "answers": ["big()", "max()", "maximum()", "largest()"],
        "correct": 1,
        "explanation": "Die max() Funktion gibt das größte Element in einer iterierbaren Struktur zurück."
    },
    {
        "category": "Datentypen und Operatoren",
        "question": "Welche Schreibweise erstellt eine leere Menge (set)?",
        "answers": ["set()", "{}", "[]", "tuple()"],
        "correct": 0,
        "explanation": "set() erstellt eine leere Menge. Geschweifte Klammern {} erstellen ein leeres Dictionary."
    },
    {
        "category": "Flow Control",
        "question": "Welche Anweisung prüft eine Bedingung?",
        "answers": ["loop", "if", "def", "try"],
        "correct": 1,
        "explanation": "Die if-Anweisung prüft eine Bedingung und führt Code aus, wenn die Bedingung wahr ist."
    },
    {
        "category": "Flow Control",
        "question": "Wie schreibt man eine Verzweigung mit Alternative?",
        "answers": ["if/for", "if/else", "while/else", "def/else"],
        "correct": 1,
        "explanation": "if/else ermöglicht eine Verzweigung mit einer Alternative für den Fall, dass die Bedingung nicht zutrifft."
    },
    {
        "category": "Flow Control",
        "question": "Welche Schleife wiederholt Code solange eine Bedingung wahr ist?",
        "answers": ["for", "if", "while", "pass"],
        "correct": 2,
        "explanation": "Die while-Schleife führt Code aus, solange die angegebene Bedingung wahr ist."
    },
    {
        "category": "Flow Control",
        "question": "Mit welchem Schlüsselwort wird eine Schleife sofort beendet?",
        "answers": ["exit", "stop", "break", "quit"],
        "correct": 2,
        "explanation": "break beendet die aktuelle Schleife sofort."
    },
    {
        "category": "Flow Control",
        "question": "Welche Schleife eignet sich, um über eine Liste zu laufen?",
        "answers": ["for", "while", "do", "switch"],
        "correct": 0,
        "explanation": "Die for-Schleife ist ideal, um über Elemente einer Liste oder anderer iterierbarer Objekte zu iterieren."
    },
    {
        "category": "Flow Control",
        "question": "Welche Anweisung überspringt nur den aktuellen Schleifendurchlauf?",
        "answers": ["pass", "continue", "break", "stop"],
        "correct": 1,
        "explanation": "continue überspringt den restlichen Code des aktuellen Schleifendurchlaufs und springt zur nächsten Iteration."
    },
    {
        "category": "Flow Control",
        "question": "Was macht pass?",
        "answers": ["beendet Schleife", "überspringt nächste Iteration", "tut nichts", "löscht eine Variable"],
        "correct": 2,
        "explanation": "pass ist eine Null-Operation - sie tut nichts und wird als Platzhalter verwendet."
    },
    {
        "category": "Flow Control",
        "question": "Wie nennt man Bedingungen innerhalb von Bedingungen?",
        "answers": ["chained", "nested", "inline", "looped"],
        "correct": 1,
        "explanation": "Verschachtelte (nested) Bedingungen sind if-Anweisungen innerhalb anderer if-Anweisungen."
    },
    {
        "category": "Flow Control",
        "question": "Welches Schlüsselwort ergänzt if für mehrere Fälle?",
        "answers": ["elif", "elseif", "else if", "orif"],
        "correct": 0,
        "explanation": "elif (else if) ermöglicht die Prüfung mehrerer Bedingungen in einer if-Anweisung."
    },
    {
        "category": "Flow Control",
        "question": "Wie wird eine Endlosschleife korrekt eingeleitet?",
        "answers": ["while True:", "for True:", "loop True:", "while 1==0:"],
        "correct": 0,
        "explanation": "while True: erzeugt eine Endlosschleife, da die Bedingung immer wahr ist."
    },
    {
        "category": "Input und Output",
        "question": "Mit welcher Funktion liest man Benutzereingaben ein?",
        "answers": ["input()", "read()", "scan()", "console()"],
        "correct": 0,
        "explanation": "input() liest eine Zeile von der Standardeingabe und gibt sie als String zurück."
    },
    {
        "category": "Input und Output",
        "question": "Welche Funktion gibt Text auf der Konsole aus?",
        "answers": ["echo()", "output()", "print()", "write()"],
        "correct": 2,
        "explanation": "print() gibt Text auf der Standardausgabe (Konsole) aus."
    },
    {
        "category": "Input und Output",
        "question": "Welche Methode zum Formatieren nutzt geschweifte Klammern {}?",
        "answers": [".join()", ".format()", ".replace()", ".fill()"],
        "correct": 1,
        "explanation": "Die format()-Methode verwendet geschweifte Klammern {} als Platzhalter."
    },
    {
        "category": "Input und Output",
        "question": "Wie heißen die f-Strings in Python?",
        "answers": ["fast strings", "formatted strings", "fixed strings", "function strings"],
        "correct": 1,
        "explanation": "f-Strings (formatted string literals) ermöglichen das Einbetten von Ausdrücken in String-Literalen."
    },
    {
        "category": "Input und Output",
        "question": "Mit welchem Schlüsselwort öffnet man Dateien, sodass sie automatisch geschlossen werden?",
        "answers": ["with", "try", "using", "auto"],
        "correct": 0,
        "explanation": "Der with-Kontextmanager sorgt dafür, dass Dateien automatisch geschlossen werden."
    },
    {
        "category": "Input und Output",
        "question": "Welche Datei-Operation öffnet eine Datei zum Schreiben (überschreiben)?",
        "answers": ["r", "w", "a", "x"],
        "correct": 1,
        "explanation": "'w' (write) öffnet eine Datei zum Schreiben und überschreibt vorhandene Inhalte."
    },
    {
        "category": "Input und Output",
        "question": "Welche Methode liest den gesamten Dateiinhalt?",
        "answers": ["read()", "readline()", "scan()", "load()"],
        "correct": 0,
        "explanation": "read() liest den gesamten Inhalt einer Datei als String."
    },
    {
        "category": "Input und Output",
        "question": "Welche Methode hängt Text an eine Datei an?",
        "answers": ["w", "r", "a", "x"],
        "correct": 2,
        "explanation": "'a' (append) öffnet eine Datei zum Anhängen von Text am Ende."
    },
    {
        "category": "Input und Output",
        "question": "Welche Funktion prüft, ob eine Datei existiert?",
        "answers": ["os.path.exists()", "os.file()", "sys.exist()", "file.exists()"],
        "correct": 0,
        "explanation": "os.path.exists() prüft, ob eine Datei oder ein Verzeichnis existiert."
    },
    {
        "category": "Input und Output",
        "question": "Welcher Modus löscht eine Datei beim Öffnen, falls sie schon da ist?",
        "answers": ["a", "x", "w", "r"],
        "correct": 2,
        "explanation": "'w' (write) löscht den vorhandenen Inhalt einer Datei, falls sie existiert."
    },
    {
        "category": "Dokumentation und Struktur",
        "question": "Wie erstellt man einen Kommentar in Python?",
        "answers": ["// Kommentar", "<!-- Kommentar -->", "# Kommentar", "% Kommentar"],
        "correct": 2,
        "explanation": "Kommentare in Python beginnen mit einem #-Zeichen."
    },
    {
        "category": "Dokumentation und Struktur",
        "question": "Wie definiert man eine Funktion?",
        "answers": ["def", "func", "function", "define"],
        "correct": 0,
        "explanation": "Funktionen werden mit dem Schlüsselwort def definiert."
    },
    {
        "category": "Dokumentation und Struktur",
        "question": "Wie nennt man einen Dummy-Platzhalter in einer Funktion ohne Code?",
        "answers": ["break", "skip", "pass", "none"],
        "correct": 3,
        "explanation": "pass ist eine Null-Operation, die als Platzhalter verwendet wird."
    },
    {
        "category": "Dokumentation und Struktur",
        "question": "Womit kann man automatische Dokumentation erzeugen?",
        "answers": ["doctest", "pydoc", "sphinx", "docstringer"],
        "correct": 1,
        "explanation": "pydoc kann automatisch Dokumentation aus Docstrings generieren."
    },
    {
        "category": "Dokumentation und Struktur",
        "question": "Welche Zeichenfolge beschreibt den Zweck einer Funktion direkt im Code?",
        "answers": ["inline comment", "docstring", "header", "note"],
        "correct": 1,
        "explanation": "Ein Docstring ist ein String, der direkt nach der Funktionsdefinition steht und diese dokumentiert."
    },
    {
        "category": "Fehlerbehandlung",
        "question": "Welches Schlüsselwort fängt Fehler ab?",
        "answers": ["if", "try", "def", "catch"],
        "correct": 1,
        "explanation": "try startet einen Block, in dem Fehler abgefangen werden können."
    },
    {
        "category": "Fehlerbehandlung",
        "question": "Welche Reihenfolge ist korrekt?",
        "answers": ["try – pass – raise", "try – else – except", "try – except – else – finally", "except – try – raise"],
        "correct": 2,
        "explanation": "Die korrekte Reihenfolge ist try, except, else, finally."
    },
    {
        "category": "Fehlerbehandlung",
        "question": "Welcher Fehler tritt auf, wenn man eine Zahl durch 0 teilt?",
        "answers": ["SyntaxError", "ZeroDivisionError", "NameError", "ValueError"],
        "correct": 1,
        "explanation": "ZeroDivisionError wird ausgelöst, wenn versucht wird, durch Null zu teilen."
    },
    {
        "category": "Fehlerbehandlung",
        "question": "Welches Modul nutzt man für Unittests in Python?",
        "answers": ["test", "unit", "unittest", "assert"],
        "correct": 2,
        "explanation": "Das unittest-Modul bietet ein Framework für Unittests in Python."
    },
    {
        "category": "Fehlerbehandlung",
        "question": "Welche Methode prüft, ob zwei Werte gleich sind im Unittest?",
        "answers": ["assertTrue", "assertIs", "assertEqual", "assertSame"],
        "correct": 2,
        "explanation": "assertEqual prüft, ob zwei Werte gleich sind."
    }
]

# Globale Variablen
current_screen = "menu"
current_question_index = 0
score = 0
answered = False
selected_answer = None
wrong_questions = []
questions = []
completed_questions = set()  # Set zur Verfolgung der bereits beantworteten Fragen
correctly_answered = set()   # Set zur Verfolgung der richtig beantworteten Fragen

# Funktion zum Auswählen von 20 zufälligen Fragen
def select_random_questions():
    global questions
    # Wähle 20 zufällige Fragen aus, die noch nicht beantwortet wurden
    unanswered = [q for q in all_questions if all_questions.index(q) not in completed_questions]
    
    if len(unanswered) >= 20:
        questions = random.sample(unanswered, 20)
    else:
        # Wenn weniger als 20 Fragen übrig sind, nimm alle verbleibenden und fülle mit bereits beantworteten auf
        questions = unanswered
        remaining = 20 - len(unanswered)
        if remaining > 0:
            answered_questions = [q for q in all_questions if all_questions.index(q) in completed_questions]
            questions.extend(random.sample(answered_questions, min(remaining, len(answered_questions))))

# Funktion zum Berechnen des Fortschritts in Prozent
def calculate_progress():
    return (len(completed_questions) / len(all_questions)) * 100

# Funktion zum Zählen der richtig beantworteten Fragen
def count_correct_answers():
    return len(correctly_answered)

# Funktion zum Zählen der falsch beantworteten Fragen
def count_wrong_answers():
    return len(completed_questions) - len(correctly_answered)

# Funktion zum Zeichnen von Text mit Zeilenumbrüchen
def draw_text(text, font, color, x, y, max_width=None):
    if max_width:
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (x, y + i * font.get_height()))
        
        return len(lines) * font.get_height()
    else:
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
        return font.get_height()

# Funktion zum Zeichnen des Menüs
def draw_menu():
    screen.fill(LIGHT_BLUE)
    
    # Titel
    title = title_font.render("Python Grundlagen Quiz", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    # Fortschrittsbalken
    progress = calculate_progress()
    pygame.draw.rect(screen, GRAY, (WIDTH // 2 - 150, 110, 300, 20), border_radius=10)
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 150, 110, 300 * (progress / 100), 20), border_radius=10)
    
    # Fortschrittsanzeige
    progress_text = menu_font.render(f"Fortschritt: {progress:.1f}%", True, DARK_BLUE)
    screen.blit(progress_text, (WIDTH // 2 - progress_text.get_width() // 2, 140))
    
    # Statistik-Anzeige
    correct_count = count_correct_answers()
    wrong_count = count_wrong_answers()
    total_answered = len(completed_questions)
    
    if total_answered > 0:
        correct_percent = (correct_count / total_answered) * 100
        wrong_percent = (wrong_count / total_answered) * 100
        
        # Richtig-Statistik
        pygame.draw.rect(screen, DARK_GREEN, (WIDTH // 2 - 150, 190, 300, 30), border_radius=5)
        correct_text = stats_font.render(f"Richtig: {correct_count} ({correct_percent:.1f}%)", True, WHITE)
        screen.blit(correct_text, (WIDTH // 2 - correct_text.get_width() // 2, 195))
        
        # Falsch-Statistik
        pygame.draw.rect(screen, DARK_RED, (WIDTH // 2 - 150, 230, 300, 30), border_radius=5)
        wrong_text = stats_font.render(f"Falsch: {wrong_count} ({wrong_percent:.1f}%)", True, WHITE)
        screen.blit(wrong_text, (WIDTH // 2 - wrong_text.get_width() // 2, 235))
    
    # Menüoptionen
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 150, 280, 300, 60), border_radius=10)
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 150, 360, 300, 60), border_radius=10)
    pygame.draw.rect(screen, RED, (WIDTH // 2 - 150, 440, 300, 60), border_radius=10)
    
    start_text = menu_font.render("Quiz starten", True, WHITE)
    practice_text = menu_font.render("Schwerpunkte üben", True, WHITE)
    exit_text = menu_font.render("Beenden", True, WHITE)
    
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 295))
    screen.blit(practice_text, (WIDTH // 2 - practice_text.get_width() // 2, 375))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, 455))
    
    # Info-Text
    info_text = small_font.render("Jedes Quiz besteht aus 20 zufälligen Fragen aus dem Pool von 40 Fragen", True, BLACK)
    screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, 520))

# Funktion zum Zeichnen der Frage
def draw_question():
    global current_question_index, answered, selected_answer
    
    screen.fill(WHITE)
    
    # Fragebalken
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 70))
    
    # Fortschritt und Punktestand
    progress_text = menu_font.render(f"Frage {current_question_index + 1} von {len(questions)}", True, WHITE)
    score_text = menu_font.render(f"Punkte: {score}", True, WHITE)
    
    screen.blit(progress_text, (20, 20))
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))
    
    # Kategorie
    category_text = question_font.render(f"Kategorie: {questions[current_question_index]['category']}", True, BLACK)
    screen.blit(category_text, (20, 90))
    
    # Frage
    question_height = draw_text(questions[current_question_index]['question'], question_font, BLACK, 20, 130, WIDTH - 40)
    
    # Antworten
    y_pos = 150 + question_height
    for i, answer in enumerate(questions[current_question_index]['answers']):
        color = GRAY
        if answered:
            if i == questions[current_question_index]['correct']:
                color = GREEN
            elif i == selected_answer:
                color = RED
        
        pygame.draw.rect(screen, color, (20, y_pos, WIDTH - 40, 50), border_radius=5)
        draw_text(answer, answer_font, BLACK, 40, y_pos + 15, WIDTH - 80)
        y_pos += 60
    
    # Erklärung (falls beantwortet)
    if answered:
        pygame.draw.rect(screen, LIGHT_BLUE, (20, y_pos + 20, WIDTH - 40, 100), border_radius=5)
        draw_text(f"Erklärung: {questions[current_question_index]['explanation']}", explanation_font, BLACK, 30, y_pos + 30, WIDTH - 60)
        
        # Weiter-Button
        pygame.draw.rect(screen, BLUE, (WIDTH - 170, HEIGHT - 70, 150, 50), border_radius=10)
        next_text = menu_font.render("Weiter", True, WHITE)
        screen.blit(next_text, (WIDTH - 170 + 75 - next_text.get_width() // 2, HEIGHT - 70 + 25 - next_text.get_height() // 2))

# Funktion zum Zeichnen des Ergebnisses
def draw_results():
    screen.fill(LIGHT_BLUE)
    
    # Titel
    title = title_font.render("Quiz beendet!", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))
    
    # Ergebnis
    result_text = menu_font.render(f"Du hast {score} von {len(questions)} Punkten erreicht!", True, BLACK)
    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 150))
    
    # Fortschritt
    progress = calculate_progress()
    progress_text = menu_font.render(f"Gesamtfortschritt: {progress:.1f}%", True, DARK_BLUE)
    screen.blit(progress_text, (WIDTH // 2 - progress_text.get_width() // 2, 200))
    
    # Statistik
    correct_count = count_correct_answers()
    wrong_count = count_wrong_answers()
    total_answered = len(completed_questions)
    
    if total_answered > 0:
        correct_percent = (correct_count / total_answered) * 100
        wrong_percent = (wrong_count / total_answered) * 100
        
        # Richtig-Statistik
        correct_text = stats_font.render(f"Insgesamt richtig: {correct_count} ({correct_percent:.1f}%)", True, DARK_GREEN)
        screen.blit(correct_text, (WIDTH // 2 - correct_text.get_width() // 2, 240))
        
        # Falsch-Statistik
        wrong_text = stats_font.render(f"Insgesamt falsch: {wrong_count} ({wrong_percent:.1f}%)", True, DARK_RED)
        screen.blit(wrong_text, (WIDTH // 2 - wrong_text.get_width() // 2, 270))
    
    # Falsch beantwortete Fragen
    wrong_indices = [i for i in range(len(all_questions)) if i in completed_questions and i not in correctly_answered]
    if wrong_indices:
        wrong_text = menu_font.render("Falsch beantwortete Fragen:", True, BLACK)
        screen.blit(wrong_text, (WIDTH // 2 - wrong_text.get_width() // 2, 310))
        
        y_pos = 340
        for i, index in enumerate(wrong_indices):
            if i < 5:  # Zeige maximal 5 Fragen an
                question_text = explanation_font.render(f"{i+1}. {all_questions[index]['question']}", True, BLACK)
                screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, y_pos))
                y_pos += 30
    
    # Zurück zum Menü-Button
    pygame.draw.rect(screen, BLUE, (WIDTH // 2 - 150, HEIGHT - 100, 300, 60), border_radius=10)
    menu_text = menu_font.render("Zurück zum Menü", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT - 100 + 30 - menu_text.get_height() // 2))

# Hauptspiel-Schleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if current_screen == "menu":
                # Quiz starten-Button
                if WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and 280 <= mouse_pos[1] <= 340:
                    current_screen = "quiz"
                    current_question_index = 0
                    score = 0
                    answered = False
                    selected_answer = None
                    wrong_questions = []
                    # Wähle 20 zufällige Fragen aus
                    select_random_questions()
                
                # Schwerpunkte üben-Button
                elif WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and 360 <= mouse_pos[1] <= 420:
                    current_screen = "quiz"
                    current_question_index = 0
                    score = 0
                    answered = False
                    selected_answer = None
                    
                    # Nur falsch beantwortete Fragen aus vorherigem Quiz
                    wrong_indices = [i for i in range(len(all_questions)) if i in completed_questions and i not in correctly_answered]
                    
                    if wrong_indices:
                        # Erstelle eine Liste mit Fragen, die falsch beantwortet wurden
                        practice_questions = [all_questions[i] for i in wrong_indices]
                        # Ersetze die Fragen-Liste mit den falsch beantworteten Fragen
                        questions.clear()
                        questions.extend(practice_questions)
                        wrong_questions = list(range(len(questions)))  # Setze wrong_questions zurück
                    else:
                        # Falls keine falsch beantworteten Fragen vorhanden sind, zeige alle Fragen
                        select_random_questions()
                        wrong_questions = []
                
                # Beenden-Button
                elif WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and 440 <= mouse_pos[1] <= 500:
                    running = False
            
            elif current_screen == "quiz":
                if not answered:
                    # Prüfe, ob eine Antwort ausgewählt wurde
                    question_height = draw_text(questions[current_question_index]['question'], question_font, BLACK, 20, 130, WIDTH - 40)
                    y_pos = 150 + question_height
                    
                    for i in range(len(questions[current_question_index]['answers'])):
                        if 20 <= mouse_pos[0] <= WIDTH - 20 and y_pos <= mouse_pos[1] <= y_pos + 50:
                            selected_answer = i
                            answered = True
                            
                            # Überprüfe die Antwort
                            original_index = all_questions.index(questions[current_question_index])
                            completed_questions.add(original_index)
                            
                            if selected_answer == questions[current_question_index]['correct']:
                                score += 1
                                correctly_answered.add(original_index)
                            else:
                                # Speichere den Index der ursprünglichen Frage
                                wrong_questions.append(original_index)
                            
                            break
                        y_pos += 60
                
                else:
                    # Weiter-Button
                    if WIDTH - 170 <= mouse_pos[0] <= WIDTH - 20 and HEIGHT - 70 <= mouse_pos[1] <= HEIGHT - 20:
                        if current_question_index < len(questions) - 1:
                            current_question_index += 1
                            answered = False
                            selected_answer = None
                        else:
                            current_screen = "results"
            
            elif current_screen == "results":
                # Zurück zum Menü-Button
                if WIDTH // 2 - 150 <= mouse_pos[0] <= WIDTH // 2 + 150 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 40:
                    current_screen = "menu"
    
    # Zeichne den aktuellen Bildschirm
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "quiz":
        draw_question()
    elif current_screen == "results":
        draw_results()
    
    pygame.display.flip()

pygame.quit()
sys.exit()