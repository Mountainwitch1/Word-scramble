import random
import tkinter as tk
from tkinter import messagebox
import os


# === Word Scramble Game Setup ===
def fetch_words():
    return ['apple', 'banana', 'orange', 'grape', 'watermelon', 'pineapple', 'strawberry', 'blueberry', 'cherry',
            'peach']


# Categorize words based on difficulty
def categorize_words(words):
    easy = [word for word in words if len(word) <= 5]
    medium = [word for word in words if len(word) > 5 and len(word) <= 8]
    hard = [word for word in words if len(word) > 8]
    return {'easy': easy, 'medium': medium, 'hard': hard}


def scramble(word):
    return ''.join(random.sample(word, len(word)))


# === GUI Setup with Tkinter ===
class WordScrambleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🧠 Word Scramble Game - 2 Player Mode")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")

        self.words_by_difficulty = categorize_words(fetch_words())
        self.reset_game_data()
        self.build_name_screen()

    def reset_game_data(self):
        self.score = {'Player 1': 0, 'Player 2': 0}
        self.round = 0
        self.timer = 10
        self.current_word = ''
        self.scrambled_word = ''
        self.player_names = ['Player 1', 'Player 2']
        self.turn_index = 0
        self.timer_id = None

    # === Step 1: Name input ===
    def build_name_screen(self):
        self.clear_widgets()

        self.title_label = tk.Label(self.root, text="Enter Player Names", font=("Arial Black", 20), bg="#2c3e50",
                                    fg="white")
        self.title_label.pack(pady=20)

        self.name_entries = []
        for i in range(2):
            label = tk.Label(self.root, text=f"Player {i + 1} Name:", font=("Arial", 14), bg="#2c3e50", fg="white")
            label.pack()
            entry = tk.Entry(self.root, font=("Arial", 14))
            entry.pack(pady=5)
            self.name_entries.append(entry)

        self.start_btn = tk.Button(self.root, text="Continue", font=("Arial", 12), bg="#3498db", fg="white",
                                   command=self.save_names)
        self.start_btn.pack(pady=20)

        self.root.update()  # Force update to ensure buttons show the text

    def save_names(self):
        self.player_names = [entry.get().strip() or f'Player {i + 1}' for i, entry in enumerate(self.name_entries)]
        self.build_difficulty_menu()

    # === Step 2: Difficulty selection ===
    def build_difficulty_menu(self):
        self.clear_widgets()

        self.title_label = tk.Label(self.root, text="Choose Difficulty", font=("Arial Black", 20), bg="#2c3e50",
                                    fg="white")
        self.title_label.pack(pady=20)

        self.difficulty_frame = tk.Frame(self.root, bg="#2c3e50")
        self.difficulty_frame.pack()

        for level in ['easy', 'medium', 'hard']:
            btn = tk.Button(self.difficulty_frame, text=level.capitalize(), font=("Arial", 12),
                            bg="#1abc9c", fg="white", width=10,
                            command=lambda l=level: self.start_game(l))
            btn.pack(side=tk.LEFT, padx=10, pady=5)  # Padding here for better visual separation

        self.root.update()  # Force update to ensure buttons show the text

    def start_game(self, difficulty):
        self.difficulty = difficulty
        total_words = self.words_by_difficulty[difficulty]

        # Ensure the sample size is not larger than the available words
        sample_size = min(len(total_words), 10)  # Ensure the sample size is not larger than the list
        self.word_list = random.sample(total_words, sample_size)

        # Continue the game as usual
        self.load_next_word()

    def load_next_word(self):
        if self.round < 10:
            self.current_player = self.player_names[self.turn_index % 2]
            self.current_word = self.word_list[self.round]
            self.scrambled_word = scramble(self.current_word)
            self.round += 1
            self.turn_index += 1
            self.timer = 10

            self.clear_widgets()

            self.word_label = tk.Label(self.root, text=f"{self.current_player}'s Turn", font=("Arial", 18),
                                       bg="#2c3e50", fg="yellow")
            self.word_label.pack(pady=10)

            self.scrambled_label = tk.Label(self.root, text=self.scrambled_word, font=("Helvetica", 28), bg="#2c3e50",
                                            fg="white")
            self.scrambled_label.pack(pady=10)

            self.entry = tk.Entry(self.root, font=("Helvetica", 16), width=20, justify="center")
            self.entry.pack(pady=5)

            self.submit_btn = tk.Button(self.root, text="Submit", font=("Arial", 12), bg="#1abc9c", fg="white",
                                        command=self.check_answer)
            self.submit_btn.pack(pady=5)

            self.timer_label = tk.Label(self.root, text=f"Time: {self.timer}", font=("Arial", 14), bg="#2c3e50",
                                        fg="red")
            self.timer_label.pack()

            self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#2c3e50", fg="white")
            self.result_label.pack(pady=5)

            self.update_timer()
        else:
            self.end_game()

    def update_timer(self):
        self.timer -= 1
        self.timer_label.config(text=f"Time: {self.timer}")
        if self.timer <= 0:
            self.result_label.config(text=f"⏰ Time's up! It was '{self.current_word}'", fg="red")
            self.root.after(1500, self.load_next_word)
        else:
            self.timer_id = self.root.after(1000, self.update_timer)

    def check_answer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        guess = self.entry.get().strip().lower()
        if guess == self.current_word:
            self.score[self.current_player] += 1
            self.result_label.config(text="✅ Correct!", fg="green")
        else:
            self.result_label.config(text=f"❌ Nope! It was '{self.current_word}'", fg="red")
        self.root.after(1500, self.load_next_word)

    def end_game(self):
        self.clear_widgets()
        p1, p2 = self.player_names
        s1, s2 = self.score[p1], self.score[p2]

        winner = "It's a tie!" if s1 == s2 else f"🏆 {p1 if s1 > s2 else p2} wins!"

        summary = f"{p1}: {s1}/5\n{p2}: {s2}/5\n\n{winner}"
        end_label = tk.Label(self.root, text=summary, font=("Arial", 16), bg="#2c3e50", fg="white")
        end_label.pack(pady=30)

        self.play_again_btn = tk.Button(self.root, text="Play Again", font=("Arial", 12), bg="#9b59b6", fg="white",
                                        command=self.reset_all)
        self.play_again_btn.pack()
        self.root.update()  # Force update to ensure buttons show the text

    def reset_all(self):
        self.reset_game_data()
        self.build_name_screen()

    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# === Run the Game ===
if __name__ == "__main__":
    root = tk.Tk()
    game = WordScrambleGame(root)
    root.mainloop()
