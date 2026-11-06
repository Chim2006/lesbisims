import math
import random
import os

# =====================================================================
# THE ENTIRE COMPREHENSIVE LESBI_SIMS BACKEND SYSTEM
# =====================================================================

class Character:
    def __init__(self, name, aesthetic):
        self.name = name
        self.aesthetic = aesthetic
        self.mood = "Normal"
        self.wallet = 500.0  # Starting money for furniture & rent
        self.job = "Unemployed"
        self.hourly_wage = 0.0
        
        # Track Relationship Points with other characters -> { "Name": [Friendship, Romance] }
        self.relationships = {}
        
        # Core Stats (0 to 100)
        self.needs = {"Energy": 100.0, "Affection": 50.0, "Pleasure": 0.0}
        
        # 3D Mesh Toggle Simulation Layers
        self.active_meshes = {"clothes": True, "base_nude": False}
        self.current_animation = "Idle_Standing"

    def update_needs_daily(self):
        """Simulates time drainage on character vitals."""
        self.needs["Energy"] = max(0.0, self.needs["Energy"] - 25.0)
        self.needs["Affection"] = max(0.0, self.needs["Affection"] - 15.0)
        if self.needs["Affection"] < 20.0:
            self.mood = "Lonely"

    def strip(self):
        self.active_meshes["clothes"] = False
        self.active_meshes["base_nude"] = True

    def dress(self):
        self.active_meshes["clothes"] = True
        self.active_meshes["base_nude"] = False


class BuildGrid:
    def __init__(self):
        self.size = 5
        self.grid = [[" . " for _ in range(self.size)] for _ in range(self.size)]

    def place_item(self, item, rx, rz):
        cx = math.floor(rx)
        cz = math.floor(rz)
        if 0 <= cx < self.size and 0 <= cz < self.size:
            if self.grid[cz][cx] == " . ":
                self.grid[cz][cx] = f"[{item[:2].upper()}]"
                return True
        return False

    def display(self):
        print("\n🏡 --- CURRENT ROOM LAYOUT SYSTEM ---")
        for row in self.grid:
            print(" ".join(row))


