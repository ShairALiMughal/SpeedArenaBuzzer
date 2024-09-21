import customtkinter as ctk
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
import pygame
from nslbuzzerfunctionality import NSLBuzzerFunctionality

class TimeDisplay(Toplevel):
    def __init__(self, master, game_name):
        super().__init__(master)
        self.title(f"NSL Timer Display - {game_name}")
        self.configure(bg="#1E1E1E")
        self.geometry("1000x700")  # Increased size for better visibility

        self.border_frame = ctk.CTkFrame(self, fg_color="#2C2C2C", corner_radius=10)
        self.border_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.inner_frame = ctk.CTkFrame(self.border_frame, fg_color="#1E1E1E", corner_radius=10)
        self.inner_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.timer_label = Label(self.inner_frame, text="10:00", font=("Roboto", 300, "bold"), bg="#1E1E1E", fg="#FFFFFF")
        self.timer_label.pack(expand=True)

        # Load and resize logos
        speed_arena_logo = Image.open("speed_arena_logo.png").resize((200, 170))
        nsl_logo = Image.open("nsl_logo.png").resize((200, 170))

        self.speed_arena_img = ImageTk.PhotoImage(speed_arena_logo)
        self.nsl_img = ImageTk.PhotoImage(nsl_logo)

        # Create a frame for logos and game name
        logo_frame = ctk.CTkFrame(self.inner_frame, fg_color="#1E1E1E")
        logo_frame.pack(side="bottom", fill="x", pady=20)

        # Add logos and game name to the logo frame
        speed_arena_label = Label(logo_frame, image=self.speed_arena_img, bg="#1E1E1E")
        speed_arena_label.pack(side="left", expand=True)

        self.game_label = Label(logo_frame, text=game_name, font=("Roboto", 40, "bold"), bg="#1E1E1E", fg="#FFFFFF")
        self.game_label.pack(side="left", expand=True)

        nsl_label = Label(logo_frame, image=self.nsl_img, bg="#1E1E1E")
        nsl_label.pack(side="right", expand=True)

    def update_time(self, time_str):
        self.timer_label.config(text=time_str)

