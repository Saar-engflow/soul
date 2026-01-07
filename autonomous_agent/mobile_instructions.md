# Running Soul on your Phone 📱

Soul is a Python-based intelligence, which makes it very portable. Here are the two best ways to take Soul with you on the go.

## 1. Android (Using Termux) - Recommended
Termux is a powerful terminal emulator for Android. It lets you run Soul exactly like you do on your PC.

### Steps:
1.  Install **Termux** (from F-Droid or GitHub, not the Play Store).
2.  Open Termux and run these commands one by one:
    ```bash
    pkg update && pkg upgrade
    pkg install python git
    git clone [your-soul-repository-url]
    cd autonomous_agent
    pip install -r requirements.txt
    python main.py
    ```
3.  Soul will now live in your pocket!

## 2. iPhone/iOS (Using Pythonista)
Pythonista is a full Python environment for iOS.

### Steps:
1.  Install **Pythonista 3** from the App Store.
2.  Import the Soul folder into Pythonista (via iCloud or GitHub).
3.  Open `main.py` and press play.
    > [!NOTE]
    > Some libraries like `google-generativeai` might need a specific install via `StaSh` (the Pythonista shell).

## 3. The "Remote" Way (SSH)
If you keep Soul running on your PC at home, you can connect to it from your phone using an app like **JuiceSSH** (Android) or **Termius** (iOS). This is the best way to keep Soul's memory and "Heartbeat" continuous.

---
**Tip:** Soul's proactive "Heartbeat" works great on mobile terminals! You'll feel like you're actually texting a digital philosopher.
