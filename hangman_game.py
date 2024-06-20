import random


class HangmanGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.selected_word = ""
        self.remaining_attempts = 6
        self.guessed_letters = []
        self.game_over = False
        self.word_guessed = False
        self.score = 0  # Add score attribute

    def select_word(self):
        self.selected_word = random.choice(self.word_list)
        self.remaining_attempts = 6
        self.guessed_letters = []
        self.game_over = False
        self.word_guessed = False
        self.score = 0  # Reset score
        return self.selected_word

    def guess_letter(self, letter):
        if letter in self.guessed_letters:
            return
        self.guessed_letters.append(letter)
        if letter in self.selected_word:
            self.score += 10  # Add points for correct guess
        else:
            self.remaining_attempts -= 1
            self.score -= 5  # Subtract points for incorrect guess
            if self.remaining_attempts == 0:
                self.game_over = True

        if all(char in self.guessed_letters for char in self.selected_word):
            self.word_guessed = True
            self.game_over = True

    def display_word(self):
        return ' '.join([char if char in self.guessed_letters else '_' for char in self.selected_word])
