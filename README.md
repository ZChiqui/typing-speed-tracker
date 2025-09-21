# Typing Speed Tracker

Typing Speed Tracker is a Tkinter desktop application for practicing typing accuracy and speed. It highlights individual words, provides per-character feedback, and tracks words-per-minute based on correct entries.

## Features
- Dark themed interface with a dedicated feedback panel that shows typed characters in green or red as you type.
- Highlights the active word in the sentence, updates automatically after each submission, and marks completed words as correct or incorrect.
- Starts timing on the first keystroke and keeps live totals for correct words, total attempts, and WPM (correct words only).
- Accepts space or enter to submit the current word and gracefully ignores accidental blank submissions.
- Restart button instantly loads a new random sentence from `sentences.txt`, resets stats, and re-enables typing without restarting the program.

## Requirements
- Python 3.10 or later (Tkinter ships with the standard CPython installer).
- A desktop environment that supports Tkinter windows (Windows, macOS, or most Linux distros).

## Getting Started
1. (Optional) Edit `sentences.txt` to add or remove practice prompts; use one sentence per line.
2. Open a terminal in the project directory.
3. Run the app:
   ```bash
   python main.py
   ```
4. Type the highlighted word. Press space (or enter) to submit the word and jump to the next one.
5. Use the **Restart** button at any time to reset stats and practice with a new random sentence.

## Project Structure
- `main.py` entry point that loads sentences and launches the GUI.
- `typing_speed_tracker.py` Tkinter implementation of the typing trainer UI and session logic.
- `helpers.py` utility for loading sentences with a safe fallback when the file is missing or empty.
- `sentences.txt` practice sentences loaded at runtime.

## Customization Tips
- Update fonts, colors, or layout by editing the widget configuration in `typing_speed_tracker.py`.
- Supply your own practice material by replacing or expanding the lines in `sentences.txt`.

## Notes
- WPM is calculated from correctly typed words since the current session start.
- If you edit `sentences.txt` while the app is running, click **Restart** to load the new content.
