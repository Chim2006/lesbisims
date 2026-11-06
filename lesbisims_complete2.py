import pygame
import sys
import math
import random

# Initialize Pygame core modules and audio mixer
pygame.init()
pygame.mixer.init()

# Window Setup Variables
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LesbiSims: Definitive Production Master Engine")
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
COLOR_BLONDE = (244, 208, 63)

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
        self.clothing_color = (40, 40, 40) if name == "Chloe" else (115, 198, 182)


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
        self.game_mode = "CAS"  # CAS (Character Customization Startup), LIVE, BUILD, INTIMACY, SHOP, TRAVEL
        self.current_location = "Home Sweet Home"
        self.current_moodlet = "Normal"
        self.narrative_ticker = "Welcome to LesbiSims. Customize your starting profile setup!"
        
        # Instantiate base entity classes
        self.chloe = SimCharacter("Chloe", "Alt-Goth", COLOR_HAIR_C)
        self.rachel = SimCharacter("Rachel", "Cottagecore", COLOR_HAIR_R)
        self.animation_tick = 0
        self.grid = [["." for _ in range(5)] for _ in range(5)]
        
        # --- NEW PHASE 5: CAS CREATOR INTERFACE BUTTONS ---
        self.cas_buttons = [
            Button(100, 200, 250, 45, "🖤 Style: Goth (Dark Hair)", "set_goth", COLOR_PRIMARY),
            Button(100, 260, 250, 45, "☀️ Style: Cottagecore (Blonde)", "set_cottage", COLOR_SECONDARY),
            Button(100, 320, 250, 45, "🎸 Style: Punk (Ginger Hair)", "set_punk", (230, 126, 34)),
            Button(100, 450, 250, 50, "✅ CONFIRM & ENTER WORLD", "confirm_cas", COLOR_GREEN)
        ]
        
        # Live Mode Control Dashboard Layout Array
        self.buttons = [
            Button(50, 440, 200, 38, "💼 Go to Work", "work"),
            Button(50, 485, 200, 38, "💬 Chat with Rachel", "chat"),
            Button(50, 530, 200, 38, "💋 Flirt Romantically", "flirt"),
            Button(50, 575, 200, 38, "💰 Cheat: Motherlode", "cheat_cash", (230, 126, 34)),
            
            Button(270, 440, 220, 38, "🔥 Initiate Lesbian Sex", "woohoo"),
            Button(270, 485, 220, 38, "☕ Apply as Barista", "hire"),
            Button(270, 530, 220, 38, "🛠️ Toggle Build Mode", "build_mode"),
            Button(270, 575, 220, 38, "🚗 Travel to Map", "open_map", COLOR_SECONDARY),
            
            Button(510, 440, 200, 38, "💤 Sleep / Next Day", "sleep"),
            Button(510, 485, 200, 38, "🛍️ Open Shop Catalog", "open_shop", COLOR_GREEN)
        ]
        
        # Explicit Adult Interaction Selection Array
        self.intimacy_buttons = [
            Button(50, 540, 200, 45, "👩‍❤️‍💋‍👩 Scissoring Track", "track_scissor", COLOR_SECONDARY),
            Button(270, 540, 200, 45, "🖐️ Manual Stimulation", "track_manual", COLOR_SECONDARY),
            Button(490, 540, 200, 45, "👅 Intimate Oral Sex", "track_oral", COLOR_SECONDARY),
            Button(720, 540, 200, 45, "💤 Conclude Sequence", "end_intimacy", (100, 100, 100))
        ]

        # Shopping Content Selection Array
        self.shop_buttons = [
            Button(50, 450, 260, 45, "👗 Buy Royal Corset ($120)", "buy_corset", COLOR_GREEN),
            Button(330, 450, 260, 45, "👚 Buy Coral Dress ($100)", "buy_dress", COLOR_GREEN),
            Button(50, 510, 260, 45, "🛏️ Buy Luxury Bed ($300)", "buy_bed", COLOR_GREEN),
            Button(330, 510, 260, 45, "🏳️‍🌈 Buy Progress Flag ($40)", "buy_flag", COLOR_GREEN),
            Button(620, 480, 200, 45, "❌ Close Catalog", "close_shop", (150, 150, 150))
        ]

        # Travel Locations Array
        self.travel_buttons = [
            Button(50, 460, 260, 45, "☕ Go to Queer Cafe", "travel_cafe", COLOR_SECONDARY),
            Button(330, 460, 260, 45, "💃 Go to Dance Lounge", "travel_lounge", COLOR_SECONDARY),
            Button(50, 520, 260, 45, "🏡 Return Home", "travel_home", COLOR_PRIMARY),
            Button(620, 490, 200, 45, "❌ Close Map", "close_map", (150, 150, 150))
        ]

    def trigger_sfx_simulation(self, sound_type):
        print(f"🎵 [SFX Engine Call]: Playing audio asset -> '{sound_type}.wav'")

    def roll_random_narrative_event(self):
        """NEW MODULE: Automatically fires story-driven events upon waking up."""
        events = [
            ("💌 Rachel left a sweet romantic letter on your desk! (+10 Romance)", "romance_boost"),
            ("💼 Your manager at the cafe gave you an unexpected performance bonus! (+$150)", "cash_boost"),
            ("🌧️ It's a rainy morning. You feel slightly sluggish today.", "sluggish"),
            ("📣 A pop-up queer festival is happening at the Dance Lounge tonight!", "festival")
        ]
        chosen_text, event_id = random.choice(events)
        self.narrative_ticker = chosen_text
        
        if event_id == "romance_boost":
            self.chloe.romance_with_partner = min(100.0, self.chloe.romance_with_partner + 10)
        elif event_id == "cash_boost":
            self.chloe.wallet += 150.0

    def roll_random_moodlet(self):
        roll = random.choice(["Normal", "Lovestruck", "Burnout", "Flustered"])
        self.current_moodlet = roll
        print(f"🎭 [Mood AI]: Chloe woke up feeling: {self.current_moodlet}")

    def handle_action(self, action_id):
        # Character Creation (CAS) Layer Sub-controls
        if action_id == "set_goth":
            self.chloe.aesthetic = "Alt-Goth"
            self.chloe.hair_color = COLOR_HAIR_C
            self.chloe.clothing_color = (25, 25, 25)
            self.narrative_ticker = "Profile updated: Goth aesthetic applied."
        elif action_id == "set_cottage":
            self.chloe.aesthetic = "Cottagecore"
            self.chloe.hair_color = COLOR_BLONDE
            self.chloe.clothing_color = (133, 193, 233)
            self.narrative_ticker = "Profile updated: Cottagecore style applied."
        elif action_id == "set_punk":
            self.chloe.aesthetic = "Punk"
            self.chloe.hair_color = COLOR_HAIR_R
            self.chloe.clothing_color = (120, 40, 140)
            self.narrative_ticker = "Profile updated: Punk rock style applied."
        elif action_id == "confirm_cas":
            self.game_mode = "LIVE"
            self.narrative_ticker = f"Game Engine Started! Live simulation active in {self.current_location}."

        # Live Simulator Actions
        elif action_id == "work":
            if self.chloe.job != "Unemployed":
                wage_multiplier = 0.5 if self.current_moodlet == "Burnout" else 1.0
                loc_bonus = 1.2 if self.current_location == "Queer Cafe" else 1.0
                self.chloe.wallet += (self.chloe.hourly_wage * 8) * wage_multiplier * loc_bonus
                self.chloe.energy = max(0.0, self.chloe.energy - 35)
                self.trigger_sfx_simulation("cash_register_payout")
        elif action_id == "chat":
            bonus = 15 if self.current_moodlet == "Lovestruck" else 8
            self.chloe.romance_with_partner = min(100.0, self.chloe.romance_with_partner + bonus)
            self.chloe.affection = min(100.0, self.chloe.affection + 15)
            self.trigger_sfx_simulation("chloe_giggle")
        elif action_id == "flirt":
            if self.chloe.romance_with_partner >= 35 or self.current_moodlet == "Lovestruck":
                self.chloe.romance_with_partner = min(100.0, self.chloe.romance_with_partner + 20)
                self.trigger_sfx_simulation("kiss_sfx_loop")
            else:
                self.chloe.romance_with_partner = max(0.0, self.chloe.romance_with_partner - 10)
                self.trigger_sfx_simulation("awkward_cough")
        elif action_id == "cheat_cash":
            self.chloe.wallet += 50000.0  
            self.trigger_sfx_simulation("motherlode_cheat_success")
        elif action_id == "hire":
            self.chloe.job = "Barista"
            self.chloe.hourly_wage = 15.0
            self.trigger_sfx_simulation("promotion_chime")
        elif action_id == "build_mode":
            self.game_mode = "BUILD" if self.game_mode == "LIVE" else "LIVE"
        elif action_id == "open_shop":
            self.game_mode = "SHOP"
        elif action_id == "close_shop":
            self.game_mode = "LIVE"
        elif action_id == "open_map":
            self.game_mode = "TRAVEL"
        elif action_id == "close_map":
            self.game_mode = "LIVE"
