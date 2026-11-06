import pygame
import sys
import os
import math
import random

# Initialize the multimedia sub-systems
pygame.init()
pygame.mixer.init()

# Setup high-resolution simulation window matrix
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("LesbiSims: Life Simulation Engine (Dev Build)")

# Official Sims-Inspired UI Color Palette
BG_COLOR = (238, 246, 246)       # Soft cool pastel background
SIMS_BLUE = (0, 150, 214)        # Classic Sims 4 Primary UI Accent
SIMS_GREEN = (46, 204, 113)      # Full health/Happy Plumbob green
LOCKED_GREY = (127, 140, 141)    # Disabled interaction overlay color
CARD_WHITE = (255, 255, 255)     # Canvas element card faces
TEXT_DARK = (44, 62, 80)         # High contrast typography
PURPLE_ROMANCE = (155, 89, 182)  # Romance tracking gauge indicator

# Initialize Core Typography Engines
font_ui = pygame.font.SysFont("Arial", 14, bold=True)
font_header = pygame.font.SysFont("Arial", 18, bold=True)

# =====================================================================
# SIMS DATABASE & STATE ENTITY ENGINE
# =====================================================================
class LesbiSim:
    def __init__(self, name, outfit_color, x_pos):
        self.name = name
        self.outfit_color = outfit_color
        self.x = x_pos
        self.y = 350
        self.radius = 45
        self.current_animation_state = "Idle"
        self.animation_timer = 0
        
    def draw(self, surface, mouse_pos):
        # Handle subtle idle breathing movement vectors
        self.animation_timer += 0.05
        bounce_offset = math.sin(self.animation_timer) * 3 if self.current_animation_state != "Idle" else 0
        
        # Draw physical boundary asset representation
        pygame.draw.circle(surface, self.outfit_color, (self.x, int(self.y + bounce_offset)), self.radius)
        pygame.draw.circle(surface, CARD_WHITE, (self.x, int(self.y + bounce_offset)), self.radius, 3)
        
        # Render overhead Name Tags
        name_surf = font_ui.render(self.name, True, TEXT_DARK)
        surface.blit(name_surf, (self.x - name_surf.get_width() // 2, int(self.y - 75 + bounce_offset)))

# Instantiate the primary lesbian couple entities
sim_a = LesbiSim("Maya", (231, 76, 60), 450)    # Crimson red top palette
sim_b = LesbiSim("Chloe", (52, 152, 219), 650)  # Cyan blue top palette

# Global Simulation Pipeline Diagnostics
relationship_bond = 15
arousal_level = 0
active_queued_action = None
action_timer_progress = 0.0
action_duration_frames = 120 # 2 seconds at 60 FPS
telemetry_status = "Welcome to LesbiSims. Click Chloe to open the Romantic Pie Menu interaction circle."
audio_feed_status = "Audio Engine Idle"
pie_menu_is_open = False

# Interaction Metadata Setup
interaction_menu_database = [
    {"name": "Hug & Cuddle", "req_bond": 0, "sound": "sigh.wav", "gain_bond": 8, "gain_arousal": 5},
    {"name": "Kissing Loop", "req_bond": 20, "sound": "kiss.wav", "gain_bond": 12, "gain_arousal": 20},
    {"name": "Intimate Sequence", "req_bond": 50, "sound": "moan.wav", "gain_bond": 15, "gain_arousal": 35}
]

# =====================================================================
# SYSTEM AUDIO & GRAPHICS LOADER HANDLERS
# =====================================================================
def execute_vocal_cue(filename):
    """Safely plays sound clips from folder directory without crashing code."""
    global audio_feed_status
    path = os.path.join("audio", filename)
    if os.path.exists(path):
        try:
            pygame.mixer.Sound(path).play()
            audio_feed_status = f"Vocal Queue Active: audio/{filename}"
        except Exception:
            audio_feed_status = f"Audio hardware asset reading exception: {filename}"
    else:
        # Fallback simulator message logic if folder has no sound assets yet
        audio_feed_status = f"[Simulated Voice Cue Played]: '{filename[:-4].upper()}'"

# Main Application Clock Rate Regulator
clock = pygame.time.Clock()
running = True

# =====================================================================
# CORE SIMULATION ENGINE LOOP RUNTIME
# =====================================================================
while running:
    clock.tick(60) # Frame limit gating logic
    screen.fill(BG_COLOR)
    current_mouse_position = pygame.mouse.get_pos()
    
    # Check menu unlocking states instantly based on variable parameters
    for opt in interaction_menu_database:
        opt["unlocked"] = relationship_bond >= opt["req_bond"]

    # 1. READ PLAYER MOUSE & SYSTEM EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if user clicks directly on Chloe (Sim B) to open Sims 4 Choice Wheel
            distance_to_chloe = math.hypot(current_mouse_position[0] - sim_b.x, current_mouse_position[1] - sim_b.y)
            
            if distance_to_chloe <= sim_b.radius and active_queued_action is None:
                pie_menu_is_open = not pie_menu_is_open
                continue
                
            # If the radial selector is active, listen for interaction target selections
            if pie_menu_is_open:
                radial_button_clicked = False
                radius_distance = 130
                
                for idx, opt in enumerate(interaction_menu_database):
                    # Radial coordinate calculations around character origin point
                    angle_offset = idx * ((2 * math.pi) / len(interaction_menu_database)) - (math.pi / 2)
                    btn_center_x = sim_b.x + int(radius_distance * math.cos(angle_offset))
                    btn_center_y = sim_b.y + int(radius_distance * math.sin(angle_offset))
                    btn_bounding_box = pygame.Rect(btn_center_x - 75, btn_center_y - 20, 150, 40)
                    
                    if btn_bounding_box.collidepoint(current_mouse_position):
                        radial_button_clicked = True
                        if opt["unlocked"]:
                            # Lock character vectors into action routines
                            active_queued_action = opt["name"]
                            action_timer_progress = 0.0
                            sim_a.current_animation_state = opt["name"]
                            sim_b.current_animation_state = opt["name"]
                            
                            telemetry_status = f"Sims FreePlay Queue Tracking: Running {opt['name']} routine..."
                            execute_vocal_cue(opt["sound"])
                            pie_menu_is_open = False
                        else:
                            telemetry_status = f"Action Locked! Need {opt['req_bond']}% Relationship Bond to initiate."
                            
                if not radial_button_clicked:
                    pie_menu_is_open = False

    # 2. RUN SIMS FREEPLAY PROGRESSION EVENT COOLDOWNS
    if active_queued_action is not None:
        action_timer_progress += 1.0 / action_duration_frames
        
        # Force character positions to pull close together during intimate timelines
        if sim_a.x < sim_b.x - 60:
            sim_a.x += 2
        if sim_b.x > sim_a.x + 60:
            sim_b.x -= 2
            
        if action_timer_progress >= 1.0:
            # Complete event: pull metric rewards from array matrix data
            for opt in interaction_menu_database:
                if opt["name"] == active_queued_action:
                    relationship_bond = min(100, relationship_bond + opt["gain_bond"])
                    arousal_level = min(100, arousal_level + opt["gain_arousal"])
                    telemetry_status = f"Completed: {opt['name']}! Bond +{opt['gain_bond']}%, Arousal +{opt['gain_arousal']}%."
            
            # Reset actor routing states back to default values
            active_queued_action = None
            action_timer_progress = 0.0
            sim_a.current_animation_state = "Idle"
            sim_b.current_animation_state = "Idle"
    else:
        # Gradually pull characters back to their baseline relaxation nodes if idle
        if sim_a.x > 450: sim_a.x -= 2
        if sim_b.x < 650: sim_b.x += 2

    # =====================================================================
    # 3. GRAPHICS RENDERING AND LAYOUT COMPOSITION STAGE
    # =====================================================================
    # Draw Sim Actors
    sim_a.draw(screen, current_mouse_position)
    sim_b.draw(screen, current_mouse_position)
    
    # Render Sims 4 Floating Plumbob Crystal above active target interactions
    plumbob_y = sim_b.y - 65 + int(math.sin(pygame.time.get_ticks() * 0.004) * 4)
    plumbob_color = SIMS_GREEN if active_queued_action is None else (243, 156, 18)
    pygame.draw.polygon(screen, plumbob_color, [(sim_b.x, plumbob_y - 12), (sim_b.x + 8, plumbob_y), (sim_b.x, plumbob_y + 12), (sim_b.x - 8, plumbob_y)])

    # Render Sims FreePlay Style Overhead Circular Action Timer Progress
    if active_queued_action is not None:
        timer_bounding_rect = pygame.Rect(sim_b.x - 25, sim_b.y - 25, 50, 50)
        pygame.draw.arc(screen, SIMS_GREEN, timer_bounding_rect, 0, action_timer_progress * 2 * math.pi, 6)

    # Render Floating Sims 4 Translucent Radial Choice Pie Menu
    if pie_menu_is_open:
        radius_distance = 130
        for idx, opt in enumerate(interaction_menu_database):
            angle_offset = idx * ((2 * math.pi) / len(interaction_menu_database)) - (math.pi / 2)
            btn_center_x = sim_b.x + int(radius_distance * math.cos(angle_offset))
            btn_center_y = sim_b.y + int(radius_distance * math.sin(angle_offset))
            btn_bounding_box = pygame.Rect(btn_center_x - 75, btn_center_y - 20, 150, 40)
            
