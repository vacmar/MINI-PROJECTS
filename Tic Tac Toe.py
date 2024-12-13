import tkinter as tk
import random

def print_board():
    for i in range(3):
        for j in range(3):
            cell = board[i][j]
            if cell:
                buttons[i][j].config(text=cell, state="disabled")
            else:
                buttons[i][j].config(text="", state="normal")

def check_win(player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or \
            all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def get_available_moves():
    return [(i, j) for i in range(3) for j in range(3) if not board[i][j]]

def get_random_move():
    return random.choice(get_available_moves())

def on_click(row, col):
    global player_X_score, player_O_score
    if not board[row][col]:
        board[row][col] = current_player
        print_board()
        if check_win(current_player):
            if current_player == "X":
                player_X_score += 1
            else:
                player_O_score += 1
            update_score_label()
            label.config(text=f"Player {current_player} wins!")
            disable_buttons()
        elif all(all(cell for cell in row) for row in board):
            label.config(text="It's a tie!")
        else:
            switch_player()

def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state="disabled")

def switch_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

def update_score_label():
    score_label.config(text=f"Player X: {player_X_score}  Player O: {player_O_score}")

def play_game():
    global board, current_player
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    print_board()
    update_score_label()
    enable_buttons()

def enable_buttons():
    for row in buttons:
        for button in row:
            button.config(state="normal")

def exit_game():
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.attributes('-fullscreen', True)  # Making the window fullscreen

    game_frame = tk.Frame(root)
    game_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    buttons = [[tk.Button(game_frame, width=10, height=5, font=("Helvetica", 16), command=lambda row=i, col=j: on_click(row, col)) for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].grid(row=i, column=j, sticky="nsew")

    label = tk.Label(root, text="Player X's turn", font=("Helvetica", 20))
    label.pack()

    player_X_score = 0
    player_O_score = 0
    score_label = tk.Label(root, text=f"Player X: {player_X_score}  Player O: {player_O_score}", font=("Helvetica", 16))
    score_label.pack()

    play_game_button = tk.Button(root, text="Play Again", font=("Helvetica", 16), command=play_game)
    play_game_button.pack()

    exit_button = tk.Button(root, text="Exit", font=("Helvetica", 16), command=exit_game)
    exit_button.pack()

    play_game()

    root.mainloop()
