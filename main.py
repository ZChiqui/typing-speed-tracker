from pathlib import Path
from typing_speed_tracker import TypingSpeedTracker
from helpers import load_sentences
import random

SENTENCES_PATH = Path("sentences.txt")
SENTENCES = load_sentences(SENTENCES_PATH)

if __name__ == "__main__":
    app = TypingSpeedTracker(SENTENCES)
    app.mainloop()
