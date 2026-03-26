# Kivy Tic-Tac-Toe with AI

A modern, interactive Tic-Tac-Toe game built using Python and the Kivy GUI framework. This application features smooth screen transitions, an undo/redo system, and an AI opponent powered by the Minimax algorithm.

## 🚀 Features

* **Graphical User Interface:** Built entirely with Kivy, featuring custom colors, grid layouts, and modal popups.
* **Versatile Game Modes:** * **Play with Friend:** Classic local 2-player mode.
  * **Play with Bot:** Challenge an automated opponent.
* **Adjustable AI Difficulty:**
  * *Easy:* The bot makes random moves on available squares.
  * *Medium:* Uses a depth-limited Minimax algorithm to play smarter but still allows the player a chance to win.
  * *Hard:* Uses the full Minimax algorithm with Alpha-Beta pruning to make optimal, unbeatable moves.
* **Game Controls:** Full `Undo` and `Redo` functionality during gameplay, complete with history tracking.

## 🧠 How the AI Works

The "Hard" difficulty level utilizes a decision-making algorithm called Minimax. This allows the bot to "look ahead" at all possible future moves on the board, scoring them to choose the absolute best path to victory (or a guaranteed draw). 

## 🛠️ Getting Started

### Prerequisites
* Python 3.x installed on your system.
* The Kivy library. You can install it via pip:
  ```bash
  pip install kivy

### How to Run
1. Clone this repository to your local machine:
   ```Bash
   git clone [https://github.com/farhansyedAli/your-repo-name.git](https://github.com/farhansyedAli/your-repo-name.git)
2. Navigate to the project directory:

   ```Bash
   cd your-repo-name
3. Run the main application file:
   ```Bash
   python main.py

### 👤 Author
Syed Farhan Ali Shah - @farhansyedAli
