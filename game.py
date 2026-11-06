import time
import random

class SimsCharacter:
    def __init__(self, name):
        self.name = name
        self.current_state = "Idle"
        self.arousal_level = 0
        self.relationship_score = 100

    def play_animation(self, anim_name):
        print(f"[{self.name}] Playing animation visual: '{anim_name}'")

    def play_audio(self, sound_type):
        # Simulates playing the voice track/vocalizations
        variations = ["soft", "intense", "gentle"]
        tone = random.choice(variations)
        print(f"🔊 AUDIO TRIGGERED: [{self.name}] playing vocalization ({sound_type}_{tone})")


class InteractionManager:
    def __init__(self, sim1, sim2):
        self.sim1 = sim1
        self.sim2 = sim2
        self.active_interaction = None

    def start_interaction(self, interaction_type):
        print(f"\n--- Starting Interaction: {interaction_type.upper()} ---")
        self.active_interaction = interaction_type
        
        if interaction_type == "hug_cuddle":
            self._execute_hug_cuddle()
        elif interaction_type == "kissing":
            self._execute_kissing()
        elif interaction_type == "intimate_cuddle":
            self._execute_intimate_cuddle()
        else:
            print("Unknown interaction.")

    def _execute_hug_cuddle(self):
        # Step 1: Sync positions and play base cuddle loop
        self.sim1.current_state = "Cuddling"
        self.sim2.current_state = "Cuddling"
        
        self.sim1.play_animation("cuddle_pose_alpha")
        self.sim2.play_animation("cuddle_pose_beta")
        time.sleep(1)  # Simulating game loop time

    def _execute_kissing(self):
        self.sim1.current_state = "Kissing"
        self.sim2.current_state = "Kissing"
        
        # Loop the kissing animation sequence
        for i in range(2):
            print(f"\n[Timeline Loop {i+1}]")
            self.sim1.play_animation("kiss_loop_active")
            self.sim2.play_animation("kiss_loop_passive")
            
            # Synchronize vocalizations with the physical contact markers
            time.sleep(0.5)
            self.sim1.play_audio("kiss_moan")
            self.sim2.play_audio("sigh_vocal")
            time.sleep(1.0)

    def _execute_intimate_cuddle(self):
        # Represents the close-contact leg-locking / scissoring positioning
        self.sim1.current_state = "Intimate_Scissoring"
        self.sim2.current_state = "Intimate_Scissoring"
        
        # Trigger the complex paired animations
        self.sim1.play_animation("scissoring_position_driver")
        self.sim2.play_animation("scissoring_position_receiver")
        
        # Intimacy loop handles continuous escalation and audio sync
        for tick in range(3):
            print(f"\n[Intimacy Animation Tick {tick+1}]")
            # Increase variables to change game state dynamically
            self.sim1.arousal_level += 20
            self.sim2.arousal_level += 20
            
            # Multi-layered audio triggers based on the execution phase
            if tick == 0:
                self.sim1.play_audio("heavy_breathing")
            else:
                self.sim1.play_audio("intense_moan")
                self.sim2.play_audio("intense_moan")
            
            time.sleep(1.5)

        # Wind down interaction
        print("\n--- Interaction Transitioning to Rest ---")
        self.sim1.current_state = "Idle"
        self.sim2.current_state = "Idle"


# --- GAME EXECUTION SIMULATION ---
if __name__ == "__main__":
    # Create the two characters
    character_a = SimsCharacter("Maya")
    character_b = SimsCharacter("Chloe")
    
    # Initialize the engine's interaction manager
    engine = InteractionManager(character_a, character_b)
    
    # Run the sequence progression
    engine.start_interaction("hug_cuddle")
    engine.start_interaction("kissing")
    engine.start_interaction("intimate_cuddle")
