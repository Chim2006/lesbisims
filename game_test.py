import pygame
import sys
import math

# Initialize Pygame core modules
pygame.init()

# Window Setup Variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LesbiSims: Complete Visual Prototype")
clock = pygame.time.Clock()

# Strict Global Color Palettes
COLOR_BG = (245, 238, 248)       
COLOR_CARD = (255, 255, 255)     
COLOR_TEXT = (44, 53, 57)        
COLOR_PRIMARY = (194, 24, 91)    
COLOR_SECONDARY = (142, 68, 173) 
COLOR_GREEN = (46, 204, 113)     
COLOR_SKIN = (250, 219, 185)     
COLOR_HAIR_C = (50, 50, 50)      
COLOR_HAIR_R = (220, 118, 51)    

# Universal Fonts Engine Configuration
font_main = pygame.font.SysFont("Arial", 16)
font_bold = pygame.font.SysFont("Arial", 18, bold=True)
font_title = pygame.font.SysFont("Arial", 28, bold=True)


class SimCharacter:
    def __init__(self, name, aesthetic, hair_color):
        self.name = name
        self.aesthetic = aesthetic
        self.hair_color = hair_color
        self.wallet = 500.0
        self.job = "Unemployed"
        self.hourly_wage = 0.0
        self.energy = 100.0
        self.affection = 40.0
        self.pleasure = 0.0
        self.romance_with_partner = 20.0
        self.is_nude = False
        self.current_pose = "Standing"


