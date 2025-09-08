import pygame
import sys
import random

# Pygame initialisieren
pygame.init()

# Bildschirmeinstellungen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump and Run Spiel")

# Farben
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Spieler-Eigenschaften
player_width, player_height = 40, 60
player_x = 50
player_y = HEIGHT - player_height - 100
player_speed = 5
jump_height = 15
is_jumping = False
jump_count = jump_height
player_velocity_y = 0
gravity = 0.8

# Level-Daten
levels = [
    # Level 1
    {
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),  # Boden
            (300, HEIGHT - 120, 200, 20),
            (600, HEIGHT - 200, 200, 20),
            (200, HEIGHT - 280, 150, 20),
            (500, HEIGHT - 350, 150, 20)
        ],
        "enemies": [
            {"x": 400, "y": HEIGHT - 80, "width": 30, "height": 30, "speed": 2, "min_x": 300, "max_x": 500},
            {"x": 700, "y": HEIGHT - 240, "width": 30, "height": 30, "speed": 2, "min_x": 600, "max_x": 800}
        ],
        "goal": (750, HEIGHT - 380, 30, 30)
    },
    # Level 2
    {
        "platforms": [
            (0, HEIGHT - 40, WIDTH, 40),  # Boden
            (200, HEIGHT - 120, 100, 20),
            (400, HEIGHT - 200, 100, 20),
            (600, HEIGHT - 280, 100, 20),
            (300, HEIGHT - 360, 100, 20),
            (500, HEIGHT - 440, 100, 20)
        ],
        "enemies": [
            {"x": 250, "y": HEIGHT - 80, "width": 30, "height": 30, "speed": 3, "min_x": 200, "max_x": 300},
            {"x": 450, "y": HEIGHT - 240, "width": 30, "height": 30, "speed": 3, "min_x": 400, "max_x": 500},
            {"x": 550, "y": HEIGHT - 480, "width": 30, "height": 30, "speed": 3, "min_x": 500, "max_x": 600}
        ],
        "goal": (700, HEIGHT - 480, 30, 30)
    }
]

current_level = 0
game_state = "playing"  # "playing", "level_complete", "game_over"

# Spieler resetten
def reset_player():
    global player_x, player_y, player_velocity_y, is_jumping
    player_x = 50
    player_y = HEIGHT - player_height - 100
    player_velocity_y = 0
    is_jumping = False

# Spiel-Loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state != "playing":
                    if game_state == "level_complete":
                        current_level += 1
                        if current_level >= len(levels):
                            current_level = 0  # Zurück zum ersten Level oder Spiel beenden
                        reset_player()
                        game_state = "playing"
                    elif game_state == "game_over":
                        reset_player()
                        game_state = "playing"
                elif not is_jumping:  # Nur springen, wenn wir nicht bereits springen
                    is_jumping = True
                    player_velocity_y = -jump_height
    
    if game_state == "playing":
        # Tasteneingaben verarbeiten
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Links bewegen mit A
            player_x -= player_speed
        if keys[pygame.K_d]:  # Rechts bewegen mit D
            player_x += player_speed
        
        # Schwerkraft anwenden
        player_velocity_y += gravity
        player_y += player_velocity_y
        
        # Kollisionserkennung mit Plattformen
        on_ground = False
        for platform in levels[current_level]["platforms"]:
            # Fall von oben auf die Plattform
            if (player_x + player_width > platform[0] and 
                player_x < platform[0] + platform[2] and 
                player_y + player_height > platform[1] and 
                player_y + player_height < platform[1] + 20 and 
                player_velocity_y > 0):
                player_y = platform[1] - player_height
                player_velocity_y = 0
                is_jumping = False
                on_ground = True
            
            # Kollision von der Seite
            if (player_x + player_width > platform[0] and 
                player_x < platform[0] + platform[2] and 
                player_y < platform[1] + platform[3] and 
                player_y + player_height > platform[1]):
                # Von rechts
                if player_x + player_width > platform[0] and player_velocity_y > 0:
                    player_x = platform[0] - player_width
                # Von links
                elif player_x < platform[0] + platform[2] and player_velocity_y > 0:
                    player_x = platform[0] + platform[2]
        
        # Bildschirmbegrenzungen
        if player_x < 0:
            player_x = 0
        if player_x > WIDTH - player_width:
            player_x = WIDTH - player_width
        if player_y > HEIGHT:
            game_state = "game_over"
        
        # Gegner aktualisieren
        for enemy in levels[current_level]["enemies"]:
            # Gegner bewegen
            enemy["x"] += enemy["speed"]  # Geschwindigkeit addieren
            if enemy["x"] < enemy["min_x"]:  # Linke Grenze
                enemy["x"] = enemy["min_x"]
                enemy["speed"] *= -1
            if enemy["x"] + enemy["width"] > enemy["max_x"]:  # Rechte Grenze
                enemy["x"] = enemy["max_x"] - enemy["width"]
                enemy["speed"] *= -1
            
            # Kollision mit Gegner
            if (player_x < enemy["x"] + enemy["width"] and 
                player_x + player_width > enemy["x"] and 
                player_y < enemy["y"] + enemy["height"] and 
                player_y + player_height > enemy["y"]):
                game_state = "game_over"
        
        # Ziel überprüfen
        goal = levels[current_level]["goal"]
        if (player_x < goal[0] + goal[2] and 
            player_x + player_width > goal[0] and 
            player_y < goal[1] + goal[3] and 
            player_y + player_height > goal[1]):
            game_state = "level_complete"
    
    # Zeichnen
    screen.fill(WHITE)
    
    # Plattformen zeichnen
    for platform in levels[current_level]["platforms"]:
        pygame.draw.rect(screen, BROWN, platform)
    
    # Gegner zeichnen
    for enemy in levels[current_level]["enemies"]:
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy["width"], enemy["height"]))
    
    # Ziel zeichnen
    goal = levels[current_level]["goal"]
    pygame.draw.rect(screen, GREEN, goal)
    
    # Spieler zeichnen
    pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))
    
    # Spielstatus anzeigen
    if game_state == "level_complete":
        font = pygame.font.SysFont(None, 36)
        text = font.render("Level geschafft! Leertaste für nächstes Level", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    
    if game_state == "game_over":
        font = pygame.font.SysFont(None, 36)
        text = font.render("Game Over! Leertaste zum Neustart", True, BLACK)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    
    # Levelnummer anzeigen
    font = pygame.font.SysFont(None, 36)
    level_text = font.render(f"Level {current_level + 1}", True, BLACK)
    screen.blit(level_text, (10, 10))
    
    # Steuerungshinweis anzeigen
    controls_text = font.render("Steuerung: A (links), D (rechts), Leertaste (springen)", True, BLACK)
    screen.blit(controls_text, (10, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()