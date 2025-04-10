# -*- coding: utf-8 -*-
"""ChessGame.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zfQEthTJBJuWfdUVtKoDAjOBf0Gx5fnv

# Chess Game - OOP Design

## 📋 Requirements

- The chess game follows the **standard rules of chess**.
- It supports **two players**, each controlling their own set of pieces.
- The game board is an **8x8 grid** with alternating black and white squares.
- Each player has **16 pieces**:
  - 1 King
  - 1 Queen
  - 2 Rooks
  - 2 Bishops
  - 2 Knights
  - 8 Pawns
- The game:
  - Validates **legal moves** for each piece.
  - **Prevents illegal moves**.
  - Detects **checkmate** and **stalemate** conditions.
  - Handles **alternate player turns**.

---

## 🧱 Class Design

### 🧩 `Piece` (Abstract Class)
Represents a chess piece.

- **Attributes**:
  - `Color color`
  - `int row, col`
- **Abstract Method**:
  - `boolean canMove(Board board, int destRow, int destCol)`

---

### ♛ Piece Subclasses

Each subclass implements its movement logic:

- `King`
- `Queen`
- `Rook`
- `Bishop`
- `Knight`
- `Pawn`

---

### 🗺️ `Board` Class

Manages the board state and piece placement.

- Stores an 8x8 grid of `Piece` objects.
- Provides methods to:
  - Get/set pieces.
  - Validate moves.
  - Detect check/checkmate/stalemate.

---

### 👤 `Player` Class

Represents a player in the game.

- **Attributes**:
  - `Color color`
- **Methods**:
  - `Move makeMove(Board board)`

---

### ➡️ `Move` Class

Represents a move made by a player.

- **Attributes**:
  - `Piece piece`
  - `int destRow, destCol`

---

### 🎮 `Game` Class

Handles game orchestration.

- Initializes the board and players.
- Manages player turns.
- Determines the game result.

---

### 🚀 `ChessGame` Class

Entry point of the application. Starts the game loop.

---

## ♟️ Fool’s Mate Strategy (Dry Run)

This is the **fastest checkmate** in chess, occurring in just two moves:

> f3 (White)

> e5 (Black)

> g4 (White)

> Qh4# (Black wins)
"""

class Move:
    def __init__(self, piece, dest_row, dest_col):
        self.piece = piece
        self.dest_row = dest_row
        self.dest_col = dest_col

from enum import Enum

class Color(Enum):
    WHITE = 1
    BLACK = 2

from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col

    @abstractmethod
    def can_move(self, board, dest_row, dest_col):
        pass