class LesbiSimsGame:
    def __init__(self):
        self.day = 1
        self.game_mode = "LIVE"  # LIVE or BUILD
        self.player = Character("Chloe", "Alt-Goth")
        self.partner = Character("Rachel", "Femme-Cottagecore")
        self.world_grid = BuildGrid()
        
        # Boot configuration
        self.player.relationships[self.partner.name] = [30.0, 10.0]

    def process_work(self):
        if self.player.job == "Unemployed":
            print("❌ You don't have a job yet! Apply for one first.")
            return
        earned = self.player.hourly_wage * 8
        self.player.wallet += earned
        self.player.needs["Energy"] = max(0.0, self.player.needs["Energy"] - 40.0)
        print(f"💼 Worked an 8-hour shift as a {self.player.job}! Earned ${earned:.2f}.")

    def process_social(self, choice_type):
        p_rel = self.player.relationships[self.partner.name]
        
        if choice_type == "1":  # Chat
            p_rel[0] = min(100.0, p_rel[0] + 15.0)
            self.player.needs["Affection"] = min(100.0, self.player.needs["Affection"] + 10.0)
            print(f"💬 You talked about music and art with {self.partner.name}. Friendship is now {p_rel[0]}.")
            
        elif choice_type == "2":  # Flirt
            if p_rel[0] >= 40.0:
                p_rel[1] = min(100.0, p_rel[1] + 20.0)
                self.player.mood = "Lovestruck"
                print(f"💋 Flirting was successful! Romantic chemistry rose to {p_rel[1]}.")
            else:
                p_rel[1] = max(0.0, p_rel[1] - 10.0)
                print(f"😳 Awkward silence. You need a higher friendship level before flirting.")
                
        elif choice_type == "3":  # Uncensored Lesbian Sex
            if p_rel[1] >= 75.0:
                print(f"\n🔥 [TRIGGERING ADULT ANIMATION SEQUENCE]")
                self.player.strip()
                self.partner.strip()
                self.player.current_animation = "Scissoring_Active_A"
                self.partner.current_animation = "Scissoring_Active_B"
                
                # Update Needs values
                self.player.needs["Pleasure"] = 100.0
                self.player.needs["Affection"] = 100.0
                self.player.needs["Energy"] = max(10.0, self.player.needs["Energy"] - 30.0)
                
                print(" -> Skeletons aligned to Bed Anchor Matrix node.")
                print(" -> Playing explicit, uncensored physical intimacy tracks loops.")
                print(" -> Both characters reached maximum pleasure satisfaction values!")
                
                # End sequence instantly for loop stability
                self.player.dress()
                self.partner.dress()
            else:
                print(f"🛑 REJECTED! Romantic chemistry ({p_rel[1]}/75) is too low for physical intimacy.")

    def run_main_loop(self):
        while True:
            print(f"\n====================================================")
            print(f"📆 DAY: {self.day} | MODE: {self.game_mode} | Funds: ${self.player.wallet:.2f}")
            print(f"👤 Job: {self.player.job} | Mood: {self.player.mood}")
            print(f"📊 Stats -> Energy: {self.player.needs['Energy']}% | Affection: {self.player.needs['Affection']}% | Pleasure: {self.player.needs['Pleasure']}%")
            print(f"💕 Partner Relationship -> Friendship: {self.player.relationships[self.partner.name][0]} | Romance: {self.player.relationships[self.partner.name][1]}")
            print(f"====================================================")
            
            if self.game_mode == "LIVE":
                print("1. Go to Work (Earn Money)")
                print("2. Interact with Partner (Rachel)")
                print("3. Apply for Job (Barista - $15/hr)")
                print("4. Switch to Build/Buy Mode")
                print("5. Sleep & Advance to Next Day")
                print("6. Quit Game")
                
                cmd = input("\nAction Selection: ")
                if cmd == "1": self.process_work()
                elif cmd == "2":
                    print("\nSelect Intimacy Option:")
                    print("  1) Chat Platonically")
                    print("  2) Flirt Romantically")
                    print("  3) Initiate Intimate Lesbian Sex (WooHoo)")
                    sub_cmd = input("  Choice: ")
                    self.process_social(sub_cmd)
                elif cmd == "3":
                    self.player.job = "Barista"
                    self.player.hourly_wage = 15.0
                    print("☕ Hired! You are now a Barista at the local queer cafe.")
                elif cmd == "4":
                    self.game_mode = "BUILD"
                elif cmd == "5":
                    # Day advance mechanics
                    self.day += 1
                    self.player.needs["Energy"] = 100.0  # Restored by sleep
                    self.player.update_needs_daily()
                    self.player.wallet -= 50.0  # Daily cost of house rent deduction
                    print("\n💤 Sleeping... Rent deducted ($50.00). Energy restored!")
                elif cmd == "6":
                    break
                    
            elif self.game_mode == "BUILD":
                self.world_grid.display()
                print("\n1. Buy & Place Double Bed ($250, Position: 2, 2)")
                print("2. Buy & Place Lesbian Pride Flag ($50, Position: 0, 4)")
                print("3. Return to Live Mode")
                
                b_cmd = input("\nBuild Choice: ")
                if b_cmd == "1":
                    if self.player.wallet >= 250:
                        if self.world_grid.place_item("Bed", 2.2, 2.8):
                            self.player.wallet -= 250
                            print("🧱 Placed Double Bed!")
                        else: print("❌ Grid space blocked!")
                    else: print("❌ Poor funds!")
                elif b_cmd == "2":
                    if self.player.wallet >= 50:
                        if self.world_grid.place_item("Flag", 0.1, 4.2):
                            self.player.wallet -= 50
                            print("🧱 Placed Pride Flag!")
                        else: print("❌ Grid space blocked!")
                    else: print("❌ Poor funds!")
                elif b_cmd == "3":
                    self.game_mode = "LIVE"

# =====================================================================
# SYSTEM EXECUTION TRIGGER
# =====================================================================
if __name__ == "__main__":
    game_instance = LesbiSimsGame()
    game_instance.run_main_loop()