class NSLBuzzerGUI:
    def __init__(self, root, game_name):
        self.app = root
        self.game_name = game_name
        self.frame = None
        self.team1_pressed = False
        self.team2_pressed = False
        self.message_label = None
        self.extra_20_sec = ctk.BooleanVar()
        self.extra_time_countdown = 20

        pygame.mixer.init()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.time_display = TimeDisplay(self.app, game_name)
        self.functionality = NSLBuzzerFunctionality(self.update_timer_display)

        self.setup_frame()
        self.setup_timer_frame()
        self.setup_buttons()
        self.setup_extra_time_checkbox()

        self.feet_sound = "feet.mp3"
        self.weapon_sound = "weapon.mp3"
        self.start_timer_sound = "POPPP.mp3"

    def setup_frame(self):
        self.frame = ctk.CTkFrame(self.app, width=1000, height=600, fg_color="#1E1E1E")
        self.frame.pack_propagate(0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def setup_timer_frame(self):
        self.timer_frame = ctk.CTkFrame(self.frame, width=900, height=300, fg_color="#2C2C2C", corner_radius=15)
        self.timer_frame.place(relx=0.5, rely=0.25, anchor="center")

        self.timer_label = Label(self.timer_frame, text="10:00", font=("Roboto", 150, "bold"), bg="#2C2C2C", fg="#FFFFFF")
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")

    def setup_buttons(self):
        button_configs = [
        # Timer controls
        ("30s", 0.10, 0.55, "#4CAF50"),
        ("10m", 0.25, 0.55, "#2196F3"),
        ("15m", 0.40, 0.55, "#9C27B0"),
        
        # Match controls
        ("Start", 0.60, 0.55, "#4CAF50"),
        ("Stop", 0.75, 0.55, "#F44336"),
        ("Pause", 0.90, 0.55, "#FF9800"),
        
        # Game selection
        ("Game 1", 0.20, 0.65, "#E91E63"),
        ("Game 2", 0.40, 0.65, "#E91E63"),
        ("Game 3", 0.60, 0.65, "#E91E63"),
        ("New", 0.80, 0.65, "#00BCD4"),
        
        # Game modes
        ("Flag 1v1", 0.20, 0.75, "#009688"),
        ("1v1", 0.40, 0.75, "#009688"),
        ("Zone 1", 0.60, 0.75, "#FF5722"),
        ("Zone 2", 0.75, 0.75, "#FF5722"),
        ("Zone 3", 0.90, 0.75, "#FF5722"),
        
        # Team controls
        ("Team 1", 0.30, 0.85, "#E53935"),
        ("Team 2", 0.70, 0.85, "#1E88E5")
        ]

        for text, x, y, color in button_configs:
            button = ctk.CTkButton(
                self.frame, text=text, fg_color=color, width=100, height=40, corner_radius=20,
                command=self.get_button_command(text), font=("Roboto", 14, "bold")
            )
            button.place(relx=x, rely=y, anchor="center")

        # Add message label with a background
        message_frame = ctk.CTkFrame(self.frame, fg_color="#2C2C2C", corner_radius=10, width=800, height=40)
        message_frame.place(relx=0.5, rely=0.95, anchor="center")

        self.message_label = Label(message_frame, text="", font=("Roboto", 14), bg="#2C2C2C", fg="#FFFFFF")
        self.message_label.place(relx=0.5, rely=0.5, anchor="center")

        # Bind keyboard keys
        self.app.bind('1', lambda event: self.team_button_pressed(1))
        self.app.bind('2', lambda event: self.team_button_pressed(2))

    def get_button_command(self, text):
        commands = {
            "30s": self.functionality.set_30_seconds,
            "10m": self.functionality.set_10_minutes,
            "15m": self.functionality.set_15_minutes,
            "Start": self.start_match_sequence,
            "Stop": self.functionality.stop_match,
            "Pause": self.functionality.pause_timer,
            "New": self.new_match,
            "Flag 1v1": self.functionality.flag_hang_1v1,
            "1v1": self.functionality.one_v_one,
            "Zone 1": self.functionality.zone_1,
            "Zone 2": self.functionality.zone_2,
            "Zone 3": self.functionality.zone_3,
            "Team 1": lambda: self.team_button_pressed(1),
            "Team 2": lambda: self.team_button_pressed(2)
        }
        return commands.get(text, lambda: switch_game(text))

    def setup_extra_time_checkbox(self):
        self.extra_time_checkbox = ctk.CTkCheckBox(
            self.frame, text="Extra 20 sec", variable=self.extra_20_sec,
            font=("Roboto", 14), fg_color="#4CAF50", hover_color="#45a049"
        )
        self.extra_time_checkbox.place(relx=0.5, rely=0.45, anchor="center")
    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def start_match_sequence(self):
        if self.extra_20_sec.get():
            self.extra_time_countdown = 20
            self.update_extra_time_display()
        else:
            self.show_feet()
    def update_extra_time_display(self):
        if self.extra_time_countdown > 0:
            self.timer_label.config(text=f"{self.extra_time_countdown}", font=("Vani", 250, "bold"))
            self.time_display.timer_label.config(text=f"{self.extra_time_countdown}", font=("Vani", 250, "bold"))
            self.extra_time_countdown -= 1
            self.app.after(1000, self.update_extra_time_display)
        else:
            self.show_feet()

    def show_feet(self):
        self.timer_label.config(text="FEET", font=("Vani", 250, "bold"))
        self.time_display.timer_label.config(text="FEET", font=("Vani", 250, "bold"))
        self.play_sound(self.feet_sound)
        self.app.after(6000, self.show_weapon)

    def show_weapon(self):
        self.timer_label.config(text="WEAPON", font=("Vani", 180, "bold"))
        self.time_display.timer_label.config(text="WEAPON", font=("Vani", 180, "bold"))
        self.play_sound(self.weapon_sound)
        self.app.after(6000, self.start_timer)

    def start_timer(self):
        self.timer_label.config(font=("Vani", 250, "bold"))
        self.time_display.timer_label.config(font=("Vani", 250, "bold"))
        self.play_sound(self.start_timer_sound)
        self.functionality.start_match()

    def update_timer_display(self, time_str):
        self.app.after(0, self.timer_label.config, {"text": time_str})
        self.app.after(0, self.time_display.update_time, time_str)

    def show(self):
        self.frame.pack()
        self.time_display.deiconify()

    def hide(self):
        self.frame.pack_forget()
        self.time_display.withdraw()
    
    def team_button_pressed(self, team):
        if not self.functionality.timer_running:
            return

        current_time = self.functionality.get_current_time_str()
        
        if team == 1 and not self.team1_pressed:
            self.team1_pressed = True
            self.functionality.stop_match()
            message = f"Team 1 pressed the button at {current_time}"
            if self.team2_pressed:
                message += f" after Team 2"
            self.message_label.config(text=message)
        elif team == 2 and not self.team2_pressed:
            self.team2_pressed = True
            self.functionality.stop_match()
            message = f"Team 2 pressed the button at {current_time}"
            if self.team1_pressed:
                message += f" after Team 1"
            self.message_label.config(text=message)

    def new_match(self):
        self.functionality.new_match()
        self.team1_pressed = False
        self.team2_pressed = False
        self.message_label.config(text="")
        self.extra_20_sec.set(False)

# Store the game instances
game_instances = {}

def switch_game(game_name):
    for game_instance in game_instances.values():
        game_instance.hide()
    game_instances[game_name].show()

def main():
    root = ctk.CTk()
    root.title("NSL Buzzer System")
    root.geometry("1000x600")

    # Create game instances
    game_instances["Game 1"] = NSLBuzzerGUI(root, "Game 1")
    game_instances["Game 2"] = NSLBuzzerGUI(root, "Game 2")
    game_instances["Game 3"] = NSLBuzzerGUI(root, "Game 3")
   

    game_instances["Game 2"].show()
    game_instances["Game 1"].hide()
    game_instances["Game 3"].hide()

    game_instances["Game 3"].show()
    game_instances["Game 1"].hide()
    game_instances["Game 2"].hide()

    # Initially show Game 1
    game_instances["Game 1"].show()
    game_instances["Game 2"].hide()
    game_instances["Game 3"].hide()


    root.mainloop()

if __name__ == "__main__":
    main()