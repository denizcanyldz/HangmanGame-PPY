import unittest
from hangman_game import HangmanGame
from flask import Flask, session
from app import app, game_to_dict, dict_to_game, save_score, get_top_scores
import re


class TestHangmanGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def setUp(self):
        self.game = HangmanGame(["python", "flask", "hangman", "javascript"])

    def test_word_selection(self):
        word = self.game.select_word()
        self.assertIn(word, ["python", "flask", "hangman", "javascript"])

    def test_initial_game_state(self):
        self.game.select_word()
        self.assertEqual(self.game.remaining_attempts, 6)
        self.assertEqual(self.game.guessed_letters, [])
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.word_guessed)
        self.assertEqual(self.game.score, 0)

    def test_correct_letter_guess(self):
        self.game.selected_word = "python"
        self.game.guess_letter('p')
        self.assertIn('p', self.game.guessed_letters)
        self.assertEqual(self.game.display_word(), "p _ _ _ _ _")

    def test_incorrect_letter_guess(self):
        self.game.selected_word = "python"
        self.game.guess_letter('z')
        self.assertIn('z', self.game.guessed_letters)
        self.assertEqual(self.game.remaining_attempts, 5)
        self.assertEqual(self.game.score, -5)

    def test_repeated_letter_guess(self):
        self.game.selected_word = "python"
        self.game.guess_letter('p')
        remaining_attempts = self.game.remaining_attempts
        score = self.game.score
        self.game.guess_letter('p')
        self.assertEqual(self.game.remaining_attempts, remaining_attempts)
        self.assertEqual(self.game.score, score)

    def test_word_guessed(self):
        self.game.selected_word = "java"
        for letter in "java":
            self.game.guess_letter(letter)
        self.assertTrue(self.game.word_guessed)
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.score, 30)

    def test_game_over(self):
        self.game.selected_word = "kotlin"
        for letter in "abcdef":
            self.game.guess_letter(letter)
        self.assertTrue(self.game.game_over)

    def test_player_name_validation(self):
        response = self.app.post('/start_game', data=dict(player_name='ab', topic='animals'))
        self.assertIn(b"Name must be at least 3 characters long and can only contain letters and numbers.",
                      response.data)

        response = self.app.post('/start_game', data=dict(player_name='abc@', topic='animals'))
        self.assertIn(b"Name must be at least 3 characters long and can only contain letters and numbers.",
                      response.data)

        response = self.app.post('/start_game', data=dict(player_name='abcd', topic='animals'))
        self.assertNotIn(b"Name must be at least 3 characters long and can only contain letters and numbers.",
                         response.data)

    def test_invalid_letter_guess(self):
        with self.app as client:
            with client.session_transaction() as sess:
                game = HangmanGame(["python", "flask", "hangman", "javascript"])
                game.select_word()
                sess['player_name'] = 'tester'
                sess['game'] = game_to_dict(game)

            response = client.post('/guess', data=dict(letter='3'))
            self.assertIn(b"Please enter a single letter (a-z).", response.data)

            response = client.post('/guess', data=dict(letter='@'))
            self.assertIn(b"Please enter a single letter (a-z).", response.data)

            response = client.post('/guess', data=dict(letter='ab'))
            self.assertIn(b"Please enter a single letter (a-z).", response.data)

    def test_valid_letter_guess(self):
        with self.app as client:
            with client.session_transaction() as sess:
                game = HangmanGame(["python", "flask", "hangman", "javascript"])
                game.selected_word = "python"
                sess['player_name'] = 'tester'
                sess['game'] = game_to_dict(game)

            response = client.post('/guess', data=dict(letter='p'))
            self.assertNotIn(b"Please enter a single letter (a-z).", response.data)
            self.assertIn(b'p _ _ _ _ _', response.data)

    def test_repeated_letter_guess_in_game(self):
        with self.app as client:
            with client.session_transaction() as sess:
                game = HangmanGame(["python", "flask", "hangman", "javascript"])
                game.selected_word = "python"
                game.guess_letter('p')
                sess['player_name'] = 'tester'
                sess['game'] = game_to_dict(game)

            response = client.post('/guess', data=dict(letter='p'))
            self.assertIn(b"You have already guessed that letter.", response.data)

    def test_successful_word_guess_and_new_word_selection(self):
        with self.app as client:
            with client.session_transaction() as sess:
                game = HangmanGame(["java"])
                game.selected_word = "java"
                for letter in "jav":
                    game.guess_letter(letter)
                sess['player_name'] = 'tester'
                sess['game'] = game_to_dict(game)

            response = client.post('/guess', data=dict(letter='a'))
            self.assertIn(b'"game_over":true', response.data)
            self.assertIn(b'"word_guessed":true', response.data)

    def test_save_score_new_player(self):
        save_score("new_player", 50)
        top_scores = get_top_scores()
        self.assertTrue(any(player['player_name'] == 'new_player' and player['score'] == 50 for player in top_scores))

    def test_save_score_existing_player_higher(self):
        save_score("existing_player", 30)
        save_score("existing_player", 50)
        top_scores = get_top_scores()
        self.assertTrue(
            any(player['player_name'] == 'existing_player' and player['score'] == 50 for player in top_scores))

    def test_save_score_existing_player_lower(self):
        save_score("existing_player2", 60)
        save_score("existing_player2", 40)
        top_scores = get_top_scores()
        self.assertTrue(
            any(player['player_name'] == 'existing_player2' and player['score'] == 60 for player in top_scores))


if __name__ == "__main__":
    unittest.main()
