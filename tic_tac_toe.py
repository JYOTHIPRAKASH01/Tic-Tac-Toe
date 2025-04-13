import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        # Game state variables
        self.current_player = "X"
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.game_active = True
        self.ai_enabled = False
        
        # Set up the main window
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.configure(bg="#f0f0f0")
        
        # Create and place the game title
        title_frame = tk.Frame(self.window, bg="#f0f0f0")
        title_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        
        title_label = tk.Label(title_frame, text="Tic Tac Toe", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack()
        
        # Create game board frame
        game_frame = tk.Frame(self.window, bg="#f0f0f0")
        game_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # Create buttons for the game board
        self.buttonsGrid = []
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(
                    game_frame, 
                    text="",
                    width=10,
                    height=5,
                    font=("Arial", 12, "bold"),
                    bg="#ffffff",
                    command=lambda i=i, j=j: self.make_move(i, j)
                )
                button.grid(row=i, column=j, padx=3, pady=3)
                row.append(button)
            self.buttonsGrid.append(row)
        
        # Create status frame for displaying current player
        status_frame = tk.Frame(self.window, bg="#f0f0f0")
        status_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame, 
            text=f"Current Player: {self.current_player}", 
            font=("Arial", 12),
            bg="#f0f0f0"
        )
        self.status_label.pack()
        
        # Create score frame
        score_frame = tk.Frame(self.window, bg="#f0f0f0")
        score_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        
        tk.Label(score_frame, text="Score:", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=3)
        tk.Label(score_frame, text="Player X:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0)
        tk.Label(score_frame, text="Player O:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=1)
        tk.Label(score_frame, text="Draws:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=2)
        
        self.score_x_label = tk.Label(score_frame, text="0", font=("Arial", 10), bg="#f0f0f0")
        self.score_x_label.grid(row=2, column=0)
        
        self.score_o_label = tk.Label(score_frame, text="0", font=("Arial", 10), bg="#f0f0f0")
        self.score_o_label.grid(row=2, column=1)
        
        self.score_draw_label = tk.Label(score_frame, text="0", font=("Arial", 10), bg="#f0f0f0")
        self.score_draw_label.grid(row=2, column=2)
        
        # Create control buttons frame
        button_frame = tk.Frame(self.window, bg="#f0f0f0")
        button_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        
        # Create reset game button
        reset_button = tk.Button(
            button_frame,
            text="Reset Game",
            font=("Arial", 10),
            bg="#e1e1e1",
            command=self.reset_game
        )
        reset_button.grid(row=0, column=0, padx=5)
        
        # Create toggle AI button
        self.ai_button = tk.Button(
            button_frame,
            text="Enable AI",
            font=("Arial", 10),
            bg="#e1e1e1",
            command=self.toggle_ai
        )
        self.ai_button.grid(row=0, column=1, padx=5)
        
        # Create reset scores button
        reset_scores_button = tk.Button(
            button_frame,
            text="Reset Scores",
            font=("Arial", 10),
            bg="#e1e1e1",
            command=self.reset_scores
        )
        reset_scores_button.grid(row=0, column=2, padx=5)

    def make_move(self, row, col):
        # Only allow moves if the game is active and the cell is empty
        if self.game_active and self.board[row][col] == "":
            # Update the board state and button text
            self.board[row][col] = self.current_player
            self.buttonsGrid[row][col].config(
                text=self.current_player,
                bg="#ffcccc" if self.current_player == "X" else "#ccccff"
            )
            
            # Check for a winner
            if self.check_winner(self.current_player):
                self.handle_win()
                return
            
            # Check for a draw
            elif self.is_draw():
                self.handle_draw()
                return
            
            # Switch to the next player
            self.switch_player()
            
            # If AI is enabled and it's O's turn, make an AI move
            if self.ai_enabled and self.current_player == "O" and self.game_active:
                self.window.after(500, self.ai_move)
    
    def ai_move(self):
        # Simple AI: First try to win, then block, then take center, then random
        
        # Try to find a winning move
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "O"
                    if self.check_winner("O"):
                        self.make_move(i, j)
                        return
                    self.board[i][j] = ""
        
        # Try to block X from winning
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = "X"
                    if self.check_winner("X"):
                        self.board[i][j] = ""
                        self.make_move(i, j)
                        return
                    self.board[i][j] = ""
        
        # Take the center if available
        if self.board[1][1] == "":
            self.make_move(1, 1)
            return
        
        # Take any available corner
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        random.shuffle(corners)
        for i, j in corners:
            if self.board[i][j] == "":
                self.make_move(i, j)
                return
        
        # Take any available side
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        random.shuffle(sides)
        for i, j in sides:
            if self.board[i][j] == "":
                self.make_move(i, j)
                return
    
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.status_label.config(text=f"Current Player: {self.current_player}")
    
    def check_winner(self, player):
        # Check rows
        for i in range(3):
            if player == self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
        
        # Check columns
        for i in range(3):
            if player == self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        
        # Check diagonals
        if player == self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if player == self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        
        return False
    
    def is_draw(self):
        for row in self.board:
            if "" in row:
                return False
        return True
    
    def handle_win(self):
        self.game_active = False
        self.scores[self.current_player] += 1
        self.update_score_display()
        
        messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
        
        # Ask if they want to play again
        play_again = messagebox.askyesno("Play Again", "Would you like to play another game?")
        if play_again:
            self.reset_game()
    
    def handle_draw(self):
        self.game_active = False
        self.scores["Draw"] += 1
        self.update_score_display()
        
        messagebox.showinfo("Game Over", "It's a draw!")
        
        # Ask if they want to play again
        play_again = messagebox.askyesno("Play Again", "Would you like to play another game?")
        if play_again:
            self.reset_game()
    
    def update_score_display(self):
        self.score_x_label.config(text=str(self.scores["X"]))
        self.score_o_label.config(text=str(self.scores["O"]))
        self.score_draw_label.config(text=str(self.scores["Draw"]))
    
    def reset_game(self):
        # Reset the game board
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        for i in range(3):
            for j in range(3):
                self.buttonsGrid[i][j].config(text="", bg="#ffffff")
        
        # Reset game state
        self.game_active = True
        self.current_player = "X"
        self.status_label.config(text=f"Current Player: {self.current_player}")
        
        # If AI is enabled and it's O's turn, make an AI move
        if self.ai_enabled and self.current_player == "O":
            self.window.after(500, self.ai_move)
    
    def reset_scores(self):
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.update_score_display()
    
    def toggle_ai(self):
        self.ai_enabled = not self.ai_enabled
        if self.ai_enabled:
            self.ai_button.config(text="Disable AI")
            if self.current_player == "O" and self.game_active:
                self.window.after(500, self.ai_move)
        else:
            self.ai_button.config(text="Enable AI")
    
    def run(self):
        # Start the main event loop
        self.window.mainloop()

# Create and run the game
if __name__ == "__main__":
    game = TicTacToe()
    game.run()
