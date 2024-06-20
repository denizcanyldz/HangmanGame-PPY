import re
import certifi
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pymongo import MongoClient
from hangman_game import HangmanGame
from read_topics import load_topics

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MongoDB setup
MONGODB_URL = "mongodb+srv://deniz:denizpjatk@cluster0.5y1k84l.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGODB_URL, tlsCAFile=certifi.where())
db = client.hangman_game
scores_collection = db.scores

topics = load_topics()


def game_to_dict(game):
    return {
        "word_list": game.word_list,
        "selected_word": game.selected_word,
        "remaining_attempts": game.remaining_attempts,
        "guessed_letters": game.guessed_letters,
        "game_over": game.game_over,
        "word_guessed": game.word_guessed,
        "score": game.score
    }


def dict_to_game(data):
    game = HangmanGame(data['word_list'])
    game.selected_word = data['selected_word']
    game.remaining_attempts = data['remaining_attempts']
    game.guessed_letters = data['guessed_letters']
    game.game_over = data['game_over']
    game.word_guessed = data['word_guessed']
    game.score = data['score']
    return game


def save_score(player_name, score):
    existing_player = scores_collection.find_one({"player_name": player_name})
    if existing_player:
        if score > existing_player['score']:
            scores_collection.update_one(
                {"player_name": player_name},
                {"$set": {"score": score}}
            )
    else:
        scores_collection.insert_one({"player_name": player_name, "score": score})


def get_top_scores():
    return list(scores_collection.find().sort("score", -1).limit(10))


@app.route('/')
def index():
    return render_template('index.html', topics=topics.keys(), error_message='')


@app.route('/start_game', methods=['POST'])
def start_game():
    player_name = request.form['player_name']
    topic = request.form['topic']

    if not re.match(r'^[a-zA-Z0-9]{3,}$', player_name):
        error_message = "Name must be at least 3 characters long and can only contain letters and numbers."
        return render_template('index.html', topics=topics.keys(), error_message=error_message)

    word_list = topics.get(topic, [])
    game = HangmanGame(word_list)
    game.select_word()
    session['player_name'] = player_name
    session['topic'] = topic
    session['game'] = game_to_dict(game)
    return render_template('game.html', player_name=player_name, word=game.display_word(),
                           attempts=game.remaining_attempts, guessed='',
                           hangman_image=url_for('static', filename='images/hangman0.png'), score=0)


@app.route('/guess', methods=['POST'])
def guess():
    letter = request.form['letter'].lower()
    game_data = session.get('game')
    game = dict_to_game(game_data)

    error_message = ''
    if len(letter) != 1 or not letter.isalpha():
        error_message = "Please enter a single letter (a-z)."
    elif letter in game.guessed_letters:
        error_message = "You have already guessed that letter."
    else:
        game.guess_letter(letter)
        session['game'] = game_to_dict(game)

    if game.game_over:
        save_score(session['player_name'], game.score)  # Save the score to the leaderboard
        session['game_result'] = {
            "word": game.selected_word,
            "word_guessed": game.word_guessed,
            "score": game.score
        }
        return jsonify({
            "word": game.display_word(),
            "attempts": game.remaining_attempts,
            "guessed": ', '.join(game.guessed_letters),
            "score": game.score,
            "hangman_image": url_for('static', filename=f'images/hangman{6 - game.remaining_attempts}.png'),
            "error_message": error_message,
            "game_over": True,
            "word_guessed": game.word_guessed  # Include word_guessed flag
        })

    return jsonify({
        "word": game.display_word(),
        "attempts": game.remaining_attempts,
        "guessed": ', '.join(game.guessed_letters),
        "score": game.score,
        "hangman_image": url_for('static', filename=f'images/hangman{6 - game.remaining_attempts}.png'),
        "error_message": error_message,
        "game_over": False,
        "word_guessed": game.word_guessed  # Include word_guessed flag
    })


@app.route('/timeout', methods=['POST'])
def timeout():
    game_data = session.get('game')
    game = dict_to_game(game_data)
    game.game_over = True
    save_score(session['player_name'], game.score)  # Save the score to the leaderboard
    session['game_result'] = {
        "word": game.selected_word,
        "word_guessed": game.word_guessed,
        "score": game.score
    }
    return redirect(url_for('game_over'))


@app.route('/game_over')
def game_over():
    result = session.get('game_result', {})
    return render_template('game_over.html', result=result)


@app.route('/leaderboard')
def leaderboard():
    top_scores = get_top_scores()
    return render_template('leaderboard.html', top_scores=top_scores, enumerate=enumerate)


@app.route('/replay', methods=['POST'])
def replay():
    session.pop('game', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
