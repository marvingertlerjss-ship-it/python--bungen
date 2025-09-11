import pygame
import sys
import json
import os
import hashlib
import random
from typing import Optional

# -----------------------------
# Konfiguration
# -----------------------------
WIDTH, HEIGHT = 900, 600
FPS = 60
FONT_SIZE = 28
SMALL_SIZE = 22
BIG_SIZE = 40
STATE_FILE = "game_state.json"
MAX_SEE = 50
REGEN_RATE = 0.25  # 25% der Differenz zu MAX_SEE pro Monat
MAX_MONATE = 10
TEAMS = ["A", "B", "C"]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ecopoly – 3 Teams, private Eingaben")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", FONT_SIZE)
FONT_SMALL = pygame.font.SysFont("Arial", SMALL_SIZE)
FONT_BIG = pygame.font.SysFont("Arial", BIG_SIZE)

# -----------------------------
# Hilfsfunktionen für State & Security
# -----------------------------
def _default_state():
    return {
        "see": MAX_SEE,
        "sonne": 50.0,  # Öko-Index (0..100). Spiel endet < 1

        "monat": 1,
        "max_monate": MAX_MONATE,
        "ended_by": None,
        "teams": {
            t: {"salt": None, "pwd_hash": None, "vorrat": 0, "letztes_gebot": None}
            for t in TEAMS
        },
        "gebote_offen": {t: None for t in TEAMS},
        "submitted_this_month": {t: False for t in TEAMS},
    }


def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                st = json.load(f)
            # --- Migration: fehlende Keys ergänzen, damit alte Saves nicht crashen ---
            st.setdefault("sonne", 50.0)
            st.setdefault("ended_by", None)
            st.setdefault("submitted_this_month", {t: False for t in TEAMS})
            st.setdefault("gebote_offen", {t: None for t in TEAMS})
            if "teams" in st:
                for t in TEAMS:
                    st["teams"].setdefault(t, {"salt": None, "pwd_hash": None, "vorrat": 0, "letztes_gebot": None})
            else:
                st["teams"] = {t: {"salt": None, "pwd_hash": None, "vorrat": 0, "letztes_gebot": None} for t in TEAMS}
            return st
        except Exception:
            pass
    return _default_state()


def save_state(state):
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def gen_salt() -> str:
    return os.urandom(16).hex()


def hash_pwd(salt: str, pwd: str) -> str:
    h = hashlib.sha256()
    h.update((salt + pwd).encode("utf-8"))
    return h.hexdigest()


def verify_pwd(salt: str, pwd_hash: str, attempt: str) -> bool:
    if salt is None or pwd_hash is None:
        return False
    return hash_pwd(salt, attempt) == pwd_hash


# -----------------------------
# UI-Komponenten
# -----------------------------
class Button:
    def __init__(self, rect, text, on_click=None, enabled=True):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.enabled = enabled

    def draw(self, surf):
        color = (200, 200, 200) if self.enabled else (140, 140, 140)
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, (60, 60, 60), self.rect, width=2, border_radius=10)
        label = FONT.render(self.text, True, (0, 0, 0))
        surf.blit(label, label.get_rect(center=self.rect.center))

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()


