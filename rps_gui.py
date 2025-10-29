"""
Rock-Paper-Scissors
Author: Ratheesh
"""

import random
import tkinter as tk
from tkinter import messagebox, ttk

# Optional Pillow for images
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# -------------------- Game Logic --------------------
CHOICES = ["rock", "paper", "scissors"]
WIN_RULES = {
    ("rock", "scissors"): "rock",
    ("scissors", "paper"): "scissors",
    ("paper", "rock"): "paper"
}


def decide_winner(player, computer):
    if player == computer:
        return "draw", "It’s a draw!"
    if (player, computer) in WIN_RULES and WIN_RULES[(player, computer)] == player:
        return "player", f"{player.capitalize()} beats {computer}!"
    return "computer", f"{computer.capitalize()} beats {player}."


# -------------------- Main App --------------------
class RPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock • Paper • Scissors")
        self.geometry("600x500")
        self.configure(bg="#f2f5f9")
        self.resizable(False, False)

        # Game state
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.best_of = tk.IntVar(value=3)
        self.images = {}

        # Load icons if available
        self.load_images()

        # Build UI
        self.create_header()
        self.create_scoreboard()
        self.create_choices()
        self.create_results()
        self.create_controls()

    # ---------- Load Images ----------
    def load_images(self):
        if not PIL_AVAILABLE:
            return
        try:
            for name in CHOICES:
                img = Image.open(f"assets/{name}.png")
                img = img.resize((120, 120))
                self.images[name] = ImageTk.PhotoImage(img)
        except Exception:
            self.images = {}

    # ---------- UI Sections ----------
    def create_header(self):
        tk.Label(
            self,
            text="Rock • Paper • Scissors",
            font=("Segoe UI", 22, "bold"),
            bg="#f2f5f9",
            fg="#1a1a1a"
        ).pack(pady=10)

    def create_scoreboard(self):
        frame = tk.Frame(self, bg="#f2f5f9")
        frame.pack(pady=10)

        self.player_label = tk.Label(frame, text="You: 0", font=("Segoe UI", 14, "bold"), fg="#2d89ef", bg="#f2f5f9")
        self.player_label.grid(row=0, column=0, padx=40)

        self.vs_label = tk.Label(frame, text="VS", font=("Segoe UI", 16, "bold"), bg="#f2f5f9")
        self.vs_label.grid(row=0, column=1)

        self.computer_label = tk.Label(frame, text="Computer: 0", font=("Segoe UI", 14, "bold"), fg="#d9534f", bg="#f2f5f9")
        self.computer_label.grid(row=0, column=2, padx=40)

    def create_choices(self):
        frame = tk.Frame(self, bg="#f2f5f9")
        frame.pack(pady=10)

        for i, choice in enumerate(CHOICES):
            if choice in self.images:
                btn = tk.Button(
                    frame,
                    image=self.images[choice],
                    bg="#e3e6eb",
                    activebackground="#c9d6e3",
                    bd=0,
                    relief="flat",
                    command=lambda c=choice: self.play_round(c)
                )
            else:
                btn = tk.Button(
                    frame,
                    text=choice.capitalize(),
                    font=("Segoe UI", 13, "bold"),
                    width=10,
                    height=2,
                    bg="#e3e6eb",
                    activebackground="#c9d6e3",
                    relief="flat",
                    command=lambda c=choice: self.play_round(c)
                )
            btn.grid(row=0, column=i, padx=20, pady=5)
            self.add_hover_effect(btn)

    def create_results(self):
        frame = tk.Frame(self, bg="#f2f5f9")
        frame.pack(pady=10)

        self.player_choice_label = tk.Label(frame, text="Your Choice: —", font=("Segoe UI", 12), bg="#f2f5f9")
        self.player_choice_label.grid(row=0, column=0, padx=40)

        self.computer_choice_label = tk.Label(frame, text="Computer Choice: —", font=("Segoe UI", 12), bg="#f2f5f9")
        self.computer_choice_label.grid(row=0, column=1, padx=40)

        self.result_label = tk.Label(
            self,
            text="Make your move!",
            font=("Segoe UI", 14, "bold"),
            bg="#f2f5f9",
            fg="#333"
        )
        self.result_label.pack(pady=15)

    def create_controls(self):
        frame = tk.Frame(self, bg="#f2f5f9")
        frame.pack(pady=10)

        tk.Label(frame, text="Best of:", bg="#f2f5f9").grid(row=0, column=0, padx=5)
        combo = ttk.Combobox(frame, textvariable=self.best_of, values=[1, 3, 5, 7], width=5, state="readonly")
        combo.grid(row=0, column=1, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e: self.reset_game())

        tk.Button(frame, text="Reset", command=self.reset_game, bg="#2d89ef", fg="white",
                  activebackground="#1e70bf", relief="flat", width=10).grid(row=0, column=2, padx=10)
        tk.Button(frame, text="Quit", command=self.quit_game, bg="#d9534f", fg="white",
                  activebackground="#c9302c", relief="flat", width=10).grid(row=0, column=3, padx=10)

    # ---------- Game Actions ----------
    def play_round(self, player_choice):
        computer_choice = random.choice(CHOICES)
        winner, reason = decide_winner(player_choice, computer_choice)

        self.rounds_played += 1
        if winner == "player":
            self.player_score += 1
            color = "#2ecc71"
            msg = f"🟢 You Win! {reason}"
        elif winner == "computer":
            self.computer_score += 1
            color = "#e74c3c"
            msg = f"🔴 Computer Wins! {reason}"
        else:
            color = "#555"
            msg = f"⚪ Draw — {reason}"

        # Update labels
        self.player_label.config(text=f"You: {self.player_score}")
        self.computer_label.config(text=f"Computer: {self.computer_score}")
        self.player_choice_label.config(text=f"Your Choice: {player_choice.capitalize()}")
        self.computer_choice_label.config(text=f"Computer Choice: {computer_choice.capitalize()}")
        self.result_label.config(text=msg, fg=color)

        # Check match winner
        max_wins = (self.best_of.get() // 2) + 1
        if self.player_score == max_wins or self.computer_score == max_wins:
            self.after(1000, self.show_match_result)

    def reset_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.player_label.config(text="You: 0")
        self.computer_label.config(text="Computer: 0")
        self.result_label.config(text="Make your move!", fg="#333")
        self.player_choice_label.config(text="Your Choice: —")
        self.computer_choice_label.config(text="Computer Choice: —")

    def show_match_result(self):
        if self.player_score > self.computer_score:
            msg = f"You won the match {self.player_score} – {self.computer_score}! 🎉"
        else:
            msg = f"Computer won {self.computer_score} – {self.player_score}. Try again!"
        messagebox.showinfo("Match Over", msg)
        self.reset_game()

    def quit_game(self):
        if messagebox.askyesno("Exit", "Are you sure you want to quit?"):
            self.destroy()

    # ---------- Utility ----------
    def add_hover_effect(self, button):
        def on_enter(e):
            button.config(bg="#c9d6e3")

        def on_leave(e):
            button.config(bg="#e3e6eb")

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)


# -------------------- Run the App --------------------
if __name__ == "__main__":
    app = RPSApp()
    app.mainloop()
