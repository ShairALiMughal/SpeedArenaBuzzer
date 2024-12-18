import time
import threading
import pygame

# Sound file constants
zon1 = "Zone1.mp3"
zon2 = "Zone2.mp3"
zon3 = "Zone3.mp3"
sound1v1 = "1v1.mp3"
flaghang = "FlagHang.mp3"
flaghang1v1 = "FlagHang1v1.mp3"
snatch = "Snatch.mp3"
horn_sound = "hornx3.mp3"  # Added horn sound constant

class NSLBuzzerFunctionality:
    def __init__(self, update_display_callback):
        self.update_display = update_display_callback
        self.timer_running = False
        self.timer_paused = False
        self.current_time = 600  # 10 minutes in seconds
        self.timer_thread = None
        self.current_game = None

    def update_timer(self):
        while self.timer_running:
            if not self.timer_paused:
                self.current_time -= 1
                if self.current_time <= 0:
                    self.current_time = 0
                    self.timer_running = False
                    self.play_sound(horn_sound)  # Play horn sound when timer ends
                
                self.update_display_time()
                
            time.sleep(1)

    def update_display_time(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        self.update_display(time_str)

    def set_30_seconds(self):
        self.current_time = 30
        self.update_display_time()
        self.timer_running = False

    def set_5_minutes(self):
        self.current_time = 300
        self.update_display_time()
        self.timer_running = False

    def set_10_minutes(self):
        self.current_time = 600
        self.update_display_time()
        self.timer_running = False

    def set_15_minutes(self):
        self.current_time = 900
        self.update_display_time()
        self.timer_running = False

    def start_match(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_paused = False
            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def stop_match(self, skip_horn=False):
        """
        Stops the match timer
        Args:
            skip_horn (bool): If True, doesn't play the horn sound
        """
        self.timer_running = False
        self.timer_paused = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join(timeout=1.0)
        if not skip_horn:  # Only play horn if not skipped
            self.play_sound(horn_sound)

    def pause_timer(self):
        self.timer_paused = not self.timer_paused

    def new_match(self):
        self.stop_match()
        self.current_time = 600
        self.update_display_time()

    def play_sound(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

    def play_sound_with_delay(self, initial_sound, delay_sound, delay):
        """
        Plays an initial sound and then plays a delayed sound after specified seconds
        """
        self.play_sound(initial_sound)
        timer = threading.Timer(delay, lambda: self.play_sound(delay_sound))
        timer.daemon = True
        timer.start()

    def flag_hang_1v1(self):
        self.play_sound(sound_file=flaghang1v1)
        self.current_game = "Flag Hang 1v1"
    
    def snatch(self):
        self.play_sound(sound_file=snatch)
        self.current_game = "Snatch"

    def hang_1v1(self):
        self.play_sound(sound_file=flaghang)
        self.current_game = "Hang 1v1"

    def one_v_one(self):
        self.play_sound(sound_file=sound1v1)
        self.current_game = "1v1"

    def zone_1(self):
        self.play_sound(sound_file=zon1)
        self.current_game = "Zone 1"
        
    def zone_2(self):
        self.play_sound(sound_file=zon2)
        self.current_game = "Zone 2"

    def zone_3(self):
        self.play_sound(sound_file=zon3)
        self.current_game = "Zone 3"
        
    def get_current_time_str(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        return f"{minutes:02d}:{seconds:02d}"