class TextInput:
    def __init__(self, rect, placeholder="", password=False, maxlen=16):
        self.rect = pygame.Rect(rect)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.password = password
        self.maxlen = maxlen

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), self.rect, border_radius=8)
        pygame.draw.rect(surf, (60, 60, 60), self.rect, width=2, border_radius=8)
        display = ("*" * len(self.text)) if self.password else self.text
        if not self.text and not self.active:
            label = FONT_SMALL.render(self.placeholder, True, (120, 120, 120))
        else:
            label = FONT_SMALL.render(display, True, (0, 0, 0))
        surf.blit(label, (self.rect.x + 10, self.rect.y + (self.rect.height - label.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass  # handled by caller
            else:
                ch = event.unicode
                if ch and ch.isprintable() and len(self.text) < self.maxlen:
                    self.text += ch

    def get(self):
        return self.text

    def clear(self):
        self.text = ""


# -----------------------------
# Screens
# -----------------------------
class ScreenBase:
    def __init__(self, app):
        self.app = app
        self.widgets = []

    def draw_header(self, title: str):
        pygame.draw.rect(screen, (240, 240, 250), (0, 0, WIDTH, 80))
        lbl = FONT_BIG.render(title, True, (20, 20, 20))
        screen.blit(lbl, (30, 20))
        # Meta rechts
        st = self.app.state
        meta = f"Monat {st['monat']}/{st['max_monate']} | Sonne: {st.get('sonne', 50.0):.1f}"
        meta_lbl = FONT.render(meta, True, (40, 40, 40))
        screen.blit(meta_lbl, (WIDTH - meta_lbl.get_width() - 30, 28))

    def draw(self):
        screen.fill((250, 252, 255))
        for w in self.widgets:
            w.draw(screen)

    def handle_event(self, event):
        for w in self.widgets:
            if hasattr(w, "handle_event"):
                w.handle_event(event)


class MainMenu(ScreenBase):
    def __init__(self, app):
        super().__init__(app)
        self.btn_team = {}
        gap = 20
        btn_w, btn_h = 220, 60
        start_x = (WIDTH - (btn_w * 3 + gap * 2)) // 2
        y = 200
        for i, t in enumerate(TEAMS):
            rect = (start_x + i * (btn_w + gap), y, btn_w, btn_h)
            self.btn_team[t] = Button(rect, f"Team {t}", on_click=lambda tt=t: self.open_team_login(tt))
            self.widgets.append(self.btn_team[t])
        self.btn_privacy = Button((WIDTH//2 - 150, 300, 300, 50), "Privatsphäre-Hinweis", on_click=self.privacy_hint)
        self.widgets.append(self.btn_privacy)
        self.btn_reset_month = Button((WIDTH//2 - 150, 370, 300, 50), "Monat abschließen (wenn alle)", on_click=self.try_close_month)
        self.widgets.append(self.btn_reset_month)
        self.btn_reset_game = Button((WIDTH//2 - 150, 440, 300, 50), "Neues Spiel (Reset)", on_click=self.reset_confirm)
        self.widgets.append(self.btn_reset_game)

    def open_team_login(self, team):
        self.app.set_screen(TeamLogin(self.app, team))

    def privacy_hint(self):
        self.app.set_screen(PrivacyScreen(self.app, "Bitte Bildschirm abdecken/wegschauen, wenn andere Teams eingeben."))

    def try_close_month(self):
        st = self.app.state
        if st["monat"] > st["max_monate"]:
            return
        # Check ob alle eingereicht haben
        if all(st["submitted_this_month"][t] for t in TEAMS):
            self.app.process_month()
            if self.app.state["monat"] > self.app.state["max_monate"]:
                self.app.set_screen(EndScreen(self.app))
            else:
                self.app.set_screen(PrivacyScreen(self.app, "Monat abgeschlossen. Nächster Monat startet.", next_to=MainMenu(self.app)))
        else:
            self.app.set_screen(PrivacyScreen(self.app, "Nicht alle Teams haben abgegeben."))

    def reset_confirm(self):
        self.app.set_screen(ConfirmReset(self.app))

    def draw(self):
        super().draw()
        self.draw_header("Ecopoly – Hauptmenü")

        st = self.app.state
        # Statusbox
        box = pygame.Rect(WIDTH//2 - 320, 100, 640, 80)
        pygame.draw.rect(screen, (230, 238, 255), box, border_radius=12)
        pygame.draw.rect(screen, (80, 100, 160), box, width=2, border_radius=12)

        status = []
        for t in TEAMS:
            done = st["submitted_this_month"][t]
            status.append(f"Team {t}: {'Abgegeben' if done else 'Offen'}")
        text = " | ".join(status)
        lbl = FONT.render(text, True, (20, 30, 50))
        screen.blit(lbl, lbl.get_rect(center=box.center))


class ConfirmReset(ScreenBase):
    def __init__(self, app):
        super().__init__(app)
        self.widgets.append(Button((WIDTH//2 - 160, 260, 150, 50), "Ja, Reset", on_click=self.reset))
        self.widgets.append(Button((WIDTH//2 + 10, 260, 150, 50), "Nein", on_click=lambda: self.app.set_screen(MainMenu(self.app))))

    def reset(self):
        self.app.state = _default_state()
        save_state(self.app.state)
        self.app.set_screen(PrivacyScreen(self.app, "Spiel zurückgesetzt.", next_to=MainMenu(self.app)))

    def draw(self):
        super().draw()
        self.draw_header("Bestätigen")
        msg = "Willst du wirklich ein neues Spiel starten? (Alles wird gelöscht)"
        lbl = FONT.render(msg, True, (50, 0, 0))
        screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, 180))


class PrivacyScreen(ScreenBase):
    def __init__(self, app, msg: str, next_to: Optional[ScreenBase]=None):
        super().__init__(app)
        self.msg = msg
        self.next_to = next_to
        self.widgets.append(Button((WIDTH//2 - 150, HEIGHT//2 + 40, 300, 60), "OK", on_click=self.go_next))

    def go_next(self):
        self.app.set_screen(self.next_to or MainMenu(self.app))

    def draw(self):
        super().draw()
        self.draw_header("Privatsphäre")
        lbl = FONT.render(self.msg, True, (0, 0, 0))
        screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, HEIGHT//2 - 20))


class TeamLogin(ScreenBase):
    def __init__(self, app, team: str):
        super().__init__(app)
        self.team = team
        self.pwd_input = TextInput((WIDTH//2 - 200, 260, 400, 50), "Passwort eingeben oder setzen", password=True, maxlen=32)
        self.widgets.append(self.pwd_input)
        self.btn_login = Button((WIDTH//2 - 200, 330, 190, 50), "Login/Setzen", on_click=self.login)
        self.btn_back = Button((WIDTH//2 + 10, 330, 190, 50), "Zurück", on_click=lambda: self.app.set_screen(MainMenu(self.app)))
        self.widgets.extend([self.btn_login, self.btn_back])
        self.error_msg = None

    def login(self):
        st = self.app.state
        team_data = st["teams"][self.team]
        pwd = self.pwd_input.get().strip()
        if not pwd:
            self.error_msg = "Passwort darf nicht leer sein."
            return
        if team_data["pwd_hash"] is None:
            # Passwort setzen
            salt = gen_salt()
            team_data["salt"] = salt
            team_data["pwd_hash"] = hash_pwd(salt, pwd)
            save_state(st)
            self.app.set_screen(PrivacyScreen(self.app, f"Passwort für Team {self.team} gesetzt.", next_to=TeamPanel(self.app, self.team)))
        else:
            if verify_pwd(team_data["salt"], team_data["pwd_hash"], pwd):
                self.app.set_screen(TeamPanel(self.app, self.team))
            else:
                self.error_msg = "Falsches Passwort."

    def draw(self):
        super().draw()
        self.draw_header(f"Team {self.team} – Login")
        hint1 = "Wenn noch kein Passwort gesetzt wurde: Hier setzen."
        lbl = FONT_SMALL.render(hint1, True, (60, 60, 60))
        screen.blit(lbl, (WIDTH//2 - lbl.get_width()//2, 200))
        if self.error_msg:
            err = FONT_SMALL.render(self.error_msg, True, (160, 0, 0))
            screen.blit(err, (WIDTH//2 - err.get_width()//2, 230))


class TeamPanel(ScreenBase):
    def __init__(self, app, team: str):
        super().__init__(app)
        self.team = team
        self.input_bid = TextInput((WIDTH//2 - 150, 290, 300, 50), "Gebot/Entnahme für diesen Monat (0..n)", password=False, maxlen=6)
        self.widgets.append(self.input_bid)
        self.btn_submit = Button((WIDTH//2 - 150, 360, 300, 50), "Abgeben", on_click=self.submit)
        self.btn_back = Button((20, HEIGHT - 70, 160, 50), "Abbrechen", on_click=self.back)
        self.widgets.extend([self.btn_submit, self.btn_back])
        self.error_msg = None

    def back(self):
        self.app.set_screen(PrivacyScreen(self.app, "Eingabe abgebrochen.", next_to=MainMenu(self.app)))

    def submit(self):
        st = self.app.state
        if st["submitted_this_month"][self.team]:
            self.error_msg = "Schon abgegeben in diesem Monat."
            return
        raw = self.input_bid.get().strip()
        if not raw.isdigit():
            self.error_msg = "Bitte eine nicht-negative Ganzzahl eingeben."
            return
        bid = int(raw)
        if bid < 0:
            self.error_msg = "Gebot darf nicht negativ sein."
            return
        # Optional: grobe Cap auf aktuellem See-Stand (nicht zwingend, da alle zusammen entnehmen)
        # Wir erlauben beliebige Eingabe; Validierung erfolgt beim Monatsabschluss.
        st["gebote_offen"][self.team] = bid
        st["submitted_this_month"][self.team] = True
        save_state(st)
        self.app.set_screen(PrivacyScreen(self.app, f"Team {self.team}: Gebot gespeichert.", next_to=MainMenu(self.app)))

    def draw(self):
        super().draw()
        self.draw_header(f"Team {self.team} – Private Eingabe")
        st = self.app.state
        team_data = st["teams"][self.team]

        # Private Infos dieses Teams
        box = pygame.Rect(WIDTH//2 - 350, 120, 700, 150)
        pygame.draw.rect(screen, (235, 255, 235), box, border_radius=12)
        pygame.draw.rect(screen, (60, 140, 60), box, width=2, border_radius=12)

        lines = [
            f"Monat: {st['monat']}/{st['max_monate']}",
            f"Dein Vorrat: {team_data['vorrat']}",
            f"Dein letztes Gebot: {team_data['letztes_gebot'] if team_data['letztes_gebot'] is not None else '-'}",
        ]
        y = box.y + 16
        for ln in lines:
            lbl = FONT.render(ln, True, (10, 50, 10))
            screen.blit(lbl, (box.x + 16, y))
            y += 36

        hint = "Wichtig: Deine Eingabe ist privat. Nach Abgabe zurück zum Hauptmenü."
        lbl2 = FONT_SMALL.render(hint, True, (60, 60, 60))
        screen.blit(lbl2, (WIDTH//2 - lbl2.get_width()//2, 250))

        if self.error_msg:
            err = FONT_SMALL.render(self.error_msg, True, (160, 0, 0))
            screen.blit(err, (WIDTH//2 - err.get_width()//2, 260))


class EndScreen(ScreenBase):
    def __init__(self, app):
        super().__init__(app)
        self.widgets.append(Button((WIDTH//2 - 150, HEIGHT - 100, 300, 50), "Neues Spiel", on_click=self.reset))

    def reset(self):
        self.app.state = _default_state()
        save_state(self.app.state)
        self.app.set_screen(MainMenu(self.app))

    def draw(self):
        super().draw()
        self.draw_header("Spielende – Zusammenfassung")
        st = self.app.state

        # Grund für Spielende
        reason = None
        if st.get("ended_by") == "Sonne<1":
            reason = "Spielende: Sonne < 1 (Öko-Index unterschritten)"
        else:
            reason = "Spielende: Max. Monate erreicht"
        lblr = FONT.render(reason, True, (120, 20, 20))
        screen.blit(lblr, (WIDTH//2 - lblr.get_width()//2, 100))

        # Rangliste
        rows = []
        for t in TEAMS:
            rows.append((t, st["teams"][t]["vorrat"]))
        rows.sort(key=lambda x: x[1], reverse=True)

        y = 160
        for rank, (t, v) in enumerate(rows, 1):
            lbl = FONT.render(f"{rank}. Team {t} – Vorrat: {v}", True, (20, 20, 20))
            screen.blit(lbl, (WIDTH//2 - 220, y))
            y += 40

        info1 = f"End-See-Stand: {st['see']}"
        info2 = f"Sonne (Öko-Index): {st['sonne']:.1f}"
        lbl2 = FONT.render(info1 + " | " + info2, True, (20, 20, 20))
        screen.blit(lbl2, (WIDTH//2 - lbl2.get_width()//2, y + 20))


# -----------------------------
# App-Controller
# -----------------------------
class App:
    def __init__(self):
        self.state = load_state()
        self.current_screen: ScreenBase = MainMenu(self)

    def set_screen(self, screen_obj: ScreenBase):
        self.current_screen = screen_obj

    def process_month(self):
        st = self.state
        if st["monat"] > st["max_monate"]:
            return

        bids = st["gebote_offen"]
        # Fehlende Gebote zählen als 0
        summe = 0
        for t in TEAMS:
            b = bids.get(t)
            if b is None:
                b = 0
            # Team-Vorrat addieren
            st["teams"][t]["vorrat"] += b
            st["teams"][t]["letztes_gebot"] = b
            bids[t] = None  # reset for next month
            summe += b

        # Entnahme & Caps
        st["see"] = max(0, st["see"] - summe)
        # Regeneration (einfaches Modell)
        regen = int(round((MAX_SEE - st["see"]) * REGEN_RATE))
        st["see"] = min(MAX_SEE, st["see"] + regen)

        # Öko-Index 'sonne' updaten
        entnahme_intens = summe / MAX_SEE
        regen_intens = regen / MAX_SEE
        delta = entnahme_intens - regen_intens
        if delta > 0:
            st["sonne"] = max(0.0, st["sonne"] - delta * 10.0)
        else:
            st["sonne"] = min(100.0, st["sonne"] + min(1.0, (-delta) * 2.0))

        # Endbedingung: sofortiges Spielende, sobald Sonne < 1
        if st["sonne"] < 1.0:
            st["monat"] = st["max_monate"] + 1
            st["ended_by"] = "Sonne<1"
            save_state(st)
            return

        # Monat weiter
        st["monat"] += 1
        st["submitted_this_month"] = {t: False for t in TEAMS}
        save_state(st)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # ESC = schneller Privacy-Screen
                    self.set_screen(PrivacyScreen(self, "Bildschirm verdecken/weitergeben."))
                self.current_screen.handle_event(event)

            self.current_screen.draw()
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    App().run()
