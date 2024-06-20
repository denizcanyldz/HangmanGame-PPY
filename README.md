# HangmanGame-PPY
# s28330
# Project Hangman

*A web-based implementation of the classic Hangman game built with Python.*

## Project Requirements and Goals

**Target Audience**

* Casual players seeking a fun and challenging word-guessing game.
* Players familiar with the classic Hangman game.
* Individuals looking for an engaging and educational activity.

**Core Gameplay**

* User enters their name (minimum 3 characters, letters and numbers only).
* Select a topic from a list of pre-defined topics.
* Guess letters to complete the word within a time limit.
* Real-time score display and remaining attempts.
* Game over upon exhausting all attempts or successful word guess.
* Leaderboard displaying top scores.

**Success Criteria**

* A playable Hangman game with core mechanics implemented.
* User-friendly interface with clear visual or text-based gameplay.
* Database integration for storing player names and scores.

**Stretch Goals**

* **Dynamic Word Fetching:** Integrate with an external dictionary API to fetch words dynamically for increased variety and challenge.
* **Advanced Scoring System:** Implement a more complex scoring system that rewards speed and accuracy.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- MongoDB
- Docker (optional for containerization)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/HangmanGame-PPY.git
   cd HangmanGame-PPY

2. **Set up a virtual environment and install dependencies:**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt

3. **Configure MongoDB:**
   Update the MONGODB_URL in app.py with your MongoDB connection string.
   ```bash
   MONGODB_URL = "your_mongodb_connection_string"

4. **Run the application:**
   ```bash
   python app.py

### Using Docker

1. **Build the Docker image:**
   ```bash
   docker build -t hangman-game .

2. **Run the Docker container:**
   ```bash
   docker run -p 5000:5000 hangman-game

Access the game at http://localhost:5000.

### How to Play
* Navigate to http://localhost:5000 in your web browser.
* Enter your name (minimum 3 characters, letters and numbers only) and select a topic.
* Start guessing letters to complete the word before the timer runs out.
* Try to guess the word with as few incorrect guesses as possible to achieve a high score.
* Check your score and see if you made it to the leaderboard.

### Project Structure
```bash
HangmanGame-PPY/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── Dockerfile
├── requirements.txt
├── app.py
├── hangman_game.py
├── read_topics.py
├── templates/
│   ├── index.html
│   ├── game.html
│   ├── leaderboard.html
│   └── game_over.html
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── images/
│   │   └── (your images here)
└── tests/
    └── test_hangman.py

