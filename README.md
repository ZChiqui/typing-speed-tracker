# Typing Speed Tracker

Typing Speed Tracker is a Tkinter desktop app that measures typing accuracy and speed one word at a time. It highlights the current word, gives per-character feedback, and keeps a running words-per-minute estimate based on correct entries.

## Features
- Highlights the active word in the sentence so you always know what to type next.
- Colors each typed character green or red in real time to show correctness.
- Marks words as correct or incorrect when you press space or enter and moves forward automatically.
- Displays totals for correct and attempted words plus a live WPM score derived from correct words only.
- Includes a restart button that swaps in a new random sentence from `sentences.txt` without closing the app.

## Requirements
- Python 3.10 or later (Tkinter ships with the standard CPython installer).
- A desktop environment that supports Tkinter windows (Windows, macOS, or most Linux distros).

## Getting Started
1. (Optional) Edit `sentences.txt` to add or remove practice prompts?one sentence per line.
2. Open a terminal in the project directory.
3. Run the app:
   ```bash
   python main.py
   ```
4. Type the highlighted word. Press space (or enter) to submit the word and jump to the next one.
5. Use the **Restart** button at any time to reset stats and practice with a new random sentence.

## Project Structure
- `main.py` ? Tkinter application for the typing tracker.
- `sentences.txt` ? Word practice sentences loaded at runtime. The app falls back to a default sentence if the file is missing or empty.

## Notes
- WPM is calculated from correctly typed words since the current session start.
- If you edit `sentences.txt` while the app is running, click **Restart** to load the new content.
