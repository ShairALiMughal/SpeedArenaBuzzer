import customtkinter as ctk
from tkinter import Label, Toplevel
from PIL import Image, ImageTk
import pygame
from nslbuzzerfunctionality import NSLBuzzerFunctionality

class TimeDisplay(Toplevel):
    def __init__(self, master, game_name):
        super().__init__(master)
        self.title(f"NSL Timer Display - {game_name}")
        self.configure(bg="black")
        self.geometry("1000x700")  # Increased size for better visibility

        # Create a frame with a white border
        self.border_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.border_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.inner_frame = ctk.CTkFrame(self.border_frame, fg_color="black", corner_radius=0)
        self.inner_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Timer label
        self.timer_label = Label(self.inner_frame, text="10:00", font=("Vani", 300, "bold"), bg="black", fg="white")
        self.timer_label.pack(expand=True)

        # Load logos
        speed_arena_logo = Image.open("speed_arena_logo.png")
        nsl_logo = Image.open("nsl_logo.png")

        speed_arena_logo = speed_arena_logo.resize((200, 170))  # Slightly increased size
        nsl_logo = nsl_logo.resize((200, 170))  # Slightly increased size

        self.speed_arena_img = ImageTk.PhotoImage(speed_arena_logo)
        self.nsl_img = ImageTk.PhotoImage(nsl_logo)

        # Create a frame for logos and game number
        self.logo_frame = ctk.CTkFrame(self.inner_frame, fg_color="black")
        self.logo_frame.pack(side="bottom", fill="x", pady=20)

        # Add logos and game number to the logo frame
        speed_arena_label = Label(self.logo_frame, image=self.speed_arena_img, bg="black")
        speed_arena_label.pack(side="left", expand=True)

        self.game_label = Label(self.logo_frame, text=game_name, font=("Vani", 24, "bold"), bg="black", fg="white")
        self.game_label.pack(side="left", expand=True)

        nsl_label = Label(self.logo_frame, image=self.nsl_img, bg="black")
        nsl_label.pack(side="left", expand=True)

    def update_time(self, time_str):
        self.timer_label.config(text=time_str)

