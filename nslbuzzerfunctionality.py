import time
import threading

class NSLBuzzerFunctionality:
    def __init__(self, update_display_callback):
        self.update_display = update_display_callback
        self.timer_running = False
        self.timer_paused = False
        self.current_time = 600  # 10 minutes in seconds
        self.timer_thread = None

    def update_timer(self):
        while self.timer_running:
            if not self.timer_paused:
                self.current_time -= 1
                if self.current_time <= 0:
                    self.current_time = 0
                    self.timer_running = False
                
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

    def set_10_minutes(self):
        self.current_time = 600
        self.update_display_time()

    def set_15_minutes(self):
        self.current_time = 900
        self.update_display_time()

    def start_match(self):
        if not self.timer_running:
            self.timer_running = True
            self.timer_paused = False
            self.timer_thread = threading.Thread(target=self.update_timer)
            self.timer_thread.daemon = True
            self.timer_thread.start()

    def new_match(self):
        self.stop_match()
        self.current_time = 600
        self.update_display_time()

    def stop_match(self):
        self.timer_running = False
        self.timer_paused = False
        if self.timer_thread:
            self.timer_thread.join()

    def pause_timer(self):
        self.timer_paused = not self.timer_paused

    def flag_hang_1v1(self):
        # Implement Flag Hang 1v1 specific logic
        pass

    def one_v_one(self):
        # Implement 1v1 specific logic
        pass

    def zone_1(self):
        # Implement Zone 1 specific logic
        pass

    def zone_2(self):
        # Implement Zone 2 specific logic
        pass

    def zone_3(self):
        # Implement Zone 3 specific logic
        pass