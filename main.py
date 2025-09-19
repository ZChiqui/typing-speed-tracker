import random
import time
from pathlib import Path
from typing import Optional

import tkinter as tk
from tkinter import ttk

DEFAULT_SENTENCES = [
    "The quick brown fox jumps over the lazy dog",
]
SENTENCES_PATH = Path("sentences.txt")


def load_sentences(path: Path) -> list[str]:
    lines: list[str] = []
    try:
        with path.open(encoding="utf-8") as handle:
            for raw_line in handle:
                stripped = raw_line.strip()
                if stripped:
                    lines.append(stripped)
    except FileNotFoundError:
        return DEFAULT_SENTENCES.copy()

    return lines or DEFAULT_SENTENCES.copy()


SENTENCES = load_sentences(SENTENCES_PATH)


class TypingSpeedTracker(tk.Tk):
    def __init__(self, sentence: str) -> None:
        super().__init__()
        self.title("Typing Speed Tracker")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)

        self.words = sentence.split()
        self.word_labels: list[tk.Label] = []
        self.current_word_index = 0
        self.correct_words = 0
        self.total_words = 0
        self.start_time: Optional[float] = None
        self.suspend_trace = False

        self._build_ui()
        self.highlight_current_word()

    def _build_ui(self) -> None:
        header = tk.Label(
            self,
            text="Speed Typing Tracker",
            font=("Segoe UI", 18, "bold"),
            fg="#f5f5f5",
            bg="#1e1e1e",
        )
        header.pack(pady=(16, 10))

        instructions = tk.Label(
            self,
            text="Type the highlighted word and press space to move forward.",
            font=("Segoe UI", 11),
            fg="#b3b3b3",
            bg="#1e1e1e",
        )
        instructions.pack()

        self.sentence_frame = tk.Frame(self, bg="#1e1e1e")
        self.sentence_frame.pack(pady=(18, 10))
        self.render_sentence_labels()

        input_frame = tk.Frame(self, bg="#1e1e1e")
        input_frame.pack(pady=(8, 6))

        entry_label = tk.Label(
            input_frame,
            text="Your input:",
            font=("Segoe UI", 12),
            fg="#f5f5f5",
            bg="#1e1e1e",
        )
        entry_label.pack(anchor="w")

        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", self.on_entry_change)

        self.entry = ttk.Entry(input_frame, textvariable=self.entry_var, font=("Segoe UI", 14))
        self.entry.pack(fill="x", ipadx=4, ipady=6)
        self.entry.focus_set()
        self.entry.bind("<space>", self.on_space_press)
        self.entry.bind("<Return>", self.on_space_press)

        feedback_label = tk.Label(
            input_frame,
            text="Feedback:",
            font=("Segoe UI", 12),
            fg="#f5f5f5",
            bg="#1e1e1e",
        )
        feedback_label.pack(anchor="w", pady=(12, 0))

        self.feedback_box = tk.Text(
            input_frame,
            height=1,
            width=30,
            font=("Consolas", 16),
            bg="#121212",
            fg="#f5f5f5",
            bd=0,
            highlightthickness=1,
            highlightbackground="#444444",
        )
        self.feedback_box.pack(fill="x", padx=(0, 0))
        self.feedback_box.configure(state="disabled")
        self.feedback_box.tag_configure("correct", foreground="#4caf50")
        self.feedback_box.tag_configure("incorrect", foreground="#f44336")

        status_frame = tk.Frame(self, bg="#1e1e1e")
        status_frame.pack(pady=(16, 8), fill="x")

        self.status_var = tk.StringVar()
        self.speed_var = tk.StringVar()

        status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 12),
            fg="#f5f5f5",
            bg="#1e1e1e",
        )
        status_label.pack(anchor="w")

        speed_label = tk.Label(
            status_frame,
            textvariable=self.speed_var,
            font=("Segoe UI", 12),
            fg="#b3b3b3",
            bg="#1e1e1e",
        )
        speed_label.pack(anchor="w")

        actions_frame = tk.Frame(self, bg="#1e1e1e")
        actions_frame.pack(pady=(10, 16))

        reset_button = ttk.Button(actions_frame, text="Restart", command=self.reset_session)
        reset_button.pack()

        self.update_status()
        self.update_speed()

    def render_sentence_labels(self) -> None:
        for widget in self.sentence_frame.winfo_children():
            widget.destroy()

        self.word_labels = []
        for idx, word in enumerate(self.words):
            label = tk.Label(
                self.sentence_frame,
                text=word,
                font=("Segoe UI", 14, "bold"),
                fg="#f5f5f5",
                bg="#2d2d2d",
                padx=6,
                pady=4,
            )
            label.grid(row=0, column=idx, padx=4)
            self.word_labels.append(label)

    def on_entry_change(self, *_: object) -> None:
        if self.suspend_trace:
            return

        if self.start_time is None and self.entry_var.get():
            self.start_time = time.perf_counter()

        self.update_feedback_display(self.entry_var.get())

    def on_space_press(self, event: tk.Event) -> str:
        typed_word = self.entry_var.get().strip()
        if not typed_word and event.keysym == "space":
            return "break"

        self.evaluate_word(typed_word)
        return "break"

    def update_feedback_display(self, typed_text: str) -> None:
        self.feedback_box.configure(state="normal")
        self.feedback_box.delete("1.0", tk.END)
        if self.current_word_index >= len(self.words):
            self.feedback_box.configure(state="disabled")
            return

        target_word = self.words[self.current_word_index]

        for idx, char in enumerate(typed_text):
            tag = "correct" if idx < len(target_word) and char == target_word[idx] else "incorrect"
            self.feedback_box.insert(tk.END, char, tag)

        self.feedback_box.configure(state="disabled")

    def evaluate_word(self, typed_word: str) -> None:
        if self.current_word_index >= len(self.words):
            return

        target_word = self.words[self.current_word_index]
        is_correct = typed_word == target_word

        label = self.word_labels[self.current_word_index]
        label.configure(
            bg="#d1f2c4" if is_correct else "#f8d7da",
            fg="#1e1e1e",
            relief="flat",
            borderwidth=0,
        )

        if is_correct:
            self.correct_words += 1
        self.total_words += 1

        self.current_word_index += 1
        self.reset_entry()
        self.update_status()
        self.update_speed()

        if self.current_word_index < len(self.words):
            self.highlight_current_word()
        else:
            self.show_completion_message()

    def highlight_current_word(self) -> None:
        for idx, label in enumerate(self.word_labels):
            if idx < self.current_word_index:
                continue
            label.configure(bg="#2d2d2d", fg="#f5f5f5", relief="flat", borderwidth=0)

        if self.current_word_index < len(self.word_labels):
            current_label = self.word_labels[self.current_word_index]
            current_label.configure(bg="#ffffff", fg="#1e1e1e", borderwidth=2, relief="solid")

    def reset_entry(self) -> None:
        self.suspend_trace = True
        self.entry_var.set("")
        self.suspend_trace = False
        self.update_feedback_display("")

    def update_status(self) -> None:
        self.status_var.set(f"Words: {self.correct_words} correct / {self.total_words} total")

    def update_speed(self) -> None:
        if self.start_time is None or self.correct_words == 0:
            self.speed_var.set("Speed: waiting for input...")
            return

        elapsed_minutes = (time.perf_counter() - self.start_time) / 60
        if elapsed_minutes <= 0:
            self.speed_var.set("Speed: calculating...")
            return

        wpm = self.correct_words / elapsed_minutes
        self.speed_var.set(f"Speed: {wpm:.1f} WPM (correct words)")

    def show_completion_message(self) -> None:
        self.entry.configure(state="disabled")
        self.speed_var.set(self.speed_var.get() + " | Session complete")

    def load_new_sentence(self, sentence: str) -> None:
        self.words = sentence.split()
        self.current_word_index = 0
        self.render_sentence_labels()
        self.highlight_current_word()

    def reset_session(self) -> None:
        self.start_time = None
        self.correct_words = 0
        self.total_words = 0

        new_sentence = random.choice(SENTENCES)
        self.load_new_sentence(new_sentence)

        self.entry.configure(state="normal")
        self.reset_entry()
        self.update_status()
        self.update_speed()


if __name__ == "__main__":
    app = TypingSpeedTracker(random.choice(SENTENCES))
    app.mainloop()