class NSLBuzzerGUI:
    def __init__(self, root, game_name):
        self.app = root
        self.game_name = game_name
        self.frame = None

        pygame.mixer.init()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.time_display = TimeDisplay(self.app, game_name)
        self.functionality = NSLBuzzerFunctionality(self.update_timer_display)

        self.setup_frame()
        self.setup_timer_frame()
        self.setup_buttons()

        self.feet_sound = "feet.mp3"
        self.weapon_sound = "weapon.mp3"
        self.start_timer_sound = "POPPP.mp3"

    def setup_frame(self):
        self.frame = ctk.CTkFrame(self.app, width=1000, height=600, fg_color="#1E1E1E")  # Darker background
        self.frame.pack_propagate(0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

    def setup_timer_frame(self):
        self.timer_frame = ctk.CTkFrame(self.frame, width=900, height=450, fg_color="#2C2C2C", corner_radius=15)  # Slightly lighter than background
        self.timer_frame.place(relx=0.5, rely=0.2, anchor="center")

        self.game_label = Label(self.timer_frame, text=self.game_name, font=("Vani", 24, "bold"), bg="#2C2C2C", fg="white")
        self.game_label.place(relx=0.5, rely=0.1, anchor="center")

        self.timer_label = Label(self.timer_frame, text="10:00", font=("Vani", 250, "bold"), bg="#2C2C2C", fg="white")
        self.timer_label.place(relx=0.5, rely=0.5, anchor="center")

        # Load logos
        speed_arena_logo = Image.open("speed_arena_logo.png")
        nsl_logo = Image.open("nsl_logo.png")

        speed_arena_logo = speed_arena_logo.resize((180, 150))
        nsl_logo = nsl_logo.resize((180, 150))

        self.speed_arena_img = ImageTk.PhotoImage(speed_arena_logo)
        self.nsl_img = ImageTk.PhotoImage(nsl_logo)

        speed_arena_label = Label(self.timer_frame, image=self.speed_arena_img, bg="#2C2C2C")
        speed_arena_label.place(relx=0.25, rely=0.85, anchor="center")

        nsl_label = Label(self.timer_frame, image=self.nsl_img, bg="#2C2C2C")
        nsl_label.place(relx=0.75, rely=0.85, anchor="center")

    def setup_buttons(self):
        button_configs = [
            ("30 Sec", 0.05, 0.65, "blue", self.functionality.set_30_seconds),
            ("10 Min", 0.05, 0.72, "blue", self.functionality.set_10_minutes),
            ("15 Min", 0.05, 0.79, "blue", self.functionality.set_15_minutes),
            ("Start Match", 0.25, 0.65, "green", self.start_match_sequence),
            ("New Match", 0.4, 0.65, "cyan", self.functionality.new_match),
            ("Stop Match", 0.25, 0.72, "orange", self.functionality.stop_match),
            ("Pause Timer", 0.4, 0.72, "orange", self.functionality.pause_timer),
            ("Game 1", 0.7, 0.65, "pink", lambda: switch_game("Game 1")),
            ("Game 2", 0.85, 0.65, "pink", lambda: switch_game("Game 2")),
            ("Game 3", 0.7, 0.72, "pink", lambda: switch_game("Game 3")),
            ("Flag Hang 1v1", 0.85, 0.72, "green", self.functionality.flag_hang_1v1),
            ("1v1", 0.7, 0.79, "green", self.functionality.one_v_one),
            ("Zone 1", 0.85, 0.79, "red", self.functionality.zone_1),
            ("Zone 2", 0.7, 0.86, "red", self.functionality.zone_2),
            ("Zone 3", 0.85, 0.86, "red", self.functionality.zone_3)
        ]

        for text, x, y, color, command in button_configs:
            button = ctk.CTkButton(
                self.frame, text=text, fg_color=color, width=120, height=40, corner_radius=10, 
                command=command, font=("Arial", 12, "bold")
            )
            button.place(relx=x, rely=y, anchor="center")

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def start_match_sequence(self):
        self.timer_label.config(text="FEET", font=("Vani", 250, "bold"))
        self.time_display.timer_label.config(text="FEET", font=("Vani", 300, "bold"))
        self.play_sound(self.feet_sound)
        self.app.after(6000, self.show_weapon)

    def show_weapon(self):
        self.timer_label.config(text="WEAPON", font=("Vani", 180, "bold"))
        self.time_display.timer_label.config(text="WEAPON", font=("Vani", 220, "bold"))
        self.play_sound(self.weapon_sound)
        self.app.after(6000, self.start_timer)

    def start_timer(self):
        self.timer_label.config(font=("Vani", 250, "bold"))
        self.time_display.timer_label.config(font=("Vani", 300, "bold"))
        self.play_sound(self.start_timer_sound)
        self.functionality.start_match()

    def update_timer_display(self, time_str):
        self.app.after(0, self.timer_label.config, {"text": time_str})
        self.app.after(0, self.time_display.update_time, time_str)

    def show(self):
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

# Store the game instances
game_instances = {}

def switch_game(game_name):
    for instance in game_instances.values():
        instance.hide()
    game_instances[game_name].show()

def main():
    root = ctk.CTk()
    root.title("NSL Buzzer System")
    root.geometry("1000x600")

    # Create three game instances
    game_instances["Game 1"] = NSLBuzzerGUI(root, "Game 1")
    game_instances["Game 2"] = NSLBuzzerGUI(root, "Game 2")
    game_instances["Game 3"] = NSLBuzzerGUI(root, "Game 3")

    # Position the time display windows
    game_instances["Game 1"].time_display.geometry("+0+0")  # Top-left corner
    game_instances["Game 2"].time_display.geometry("+960+0")  # Top-right corner
    game_instances["Game 3"].time_display.geometry("+480+740")  # Bottom-center

    # Initially show Game 1 controls
    game_instances["Game 1"].show()
    game_instances["Game 2"].hide()
    game_instances["Game 3"].hide()

    game_instances["Game 2"].show()
    game_instances["Game 1"].hide()
    game_instances["Game 3"].hide()

    game_instances["Game 3"].show()
    game_instances["Game 1"].hide()
    game_instances["Game 2"].hide()

    game_instances["Game 1"].show()
    game_instances["Game 2"].hide()
    game_instances["Game 3"].hide()
    
    root.mainloop()

if __name__ == "__main__":
    main()