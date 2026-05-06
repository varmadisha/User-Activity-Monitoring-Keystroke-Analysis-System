🛡 User Activity Monitoring & Keystroke Analysis System


📄 Description

This project is a Python-based user activity monitoring system that tracks keystrokes and analyzes user behavior in real time. It captures keyboard inputs, monitors active applications,
detects suspicious patterns, and generates logs for analysis. The system also captures screenshots and automatically sends them to Telegram for remote monitoring.


🚀 Features

🔴 Real-time keystroke logging
🖥 Active application tracking
⚠ Suspicious keyword detection (e.g., password, OTP, bank)
⚡ Fast typing behavior detection
📊 Application usage statistics
📸 Automatic screenshot capture
📤 Screenshots & logs sent directly to Telegram
📝 Log file generation and export
🎨 GUI-based monitoring dashboard (Tkinter)


🛠 Technologies Used

Python
Tkinter (GUI)
pynput (keyboard listener)
pyautogui (screenshots)
requests (Telegram API)
pygetwindow (active window tracking)


📷 How It Works

Start monitoring using the GUI
System captures keystrokes and active applications
Detects suspicious behavior (keywords / fast typing)
Takes screenshots automatically
📤 Sends screenshots and logs to Telegram bot
Saves activity logs locally


⚙ Installation

git clone https://github.com/varmadisha/User-Activity-Monitoring-Keystroke-Analysis-System
cd your-repo-name

pip install pynput pyautogui requests pygetwindow


▶ Run the Project

python main.py


🔐 Telegram Integration

Configure your BOT_TOKEN and CHAT_ID in the script
All screenshots and logs will be automatically sent to your Telegram


⚠ Disclaimer

This project is developed for educational and cybersecurity learning purposes only. Do not use it for unauthorized monitoring or unethical activities.


👩‍💻 Author

Disha Varma

📧 dishavarma910@gmail.com