class Bishop(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = abs(dest_row - self.row)
        col_diff = abs(dest_col - self.col)
        return row_diff == col_diff

class King(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = abs(dest_row - self.row)
        col_diff = abs(dest_col - self.col)
        return row_diff <= 1 and col_diff <= 1

class Knight(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = abs(dest_row - self.row)
        col_diff = abs(dest_col - self.col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

class Pawn(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = dest_row - self.row
        col_diff = abs(dest_col - self.col)

        if self.color == Color.WHITE:
            return (row_diff == 1 and col_diff == 0) or \
                   (self.row == 1 and row_diff == 2 and col_diff == 0) or \
                   (row_diff == 1 and col_diff == 1 and board.get_piece(dest_row, dest_col) is not None)
        else:
            return (row_diff == -1 and col_diff == 0) or \
                   (self.row == 6 and row_diff == -2 and col_diff == 0) or \
                   (row_diff == -1 and col_diff == 1 and board.get_piece(dest_row, dest_col) is not None)

class Queen(Piece):
    def can_move(self, board, dest_row, dest_col):
        row_diff = abs(dest_row - self.row)
        col_diff = abs(dest_col - self.col)
        return (row_diff == col_diff) or (self.row == dest_row or self.col == dest_col)

class Rook(Piece):
    def can_move(self, board, dest_row, dest_col):
        return self.row == dest_row or self.col == dest_col

class Player:
    def __init__(self, color):
        self.color = color

    def make_move(self, board, move):
        piece = move.piece
        dest_row = move.dest_row
        dest_col = move.dest_col

        if board.is_valid_move(piece, dest_row, dest_col):
            source_row = piece.row
            source_col = piece.col
            board.set_piece(source_row, source_col, None)
            board.set_piece(dest_row, dest_col, piece)
            piece.row = dest_row
            piece.col = dest_col
        else:
            raise ValueError("Invalid move!")

import copy

class Board:
    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        self._initialize_board()

    def _initialize_board(self):
        # Initialize white pieces
        self.board[0][0] = Rook(Color.WHITE, 0, 0)
        self.board[0][1] = Knight(Color.WHITE, 0, 1)
        self.board[0][2] = Bishop(Color.WHITE, 0, 2)
        self.board[0][3] = Queen(Color.WHITE, 0, 3)
        self.board[0][4] = King(Color.WHITE, 0, 4)
        self.board[0][5] = Bishop(Color.WHITE, 0, 5)
        self.board[0][6] = Knight(Color.WHITE, 0, 6)
        self.board[0][7] = Rook(Color.WHITE, 0, 7)
        for i in range(8):
            self.board[1][i] = Pawn(Color.WHITE, 1, i)

        # Initialize black pieces
        self.board[7][0] = Rook(Color.BLACK, 7, 0)
        self.board[7][1] = Knight(Color.BLACK, 7, 1)
        self.board[7][2] = Bishop(Color.BLACK, 7, 2)
        self.board[7][3] = Queen(Color.BLACK, 7, 3)
        self.board[7][4] = King(Color.BLACK, 7, 4)
        self.board[7][5] = Bishop(Color.BLACK, 7, 5)
        self.board[7][6] = Knight(Color.BLACK, 7, 6)
        self.board[7][7] = Rook(Color.BLACK, 7, 7)
        for i in range(8):
            self.board[6][i] = Pawn(Color.BLACK, 6, i)

    def get_piece(self, row, col):
        return self.board[row][col]

    def set_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_move(self, piece, dest_row, dest_col):
        if piece is None or dest_row < 0 or dest_row > 7 or dest_col < 0 or dest_col > 7:
            return False
        dest_piece = self.board[dest_row][dest_col]
        return (dest_piece is None or dest_piece.color != piece.color) and \
               piece.can_move(self, dest_row, dest_col)

    def is_in_check(self, color, king_row, king_col):
        # Directions for sliding pieces (Rook, Bishop, Queen)
        directions = [
            (-1, 0),  # Up (Vertical)
            (1, 0),   # Down (Vertical)
            (0, -1),  # Left (Horizontal)
            (0, 1),   # Right (Horizontal)
            (-1, -1), # Top-left (Diagonal)
            (-1, 1),  # Top-right (Diagonal)
            (1, -1),  # Bottom-left (Diagonal)
            (1, 1),   # Bottom-right (Diagonal)
        ]
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color != color:
                    # Check if this piece can attack the king's position
                    if isinstance(piece, Rook) or isinstance(piece, Queen):
                        if piece.can_move(self, king_row, king_col):
                            # Check if the path is blocked for rooks/queens (only horizontal/vertical)
                            if row == king_row or col == king_col:
                                step_row = (king_row - row) // max(1, abs(king_row - row)) if row != king_row else 0
                                step_col = (king_col - col) // max(1, abs(king_col - col)) if col != king_col else 0
                                r, c = row + step_row, col + step_col
                                while r != king_row or c != king_col:
                                    if self.get_piece(r, c) is not None:  # A piece is blocking
                                        break
                                    r += step_row
                                    c += step_col
                                else:
                                    return True  # No blockage, valid attack path found
                    if isinstance(piece, Bishop) or isinstance(piece, Queen):
                        if piece.can_move(self, king_row, king_col):
                            # Check if the diagonal path is blocked
                            if abs(row - king_row) == abs(col - king_col):
                                step_row = (king_row - row) // max(1, abs(king_row - row)) if row != king_row else 0
                                step_col = (king_col - col) // max(1, abs(king_col - col)) if col != king_col else 0
                                r, c = row + step_row, col + step_col
                                while r != king_row or c != king_col:
                                    if self.get_piece(r, c) is not None:  # A piece is blocking
                                        break
                                    r += step_row
                                    c += step_col
                                else:
                                    return True  # No blockage, valid attack path found
                    if isinstance(piece, Knight):
                        if piece.can_move(self, king_row, king_col):
                            return True  # Knights can jump over pieces, so just check if they can attack

                    if isinstance(piece, Pawn):
                        # Pawns only attack diagonally, so check if the opponent pawn can attack the king
                        if piece.can_move(self, king_row, king_col):
                            return True  # Pawn attacks in a specific way

                    if isinstance(piece, King):
                        if piece.can_move(self, king_row, king_col):
                            return True  # Check if an opposing king can attack

        return False  # No piece can attack the king


    def copy_board(self):
        # Create a new Board instance and copy the pieces to it
        new_board = Board()
        new_board.board = copy.deepcopy(self.board)  # Deep copy the board to avoid reference issues
        return new_board


    def is_checkmate(self, color):
        # Step 1: Find the king of the current color
        king = None
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king = piece
                    break
            if king:
                break

        # Step 2: Check if the king is in check
        if not self.is_in_check(color, king.row, king.col):
            return False
        print("King in Check")
        # Step 3: Try all possible moves of the current player to see if any remove the check


        return True  # No moves prevent check, so it's checkmate



    def is_stalemate(self, color):
        # Step 1: Find the king of the current color
        king = None
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king = piece
                    break
            if king:
                break

        # Step 2: Check if the king is not in check
        if self.is_in_check(color, king.row, king.col):
            return False  # If the king is in check, it's not stalemate

        # Step 3: Check if the current player has any legal moves
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    for dest_row in range(8):
                        for dest_col in range(8):
                            if self.is_valid_move(piece, dest_row, dest_col):
                                return False  # Found a legal move

        return True  # No legal moves, so it's stalemate


    def display_board(self):
      # Iterate through the board and print the pieces in the desired format
      for row in self.board:
          row_display = ""
          for piece in row:
              if piece is None:
                  row_display += ". "
              else:
                  if isinstance(piece, King):
                      row_display += "K "
                  elif isinstance(piece, Queen):
                      row_display += "Q "
                  elif isinstance(piece, Rook):
                      row_display += "R "
                  elif isinstance(piece, Pawn):
                      row_display += "P "
                  elif isinstance(piece, Knight):
                      row_display += "Kn "
                  elif isinstance(piece, Bishop):
                      row_display += "B "
          print(row_display.strip())  # Remove the trailing space at the end of each row
      print("\n")  # Add a newline after the board for better readability

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player(Color.WHITE), Player(Color.BLACK)]
        self.current_player = 0

    def start(self):
        # Game loop

        while not self._is_game_over():

            self.board.display_board()

            player = self.players[self.current_player]
            print(f"{player.color.name}'s turn.")

            # Get move from the player
            move = self._get_player_move(player)


            # Make the move on the board
            player.make_move(self.board, move)

            # Switch to the next player
            self.current_player = (self.current_player + 1) % 2

        # Display game result
        self._display_result()

    def _is_game_over(self):
        return self.board.is_checkmate(Color.WHITE) or self.board.is_checkmate(Color.BLACK) or \
               self.board.is_stalemate(Color.WHITE) or self.board.is_stalemate(Color.BLACK)

    def _get_player_move(self, player):
        # TODO: Implement logic to get a valid move from the player
        # For simplicity, let's assume the player enters the move via console input
        source_row = int(input("Enter source row: "))
        source_col = int(input("Enter source column: "))
        dest_row = int(input("Enter destination row: "))
        dest_col = int(input("Enter destination column: "))

        piece = self.board.get_piece(source_row, source_col)
        if piece is None or piece.color != player.color:
            raise ValueError("Invalid piece selection!")

        return Move(piece, dest_row, dest_col)

    def _display_result(self):
        if self.board.is_checkmate(Color.WHITE):
            print("Black wins by checkmate!")
        elif self.board.is_checkmate(Color.BLACK):
            print("White wins by checkmate!")
        elif self.board.is_stalemate(Color.WHITE) or self.board.is_stalemate(Color.BLACK):
            print("The game ends in a stalemate!")

class ChessGameDemo:
    @staticmethod
    def run():
        game = Game()
        game.start()

if __name__ == "__main__":
    ChessGameDemo.run()

# R Kn B Q K B Kn R
# P  P P P P . .  P
# .  . . . . P .  .
# .  . . . . . P  Q
# .  . . . . . .  .
# .  . . . P . .  .
# P  P P P . P P  P
# R Kn B . K B Kn R