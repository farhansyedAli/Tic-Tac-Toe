from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
import random
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
import math

background_color = (16 / 255, 0, 43 / 255, 1)
button_bg_color = (36 / 255, 0, 70 / 255, 1)
x_color = (0, 212 / 255, 1, 1)
o_color = (1, 0, 84 / 255, 1)

mode = None
difficulty = "medium"  # default difficulty


def summ(a, b, c):
    return a + b + c


def check_win(x_state, z_state):
    wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]]
    for win in wins:
        if summ(x_state[win[0]], x_state[win[1]], x_state[win[2]]) == 3:
            return 1
        if summ(z_state[win[0]], z_state[win[1]], z_state[win[2]]) == 3:
            return 0
    return -1


def convert_to_board(x_state, z_state):
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for idx in range(9):
        if x_state[idx]:
            board[idx // 3][idx % 3] = 'X'
        elif z_state[idx]:
            board[idx // 3][idx % 3] = 'O'
    return board


def is_winner_board(board, player):
    for row in board:
        if row[0] == row[1] == row[2] == player:
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


def is_full_board(board):
    return all(cell != ' ' for row in board for cell in row)


def alphabetA(board, depth, alpha, beta, is_maximizing):
    if is_winner_board(board, 'O'):
        return 10 - depth
    if is_winner_board(board, 'X'):
        return depth - 10
    if is_full_board(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = alphabetA(board, depth + 1, alpha, beta, False)
                    board[i][j] = ' '
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = alphabetA(board, depth + 1, alpha, beta, True)
                    board[i][j] = ' '
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score


def best_move_easy(x_state, z_state):
    board = convert_to_board(x_state, z_state)

    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    return random.choice(empty) if empty else None


def best_move_medium(x_state, z_state):
    board = convert_to_board(x_state, z_state)

    def minimax_limited(brd, depth, is_maximizing):
        if is_winner_board(brd, 'O'):
            return 10 - depth
        if is_winner_board(brd, 'X'):
            return depth - 10
        if is_full_board(brd) or depth == 2:  # limit depth for medium
            return 0

        if is_maximizing:
            bst_scr = -math.inf
            for i in range(3):
                for j in range(3):
                    if brd[i][j] == ' ':
                        brd[i][j] = 'O'
                        scr = minimax_limited(brd, depth + 1, False)
                        brd[i][j] = ' '
                        bst_scr = max(bst_scr, scr)
            return bst_scr
        else:
            bst_scr = math.inf
            for i in range(3):
                for j in range(3):
                    if brd[i][j] == ' ':
                        brd[i][j] = 'X'
                        scr = minimax_limited(brd, depth + 1, True)
                        brd[i][j] = ' '
                        bst_scr = min(bst_scr, scr)
            return bst_scr

    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax_limited(board, 0, False)
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def best_move_hard(x_state, z_state):
    best_score = -math.inf
    move = None
    board = convert_to_board(x_state, z_state)
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = alphabetA(board, 0, -math.inf, math.inf, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move


def confirm_exit(instance):
    # Create a dimmed background popup
    popup = ModalView(size_hint=(0.6, 0.4), background_color=(0, 0, 0, 0.7))
    layout = BoxLayout(orientation='vertical', spacing=20, padding=20)
    label = Label(
        text="Are you sure you want to exit?",
        font_size=24,
        halign="center",
        valign="middle",
        color=(1, 1, 1, 1)
    )
    label.bind(size=label.setter('text_size'))  # Allow wrapping
    button_layout = BoxLayout(spacing=20, size_hint=(1, 0.4))
    yes_button = Button(
        text="Yes",
        background_color=(1, 0.2, 0.2, 1),
        font_size=20,
        size_hint=(0.5, 1)
    )
    no_button = Button(
        text="No",
        background_color=(0.2, 1, 0.2, 1),
        font_size=20,
        size_hint=(0.5, 1)
    )
    button_layout.add_widget(yes_button)
    button_layout.add_widget(no_button)
    layout.add_widget(label)
    layout.add_widget(button_layout)

    popup.add_widget(layout)

    yes_button.bind(on_release=lambda x: App.get_running_app().stop())
    no_button.bind(on_release=popup.dismiss)

    popup.open()


class ModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.add_widget(self.layout)

        self.title = Label(text="Select Game Mode", font_size=32, color=(1, 1, 1, 1))
        self.layout.add_widget(self.title)

        self.friend_btn = Button(text="Play with Friend", font_size=24, background_color=(60/255, 9/255, 108 / 255, 1))
        self.bot_btn = Button(text="Play with Bot", font_size=24, background_color=(60 / 255, 9 / 255, 108 / 255, 1))
        self.exit_btn = Button(text="Exit Game", font_size=24, background_color=(60 / 255, 9 / 255, 108 / 255, 1))

        self.friend_btn.bind(on_release=lambda x: self.start_game('friend'))
        self.bot_btn.bind(on_release=self.show_slider)
        self.exit_btn.bind(on_release=confirm_exit)

        self.layout.add_widget(self.friend_btn)
        self.layout.add_widget(self.bot_btn)
        self.layout.add_widget(self.exit_btn)

        # Slider UI (hidden initially)
        self.slider_label = Label(text="", font_size=20, color=(1, 1, 1, 1))
        self.slider = Slider(min=0, max=2, value=1)
        self.slider.opacity = 0
        self.slider_label.opacity = 0
        self.slider.bind(value=self.on_slider_value_change)
        self.layout.add_widget(self.slider_label)
        self.layout.add_widget(self.slider)

        self.play_bot_button = Button(text="Start Game", font_size=24, background_color=(36/255, 160/255, 70/255, 1),
                                      opacity=0)
        self.play_bot_button.bind(on_release=lambda x: self.start_game('bot'))
        self.layout.add_widget(self.play_bot_button)

        # Back button to return to full selection menu
        self.back_button = Button(text="Back", font_size=20, background_color=(0.4, 0.4, 1, 1), opacity=0)
        self.back_button.bind(on_release=self.show_main_menu)
        self.layout.add_widget(self.back_button)

    def show_slider(self, instance):
        # Hide main buttons
        self.friend_btn.opacity = 0
        self.bot_btn.opacity = 0
        self.exit_btn.opacity = 0
        self.friend_btn.disabled = True
        self.bot_btn.disabled = True
        self.exit_btn.disabled = True

        # Show difficulty options
        self.slider.opacity = 1
        self.slider_label.opacity = 1
        self.play_bot_button.opacity = 1
        self.back_button.opacity = 1
        self.on_slider_value_change(self.slider, self.slider.value)

    def show_main_menu(self, instance):
        # Show main buttons
        self.friend_btn.opacity = 1
        self.bot_btn.opacity = 1
        self.exit_btn.opacity = 1
        self.friend_btn.disabled = False
        self.bot_btn.disabled = False
        self.exit_btn.disabled = False

        # Hide difficulty options
        self.slider.opacity = 0
        self.slider_label.opacity = 0
        self.play_bot_button.opacity = 0
        self.back_button.opacity = 0

    def on_slider_value_change(self, instance, value):
        global difficulty
        rounded = round(value)
        level_map = {
            0: ("easy", (0.2, 1, 0.2, 1)),  # Green
            1: ("medium", (1, 0.6, 0, 1)),  # Orange
            2: ("hard", (1, 0.2, 0.2, 1))   # Red
        }
        level, color = level_map[rounded]
        difficulty = level
        self.slider_label.text = f"Difficulty: {difficulty.capitalize()}"
        self.slider_label.color = color

    def start_game(self, selected_mode):
        global mode
        mode = selected_mode
        self.manager.get_screen('game').reset_game()
        self.manager.current = "game"


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        # Game grid layout
        self.grid_layout = GridLayout(cols=3, spacing=5, padding=10, size_hint=(1, 0.85))
        self.main_layout.add_widget(self.grid_layout)

        # Undo/Redo layout
        self.control_layout = BoxLayout(size_hint=(1, 0.15), spacing=10, padding=[10, 10])
        self.undo_btn = Button(text="Undo", font_size=20, background_color=(0.4, 0.4, 0.7, 1))
        self.redo_btn = Button(text="Redo", font_size=20, background_color=(0.2, 0.5, 0.2, 1))
        self.undo_btn.bind(on_release=self.undo_move)
        self.redo_btn.bind(on_release=self.redo_move)
        self.control_layout.add_widget(self.undo_btn)
        self.control_layout.add_widget(self.redo_btn)

        self.main_layout.add_widget(self.control_layout)
        self.add_widget(self.main_layout)

        self.buttons = []
        self.x_state = [0] * 9
        self.z_state = [0] * 9
        self.turn = 1

        self.history = []  # stores (index, player) tuples
        self.redo_stack = []

        self.build_board()

    def build_board(self):
        self.grid_layout.clear_widgets()
        self.buttons.clear()
        for i in range(9):
            button = Button(font_size=48, background_color=button_bg_color)
            button.bind(on_release=lambda btn, idx=i: self.button_click(btn, idx))
            self.grid_layout.add_widget(button)
            self.buttons.append(button)

    def button_click(self, button, index):
        if self.x_state[index] == 0 and self.z_state[index] == 0:
            if self.turn == 1:
                button.text = "X"
                button.color = x_color
                self.x_state[index] = 1
                self.history.append((index, 'X'))
                self.redo_stack.clear()
            else:
                button.text = "O"
                button.color = o_color
                self.z_state[index] = 1
                self.history.append((index, 'O'))
                self.redo_stack.clear()
            self.check_and_continue()

    def check_and_continue(self):
        winner = check_win(self.x_state, self.z_state)
        if winner != -1:
            if winner == 1:
                self.manager.get_screen('result').set_result("X Won the Match!")
            else:
                self.manager.get_screen('result').set_result("O Won the Match!")
            self.manager.current = 'result'
        elif all(self.x_state[i] or self.z_state[i] for i in range(9)):
            self.manager.get_screen('result').set_result("It's a Draw!")
            self.manager.current = 'result'
        else:
            self.turn = 1 - self.turn
            if mode == "bot" and self.turn == 0:
                Clock.schedule_once(lambda dt: self.bot_move(), 0.2)

    def bot_move(self):
        if difficulty == "easy":
            move = best_move_easy(self.x_state, self.z_state)
        elif difficulty == "medium":
            move = best_move_medium(self.x_state, self.z_state)
        elif difficulty == "hard":
            move = best_move_hard(self.x_state, self.z_state)
        if move:
            idx = move[0] * 3 + move[1]
            if self.x_state[idx] == 0 and self.z_state[idx] == 0:
                self.buttons[idx].text = "O"
                self.buttons[idx].color = o_color
                self.z_state[idx] = 1
                self.history.append((idx, 'O'))
                self.redo_stack.clear()
                self.check_and_continue()

    def undo_move(self, instance=None):
        if not self.history:
            return

        index, player = self.history.pop()
        self.redo_stack.append((index, player))

        self.buttons[index].text = ""
        self.buttons[index].color = (1, 1, 1, 1)

        if player == 'X':
            self.x_state[index] = 0
            self.turn = 1
        else:
            self.z_state[index] = 0
            self.turn = 0

    def redo_move(self, instance=None):
        if not self.redo_stack:
            return

        index, player = self.redo_stack.pop()
        self.history.append((index, player))

        if player == 'X':
            self.buttons[index].text = "X"
            self.buttons[index].color = x_color
            self.x_state[index] = 1
            self.turn = 0
        else:
            self.buttons[index].text = "O"
            self.buttons[index].color = o_color
            self.z_state[index] = 1
            self.turn = 1

    def reset_game(self):
        self.x_state = [0] * 9
        self.z_state = [0] * 9
        self.turn = 1
        self.history.clear()
        self.redo_stack.clear()
        for button in self.buttons:
            button.text = ""
            button.color = (1, 1, 1, 1)
            button.background_color = button_bg_color


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.label = Label(text="", font_size=32, color=(1, 1, 1, 1))
        layout.add_widget(self.label)

        play_again_btn = Button(text="Play Again", font_size=24, background_color=(60 / 255, 9 / 255, 108 / 255, 1))
        home_btn = Button(text="Home", font_size=24, background_color=(60 / 255, 9 / 255, 108 / 255, 1))

        play_again_btn.bind(on_release=self.play_again)
        home_btn.bind(on_release=self.go_home)

        layout.add_widget(play_again_btn)
        layout.add_widget(home_btn)

        self.add_widget(layout)

    def set_result(self, text):
        self.label.text = text

    def play_again(self, instance):
        self.manager.get_screen('game').reset_game()
        self.manager.current = 'game'

    def go_home(self, instance):
        self.manager.current = 'mode'


class TicTacToeApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ModeScreen(name='mode'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ResultScreen(name='result'))
        return sm


if __name__ == '__main__':
    TicTacToeApp().run()
