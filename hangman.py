import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from tkinter import simpledialog
from PIL import Image, ImageTk

def get_random_word():
    words = ['apple', 'banana', 'cherry', 'grape', 'lemon', 'orange', 'pear', 'pineapple', 'strawberry']
    return random.choice(words)

class HangmanGUI:
    def __init__(self, root):
        # Same initialization code as before
        self.game_canvas = None
        self.hangman_images = None
        self.guess_entry = None
        self.guess_label = None
        self.guess_button = None
        self.game_frame = None
        self.root = root
        self.root.title("Hangman Game")
        self.root.configure(bg="#f0f0f0")

        self.play_frame = tk.Frame(root, bg="#f0f0f0")
        self.play_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.play_frame, width=900, height=700, bg="#f0f0f0")
        self.canvas.pack()

        self.secret_word = get_random_word()
        self.correct_letters = ""
        self.missed_letters = ""
        self.game_is_done = False

        self.bg_image = Image.open("image.jpg")
        self.bg_image = self.bg_image.resize((900, 650))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)

        self.custom_font = font.Font(family="Times new Roman", size=20, weight="bold")
        self.play_button = tk.Button(
            self.play_frame, text="Play!", command=self.start_game, font=self.custom_font, height=1, width=6,
            bg="white", activebackground="#00FF00", fg="black"
        )
        self.play_button.place(relx=0.44, rely=0.45, anchor="ne")

        self.play_button.bind("<Enter>", lambda e: self.play_button.config(bg="#00FF00", fg="blue"))
        self.play_button.bind("<Leave>", lambda e: self.play_button.config(bg="white", fg="black"))
        self.hangman_text1 = tk.Label(self.play_frame, text="fgxjud", font=("Times New Roman", 5, "bold"),bg="#f0f0f0")
        self.hangman_text = tk.Label(self.play_frame, text="Hangman", font=("Times New Roman", 36, "bold"), bg="#f0f0f0")
        self.hangman_text.place(relx=0.5, rely=0.35, anchor="ne")

        self.bg_label = None

    def start_game(self):
        self.play_button.destroy()
        self.hangman_text.destroy()

        if self.bg_label:
            self.canvas.delete(self.bg_label)

        game_bg_image = Image.open("img.png")
        game_bg_image = game_bg_image.resize((1100, 1123))
        game_bg_photo = ImageTk.PhotoImage(game_bg_image)

        self.game_frame = tk.Frame(self.play_frame, bg="#f0f0f0")
        self.game_frame.place(x=0, y=0)

        self.game_canvas = tk.Canvas(self.game_frame, width=900, height=700, bg="#f0f0f0")
        self.game_canvas.pack()

        self.bg_label = self.game_canvas.create_image(0, 0, anchor="nw", image=game_bg_photo)
        self.bg_photo = game_bg_photo

        self.hangman_images = [
            """
            H A N G M A N 

              *---*
                  |
                  |
                  |
                  |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
                  |
                  |
                  |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
              O   |
                  |
                  |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
              O   |
             /    |
                  |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
              O   |
             /|   |
                  |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
              O   |
             /|\  |
                  |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
              O   |
             /|\  |
             /    |
                  |
            ==========
            =========
            """,
            """
            H A N G M A N 

              *---*
              |   |
              O   |
             /|\  |
             / \  |
                  |
            ==========
            =========
            """
        ]

        self.guess_button = tk.Button(self.game_canvas, text="Guess", command=self.make_guess, font=self.custom_font)
        self.guess_button.place(x=400, y=600)

        self.guess_label = tk.Label(self.game_canvas, text="Guess a letter:", font=self.custom_font, bg="#f0f0f0")
        self.guess_label.place(relx=0.2, rely=0.7)

        self.guess_entry = tk.Entry(self.game_canvas, font=self.custom_font)
        self.guess_entry.place(relx=0.4, rely=0.7)

        self.update_display()

    def update_display(self):
        self.game_canvas.delete("all")

        if self.missed_letters:
            self.game_canvas.create_text(200, 50, text=self.hangman_images[len(self.missed_letters)],
                                         font=("Courier", 12), anchor="n")
        else:
            self.game_canvas.create_text(200, 50, text=self.hangman_images[0], font=("Courier", 12), anchor="n")

        self.game_canvas.create_text(200, 300, text="Incorrect Letters: " + ' '.join(self.missed_letters), font=("Courier", 12), anchor="n")
        displayed_word = ' '.join([letter if letter in self.correct_letters else '_' for letter in self.secret_word])
        self.game_canvas.create_text(200, 250, text=displayed_word, font=("Courier", 24), anchor="n")

    def make_guess(self):
        guess = self.guess_entry.get().lower()

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showinfo("Hangman", "Please enter a single letter.")
            return

        if guess in self.correct_letters or guess in self.missed_letters:
            messagebox.showinfo("Hangman", "You have already guessed that letter. Choose again.")
            return

        if guess in self.secret_word:
            self.correct_letters += guess
            if all(letter in self.correct_letters for letter in self.secret_word):
                messagebox.showinfo("Hangman", "You have won! The secret word is \"" + self.secret_word + "\".")
                self.game_is_done = True
        else:
            self.missed_letters += guess
            if len(self.missed_letters) == len(self.hangman_images):
                messagebox.showinfo("Hangman",
                                    "You have run out of guesses! The secret word was \"" + self.secret_word + "\".")
                self.game_is_done = True

        if self.game_is_done:
            play_again = simpledialog.askstring("Hangman", "Do you want to play again? (yes/no)")
            if play_again and play_again.lower() == 'yes':
                self.reset_game()
            else:
                self.root.destroy()
        else:
            self.update_display()
            self.guess_entry.delete(0, tk.END)

    def reset_game(self):
        self.secret_word = get_random_word()
        self.correct_letters = ''
        self.missed_letters = ''
        self.game_is_done = False
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanGUI(root)
    root.mainloop()