class Button:
    def __init__(self, x, y, width, height, text, action_id, color=COLOR_PRIMARY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_id = action_id
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surf = font_bold.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class LesbiSimsEngine:
    def __init__(self):
        self.day = 1
        self.game_mode = "LIVE"  
        self.chloe = SimCharacter("Chloe", "Alt-Goth", COLOR_HAIR_C)
        self.rachel = SimCharacter("Rachel", "Cottagecore", COLOR_HAIR_R)
        self.animation_tick = 0
        self.grid = [["." for _ in range(5)] for _ in range(5)]
        
        # Primary Action Control Array
        self.buttons = [
            Button(50, 450, 200, 40, "💼 Go to Work", "work"),
            Button(50, 500, 200, 40, "💬 Chat with Rachel", "chat"),
            Button(50, 555, 200, 40, "💋 Flirt Romantically", "flirt"),
            Button(270, 450, 220, 40, "🔥 Initiate Lesbian Sex", "woohoo"),
            Button(270, 500, 220, 40, "☕ Apply as Barista", "hire"),
            Button(270, 555, 220, 40, "🛠️ Toggle Build Mode", "build_mode"),
            Button(510, 450, 200, 40, "💤 Sleep / Next Day", "sleep")
        ]
        
        # Explicit Adult Interaction Selection Array
        self.intimacy_buttons = [
            Button(50, 540, 200, 45, "👩‍❤️‍💋‍👩 Scissoring Track", "track_scissor", COLOR_SECONDARY),
            Button(270, 540, 200, 45, "🖐️ Manual Stimulation", "track_manual", COLOR_SECONDARY),
            Button(490, 540, 200, 45, "👅 Intimate Oral Sex", "track_oral", COLOR_SECONDARY),
            Button(720, 540, 200, 45, "💤 Conclude Sequence", "end_intimacy", (100, 100, 100))
        ]

    def handle_action(self, action_id):
        if action_id == "work":
            if self.chloe.job != "Unemployed":
                self.chloe.wallet += self.chloe.hourly_wage * 8
                self.chloe.energy = max(0.0, self.chloe.energy - 35)
        elif action_id == "chat":
            self.chloe.romance_with_partner = min(100.0, self.chloe.romance_with_partner + 8)
            self.chloe.affection = min(100.0, self.chloe.affection + 15)
        elif action_id == "flirt":
            if self.chloe.romance_with_partner >= 35:
                self.chloe.romance_with_partner = min(100.0, self.chloe.romance_with_partner + 15)
            else:
                self.chloe.romance_with_partner = max(0.0, self.chloe.romance_with_partner - 5)
        elif action_id == "hire":
            self.chloe.job = "Barista"
            self.chloe.hourly_wage = 15.0
        elif action_id == "build_mode":
            self.game_mode = "BUILD" if self.game_mode == "LIVE" else "LIVE"
        elif action_id == "sleep":
            self.day += 1
            self.chloe.energy = 100.0
            self.chloe.wallet -= 50.0  
            self.chloe.pleasure = 0.0
        elif action_id == "woohoo":
            if self.chloe.romance_with_partner >= 75.0:
                self.game_mode = "INTIMACY"
                self.chloe.is_nude = True
                self.rachel.is_nude = True
                self.chloe.current_pose = "Scissoring_Loop_A"
        elif action_id == "track_scissor":
            self.chloe.current_pose = "Scissoring_Loop_A"
            self.chloe.pleasure = min(100.0, self.chloe.pleasure + 25)
        elif action_id == "track_manual":
            self.chloe.current_pose = "Manual_Loop"
            self.chloe.pleasure = min(100.0, self.chloe.pleasure + 15)
        elif action_id == "track_oral":
            self.chloe.current_pose = "Oral_Loop"
            self.chloe.pleasure = min(100.0, self.chloe.pleasure + 30)
        elif action_id == "end_intimacy":
            self.game_mode = "LIVE"
            self.chloe.is_nude = False
            self.rachel.is_nude = False
            self.chloe.current_pose = "Standing"
            self.chloe.affection = 100.0

    def draw_characters(self):
        self.animation_tick += 1
        bobbing = math.sin(self.animation_tick * 0.1) * 4
        
        if self.game_mode == "INTIMACY":
            pygame.draw.rect(screen, (169, 137, 197), (550, 180, 380, 200), border_radius=10)
            pygame.draw.rect(screen, (230, 230, 250), (570, 190, 340, 180)) 
            
            if self.chloe.current_pose == "Scissoring_Loop_A":
                shift = math.sin(self.animation_tick * 0.3) * 12
                pygame.draw.circle(screen, COLOR_SKIN, (700 + int(shift), 270), 25) 
                pygame.draw.circle(screen, COLOR_SKIN, (760 - int(shift), 270), 25) 
                pygame.draw.rect(screen, COLOR_HAIR_C, (685 + int(shift), 245, 30, 15), border_radius=5)
                pygame.draw.rect(screen, COLOR_HAIR_R, (745 - int(shift), 245, 30, 15), border_radius=5)
            else:
                pygame.draw.circle(screen, COLOR_SKIN, (710, 260 + int(bobbing)), 25)
                pygame.draw.circle(screen, COLOR_SKIN, (780, 260 - int(bobbing)), 25)
                pygame.draw.rect(screen, COLOR_HAIR_C, (695, 235 + int(bobbing), 30, 15), border_radius=5)
                pygame.draw.rect(screen, COLOR_HAIR_R, (765, 235 - int(bobbing), 30, 15), border_radius=5)
        else:
            pygame.draw.circle(screen, COLOR_SKIN, (650, 220 + int(bobbing)), 30) 
            pygame.draw.rect(screen, COLOR_HAIR_C, (630, 190 + int(bobbing), 40, 25), border_radius=6) 
            pygame.draw.rect(screen, (40, 40, 40), (625, 250 + int(bobbing), 50, 70), border_radius=4) 
            
            pygame.draw.circle(screen, COLOR_SKIN, (800, 220 - int(bobbing)), 30)
            pygame.draw.rect(screen, COLOR_HAIR_R, (780, 190 - int(bobbing), 40, 25), border_radius=6)
            pygame.draw.rect(screen, (115, 198, 182), (775, 250 - int(bobbing), 50, 70), border_radius=4) 

    def draw_hud_and_menus(self):
        pygame.draw.rect(screen, COLOR_CARD, (30, 20, 450, 380), border_radius=12) 
        pygame.draw.rect(screen, COLOR_CARD, (500, 20, 470, 380), border_radius=12) 
        pygame.draw.rect(screen, COLOR_CARD, (30, 420, 940, 200), border_radius=12) 
        
        title_surf = font_title.render("LesbiSims Engine Console", True, COLOR_PRIMARY)
        screen.blit(title_surf, (50, 40))
        
        day_surf = font_bold.render(f"Simulation Day: {self.day}   |   Mode: {self.game_mode}", True, COLOR_TEXT)
        screen.blit(day_surf, (50, 85))
        
        wallet_surf = font_main.render(f"Available Funds: ${self.chloe.wallet:.2f}", True, COLOR_TEXT)
        screen.blit(wallet_surf, (50, 130))
        
        job_surf = font_main.render(f"Job: {self.chloe.job} (${self.chloe.hourly_wage}/hr)", True, COLOR_TEXT)
        screen.blit(job_surf, (50, 160))
        
        self.render_stat_bar(50, 220, "Energy", self.chloe.energy, (230, 126, 34))
        self.render_stat_bar(50, 260, "Affection", self.chloe.affection, (52, 152, 219))
        self.render_stat_bar(50, 300, "Pleasure", self.chloe.pleasure, COLOR_PRIMARY)
        self.render_stat_bar(50, 350, "Rachel Romance", self.chloe.romance_with_partner, COLOR_SECONDARY)
        
        if self.game_mode == "BUILD":
            for r in range(5):
                for c in range(5):
                    pygame.draw.rect(screen, (220, 220, 220), (540 + (c * 65), 80 + (r * 55), 55, 45), 1)
            notice_surf = font_bold.render("BUILD GRID ACTIVE: Left-Click node blocks to place assets", True, COLOR_SECONDARY)
            screen.blit(notice_surf, (530, 45))

    def render_stat_bar(self, x, y, label, value, color):
        lbl_surf = font_main.render(f"{label}: {int(value)}%", True, COLOR_TEXT)
        screen.blit(lbl_surf, (x, y))
        pygame.draw.rect(screen, (220, 220, 220), (x + 180, y + 2, 200, 14), border_radius=4)
        fill_w = int((value / 100.0) * 200)
        if fill_w > 0:
            pygame.draw.rect(screen, color, (x + 180, y + 2, fill_w, 14), border_radius=4)

    def run_main_loop(self):
        running = True
        while running:
            screen.fill(COLOR_BG)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
