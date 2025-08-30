# -*- coding: utf-8 -*-

import customtkinter as ctk
from PIL import Image, ImageTk
import base64
import io
import math
import random
import time
import threading
import requests

# This function fetches images from URLs and converts them to Base64.
# It's a dynamic replacement for the static IMAGE_DATA dictionary.
import os
import json
import requests
import base64
import io
from PIL import Image

# --- Asset and Cache Configuration ---
ASSETS_DIR = ".\\assets"
CACHE_FILE = os.path.join(ASSETS_DIR, "image_data.json")

def load_or_create_image_data():
    """
    Loads Base64 image data from a JSON cache if it exists.
    If not, it downloads images, processes them, saves them locally,
    and creates the JSON cache for future use.
    """
    # 1. Try to load from cache first for fast startup
    if os.path.exists(CACHE_FILE):
        print(f"Loading cached image data from {CACHE_FILE}...")
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read cache file. Re-generating... Error: {e}")

    print("Image cache not found. Generating new image data...")
    
    # 2. If cache fails, create the assets directory
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    # Latest URLs for the chess piece images
    image_urls = {
        'b_queen': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025946/black_queen.png',
        'b_king': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025948/black_king.png',
        'b_rook': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025345/black_rook.png',
        'b_bishop': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025951/black_bishop.png',
        'b_knight': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025947/black_knight.png',
        'b_pawn': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025945/black_pawn.png',
        'w_queen': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025952/white_queen.png',
        'w_king': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025943/white_king.png',
        'w_rook': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025949/white_rook.png',
        'w_bishop': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025944/white_bishop.png',
        'w_knight': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025325/white_knight.png',
        'w_pawn': 'https://media.geeksforgeeks.org/wp-content/uploads/20240302025953/white_pawn.png'
    }

    generated_image_data = {}

    for name, url in image_urls.items():
        image_filename = f"{name}.png"
        local_path = os.path.join(ASSETS_DIR, image_filename)

        # 3. Check if image exists locally, otherwise download it
        if not os.path.exists(local_path):
            try:
                print(f"Downloading {image_filename}...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                print(f"Fatal: Could not download {name}. Error: {e}")
                # Assign a blank string and continue, or you could exit
                generated_image_data[name] = ""
                continue
        else:
            print(f"Found {image_filename} in local assets.")
            
        # 4. Process the local image file to create Base64 data
        try:
            with Image.open(local_path) as img:
                img = img.convert("RGBA")
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue())
                generated_image_data[name] = img_base64.decode('utf-8')
        except IOError as e:
            print(f"Fatal: Could not process image {local_path}. Error: {e}")
            generated_image_data[name] = ""

    # 5. Save the newly generated data to the cache file
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(generated_image_data, f, indent=4)
        print(f"Image data cache created at {CACHE_FILE}")
    except IOError as e:
        print(f"Warning: Could not save cache file. Error: {e}")

    return generated_image_data

# --- Main data loading section ---
# This single function call handles everything.
IMAGE_DATA = load_or_create_image_data()

# --- AI and Game Logic Constants ---
PIECE_VALUES = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}
CHECKMATE_SCORE = 100000
STALEMATE_SCORE = 0
MAX_DEPTH_DEFAULT = 3

# Piece-Square Tables for positional evaluation
# (Values are flipped for black pieces)
PST = {
    'P': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10,  5,  5],
        [0,  0,  0, 20, 20,  0,  0,  0],
        [5, -5,-10,  0,  0,-10, -5,  5],
        [5, 10, 10,-20,-20, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ],
    'N': [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ],
    'B': [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ],
    'R': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ],
    'Q': [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [-5,  0,  5,  5,  5,  5,  0, -5],
        [0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ],
    'K': [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [20, 30, 10,  0,  0, 10, 30, 20]
    ]
}


class ChessLogic:
    def __init__(self):
        self.new_game()

    def new_game(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enpassant_possible = ()
        self.current_castling_rights = {"wks": True, "wqs": True, "bks": True, "bqs": True}
        self.castle_rights_log = [{"wks": True, "wqs": True, "bks": True, "bqs": True}]

    def make_move(self, move):
        if not move: return
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == "wK": self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK": self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_col] = "--"

        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ((move.start_row + move.end_row) // 2, move.start_col)
        else:
            self.enpassant_possible = ()

        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
            else:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]
                self.board[move.end_row][move.end_col - 2] = '--'

        self.update_castling_rights(move)
        self.castle_rights_log.append(self.current_castling_rights.copy())

    def undo_move(self):
        if not self.move_log: return
        move = self.move_log.pop()
        self.board[move.start_row][move.start_col] = move.piece_moved
        self.board[move.end_row][move.end_col] = move.piece_captured
        self.white_to_move = not self.white_to_move
        if move.piece_moved == "wK": self.white_king_location = (move.start_row, move.start_col)
        elif move.piece_moved == "bK": self.black_king_location = (move.start_row, move.start_col)

        if move.is_enpassant_move:
            self.board[move.end_row][move.end_col] = "--"
            self.board[move.start_row][move.end_col] = move.piece_captured
            self.enpassant_possible = (move.end_row, move.end_col)
        
        if move.piece_moved[1] == 'P' and abs(move.start_row - move.end_row) == 2:
            self.enpassant_possible = ()

        self.castle_rights_log.pop()
        self.current_castling_rights = self.castle_rights_log[-1].copy()

        if move.is_castle_move:
            if move.end_col - move.start_col == 2:
                self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 1]
                self.board[move.end_row][move.end_col - 1] = '--'
            else:
                self.board[move.end_row][move.end_col - 2] = self.board[move.end_row][move.end_col + 1]
                self.board[move.end_row][move.end_col + 1] = '--'
        
        self.checkmate = False
        self.stalemate = False

    def update_castling_rights(self, move):
        if move.piece_moved == 'wK':
            self.current_castling_rights['wks'] = False
            self.current_castling_rights['wqs'] = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights['bks'] = False
            self.current_castling_rights['bqs'] = False
        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0: self.current_castling_rights['wqs'] = False
                elif move.start_col == 7: self.current_castling_rights['wks'] = False
        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0: self.current_castling_rights['bqs'] = False
                elif move.start_col == 7: self.current_castling_rights['bks'] = False
        
        if move.piece_captured == 'wR' and move.end_row == 7:
            if move.end_col == 0: self.current_castling_rights['wqs'] = False
            elif move.end_col == 7: self.current_castling_rights['wks'] = False
        elif move.piece_captured == 'bR' and move.end_row == 0:
            if move.end_col == 0: self.current_castling_rights['bqs'] = False
            elif move.end_col == 7: self.current_castling_rights['bks'] = False


    def get_valid_moves(self):
        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        king_row, king_col = self.white_king_location if self.white_to_move else self.black_king_location

        if self.in_check:
            if len(self.checks) == 1:
                check = self.checks[0]
                check_row, check_col = check[0], check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == 'N':
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col: break
                
                moves = self.get_all_possible_moves()
                moves = [move for move in moves if move.piece_moved[1] == 'K' or \
                         (move.end_row, move.end_col) in valid_squares]
            else: # Double check
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_possible_moves()
        
        self.get_castle_moves(king_row, king_col, moves)
        
        if len(moves) == 0:
            if self.in_check: self.checkmate = True
            else: self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        return moves

    def is_square_attacked(self, r, c):
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opp_moves:
            if move.end_row == r and move.end_col == c:
                return True
        return False

    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        ally_color = "w" if self.white_to_move else "b"
        enemy_color = "b" if self.white_to_move else "w"
        start_row, start_col = self.white_king_location if self.white_to_move else self.black_king_location

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        if (0 <= j <= 3 and piece_type == 'R') or \
                           (4 <= j <= 7 and piece_type == 'B') or \
                           (i == 1 and piece_type == 'P' and ((enemy_color == 'w' and 6 <= j <= 7) or (enemy_color == 'b' and 4 <= j <= 5))) or \
                           (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break
        
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
        return in_check, pins, checks

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    if piece == 'P': self.get_pawn_moves(r, c, moves)
                    elif piece == 'R': self.get_rook_moves(r, c, moves)
                    elif piece == 'N': self.get_knight_moves(r, c, moves)
                    elif piece == 'B': self.get_bishop_moves(r, c, moves)
                    elif piece == 'Q': self.get_queen_moves(r, c, moves)
                    elif piece == 'K': self.get_king_moves(r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        move_amount = -1 if self.white_to_move else 1
        start_row = 6 if self.white_to_move else 1
        enemy_color = 'b' if self.white_to_move else 'w'
        king_row, king_col = self.white_king_location if self.white_to_move else self.black_king_location

        if self.board[r + move_amount][c] == "--":
            if not piece_pinned or pin_direction == (move_amount, 0) or pin_direction == (-move_amount, 0):
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * move_amount, c), self.board))

        if c - 1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board))
                elif (r + move_amount, c - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c:
                            inside_range = range(king_col + 1, c -1)
                            outside_range = range(c + 1, 8)
                        else:
                            inside_range = range(king_col -1, c, -1)
                            outside_range = range(c-2, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_amount, c-1), self.board, is_enpassant_move=True))

        if c + 1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[r + move_amount][c + 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board))
                elif (r + move_amount, c + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c:
                            inside_range = range(king_col + 1, c)
                            outside_range = range(c + 2, 8)
                        else:
                            inside_range = range(king_col -1, c+1, -1)
                            outside_range = range(c-1, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != "--":
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_amount, c + 1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, r, c, moves):
        self.get_straight_moves(r, c, moves, ((-1, 0), (0, -1), (1, 0), (0, 1)))

    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break
        
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row = r + m[0]
            end_col = c + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        self.get_straight_moves(r, c, moves, ((-1, -1), (-1, 1), (1, -1), (1, 1)))

    def get_queen_moves(self, r, c, moves):
        self.get_straight_moves(r, c, moves, ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)))

    def get_king_moves(self, r, c, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row = r + row_moves[i]
            end_col = c + col_moves[i]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    if ally_color == 'w': self.white_king_location = (end_row, end_col)
                    else: self.black_king_location = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if ally_color == 'w': self.white_king_location = (r, c)
                    else: self.black_king_location = (r, c)

    def get_straight_moves(self, r, c, moves, directions):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q': self.pins.remove(self.pins[i])
                break

        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break
                        else: break
                else: break

    def get_castle_moves(self, r, c, moves):
        if self.is_square_attacked(r, c): return
        if (self.white_to_move and self.current_castling_rights['wks']) or \
           (not self.white_to_move and self.current_castling_rights['bks']):
            self.get_kingside_castle_moves(r, c, moves)
        if (self.white_to_move and self.current_castling_rights['wqs']) or \
           (not self.white_to_move and self.current_castling_rights['bqs']):
            self.get_queenside_castle_moves(r, c, moves)

    def get_kingside_castle_moves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.is_square_attacked(r, c + 1) and not self.is_square_attacked(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, is_castle_move=True))

    def get_queenside_castle_moves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.is_square_attacked(r, c - 1) and not self.is_square_attacked(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, is_castle_move=True))


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row, self.start_col = start_sq
        self.end_row, self.end_col = end_sq
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        
        self.is_pawn_promotion = (self.piece_moved == 'wP' and self.end_row == 0) or \
                                 (self.piece_moved == 'bP' and self.end_row == 7)
        
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = 'wP' if self.piece_moved == 'bP' else 'bP'
            
        self.is_castle_move = is_castle_move
        self.is_capture = self.piece_captured != "--"
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        return isinstance(other, Move) and self.move_id == other.move_id

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
        
    def __str__(self):
        if self.is_castle_move:
            return "O-O" if self.end_col == 6 else "O-O-O"

        end_square = self.get_rank_file(self.end_row, self.end_col)
        
        if self.piece_moved[1] == 'P':
            if self.is_capture:
                return self.cols_to_files[self.start_col] + "x" + end_square
            else:
                return end_square
        
        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square


class ChessAI:
    @staticmethod
    def find_best_move(game_state, valid_moves, depth, human_like=True):
        if not valid_moves: return None
        
        start_time = time.time()
        
        # At low levels, introduce some randomness
        if depth <= 2 and human_like:
            if random.random() < 0.3: # 30% chance of a random (but valid) move
                return valid_moves[random.randint(0, len(valid_moves) - 1)]

        turn_multiplier = 1 if game_state.white_to_move else -1
        opponent_min_max_score = CHECKMATE_SCORE
        best_player_move = None
        
        # Shuffle for move variety
        random.shuffle(valid_moves)

        for player_move in valid_moves:
            game_state.make_move(player_move)
            opponents_moves = game_state.get_valid_moves()
            
            if game_state.checkmate:
                opponent_max_score = -CHECKMATE_SCORE
            elif game_state.stalemate:
                opponent_max_score = STALEMATE_SCORE
            else:
                opponent_max_score = -CHECKMATE_SCORE
                for o_move in opponents_moves:
                    game_state.make_move(o_move)
                    game_state.get_valid_moves()
                    if game_state.checkmate:
                        score = CHECKMATE_SCORE
                    elif game_state.stalemate:
                        score = STALEMATE_SCORE
                    else:
                        score = -turn_multiplier * ChessAI.score_board(game_state.board)
                    if score > opponent_max_score:
                        opponent_max_score = score
                    game_state.undo_move()
            
            if opponent_max_score < opponent_min_max_score:
                opponent_min_max_score = opponent_max_score
                best_player_move = player_move
            game_state.undo_move()
        
        end_time = time.time()
        
        # Simulate thinking time
        if human_like:
            elapsed = end_time - start_time
            min_think_time = random.uniform(0.4, 0.8)
            if elapsed < min_think_time:
                time.sleep(min_think_time - elapsed)

        return best_player_move

    @staticmethod
    def find_best_move_minimax(game_state, valid_moves, depth):
        if not valid_moves: return None
        global next_move
        next_move = None
        random.shuffle(valid_moves)
        
        ChessAI.minimax_alpha_beta(game_state, valid_moves, depth, -CHECKMATE_SCORE, CHECKMATE_SCORE, 
                                  1 if game_state.white_to_move else -1)
        return next_move

    @staticmethod
    def minimax_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
        global next_move
        if depth == 0:
            return turn_multiplier * ChessAI.score_board(game_state.board)

        max_score = -CHECKMATE_SCORE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            score = -ChessAI.minimax_alpha_beta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
            if score > max_score:
                max_score = score
                if depth == MAX_DEPTH_DEFAULT:
                    next_move = move
            game_state.undo_move()
            if max_score > alpha:
                alpha = max_score
            if alpha >= beta:
                break
        return max_score

    @staticmethod
    def score_board(board):
        score = 0
        for r in range(8):
            for c in range(8):
                square = board[r][c]
                if square != '--':
                    piece_position_score = 0
                    piece_type = square[1]
                    if piece_type in PST:
                        if square[0] == 'w':
                            piece_position_score = PST[piece_type][r][c]
                        else:
                            piece_position_score = PST[piece_type][7 - r][c]
                    
                    if square[0] == 'w':
                        score += PIECE_VALUES[piece_type] + piece_position_score
                    else:
                        score -= PIECE_VALUES[piece_type] + piece_position_score
        return score


class ChessGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gemini Chess")
        self.geometry("1100x750")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        ctk.set_appearance_mode("Dark")
        self.SQUARE_SIZE = 80
        self.BOARD_WIDTH = self.BOARD_HEIGHT = 8 * self.SQUARE_SIZE
        
        self.game_logic = ChessLogic()
        self.images = {}
        self.valid_moves = self.game_logic.get_valid_moves()
        self.move_made = False
        self.selected_square = ()
        self.player_clicks = []
        self.game_over = False
        self.human_turn = True
        self.ai_thinking = False
        self.auto_play = False
        
        self.create_widgets()
        self.load_images()
        self.draw_game_state()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Board Frame
        self.board_frame = ctk.CTkFrame(self.main_frame, width=self.BOARD_WIDTH, height=self.BOARD_HEIGHT)
        self.board_frame.pack(side="left", padx=10, pady=10)
        self.board_canvas = ctk.CTkCanvas(self.board_frame, width=self.BOARD_WIDTH, height=self.BOARD_HEIGHT, 
                                          highlightthickness=0)
        self.board_canvas.pack()
        self.board_canvas.bind("<Button-1>", self.on_square_click)
        self.board_canvas.bind("<B1-Motion>", self.drag_piece)
        self.board_canvas.bind("<ButtonRelease-1>", self.drop_piece)
        self.drag_data = {"item": None, "x": 0, "y": 0}

        # Side Panel
        self.side_panel = ctk.CTkFrame(self.main_frame, width=250)
        self.side_panel.pack(side="right", fill="y", padx=10, pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self.side_panel, text="White's Turn", font=ctk.CTkFont(size=20, weight="bold"))
        self.status_label.pack(pady=10)
        
        # Timers
        self.timer_frame = ctk.CTkFrame(self.side_panel)
        self.timer_frame.pack(pady=10, fill="x", padx=10)
        self.white_timer_label = ctk.CTkLabel(self.timer_frame, text="White: 10:00", font=ctk.CTkFont(size=16))
        self.white_timer_label.pack()
        self.black_timer_label = ctk.CTkLabel(self.timer_frame, text="Black: 10:00", font=ctk.CTkFont(size=16))
        self.black_timer_label.pack()

        # Controls Frame
        controls_frame = ctk.CTkFrame(self.side_panel)
        controls_frame.pack(pady=10, fill="x", padx=10)
        
        self.new_game_button = ctk.CTkButton(controls_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(fill="x", pady=5)
        
        self.undo_button = ctk.CTkButton(controls_frame, text="Undo Move", command=self.undo_move_action)
        self.undo_button.pack(fill="x", pady=5)

        self.autoplay_button = ctk.CTkButton(controls_frame, text="Auto Play", command=self.toggle_autoplay)
        self.autoplay_button.pack(fill="x", pady=5)
        
        # AI Difficulty
        difficulty_frame = ctk.CTkFrame(self.side_panel)
        difficulty_frame.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(difficulty_frame, text="Difficulty Level").pack()
        self.difficulty_slider = ctk.CTkSlider(difficulty_frame, from_=1, to=10, number_of_steps=9, command=self.set_difficulty)
        self.difficulty_slider.set(MAX_DEPTH_DEFAULT)
        self.difficulty_slider.pack(fill="x", padx=5)
        self.difficulty_label = ctk.CTkLabel(difficulty_frame, text=f"Level: {MAX_DEPTH_DEFAULT}")
        self.difficulty_label.pack()
        
        # Move History
        history_frame = ctk.CTkFrame(self.side_panel)
        history_frame.pack(pady=10, fill="both", expand=True, padx=10)
        ctk.CTkLabel(history_frame, text="Move History", font=ctk.CTkFont(size=16)).pack()
        self.history_box = ctk.CTkTextbox(history_frame, state="disabled", font=ctk.CTkFont(size=14))
        self.history_box.pack(fill="both", expand=True, pady=5)


    def on_closing(self):
        self.auto_play = False # Stop autoplay thread
        self.destroy()

    def set_difficulty(self, value):
        global MAX_DEPTH_DEFAULT
        MAX_DEPTH_DEFAULT = int(value)
        self.difficulty_label.configure(text=f"Level: {MAX_DEPTH_DEFAULT}")

    def load_images(self):
        for piece, data in IMAGE_DATA.items():
            if not data: continue
            img_data = base64.b64decode(data)
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((self.SQUARE_SIZE, self.SQUARE_SIZE), Image.Resampling.LANCZOS)
            self.images[piece] = ImageTk.PhotoImage(img)

    def draw_game_state(self):
        self.board_canvas.delete("all")
        self.draw_board()
        self.highlight_last_move()
        self.highlight_check()
        self.draw_pieces()

    def draw_board(self):
        colors = ["#DFE1E3", "#646D73"] # Light and dark square colors
        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                self.board_canvas.create_rectangle(c * self.SQUARE_SIZE, r * self.SQUARE_SIZE,
                                                   (c + 1) * self.SQUARE_SIZE, (r + 1) * self.SQUARE_SIZE,
                                                   fill=color, outline="")

    def draw_pieces(self):
        self.board_canvas.delete("pieces")
        for r in range(8):
            for c in range(8):
                piece = self.game_logic.board[r][c]
                if piece != "--" and piece in self.images:
                    self.board_canvas.create_image(c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                                   r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                                   image=self.images[piece], tags=("pieces", f"piece_{r}_{c}"))

    def highlight_squares(self):
        if self.selected_square != ():
            r, c = self.selected_square
            # Highlight selected square
            self.board_canvas.create_rectangle(c * self.SQUARE_SIZE, r * self.SQUARE_SIZE,
                                               (c + 1) * self.SQUARE_SIZE, (r + 1) * self.SQUARE_SIZE,
                                               fill="#F6F669", outline="", tags="highlight")
            # Highlight valid moves
            for move in self.valid_moves:
                if move.start_row == r and move.start_col == c:
                    end_r, end_c = move.end_row, move.end_col
                    if self.game_logic.board[end_r][end_c] == "--":
                        self.board_canvas.create_oval(end_c * self.SQUARE_SIZE + self.SQUARE_SIZE * 0.3,
                                                      end_r * self.SQUARE_SIZE + self.SQUARE_SIZE * 0.3,
                                                      end_c * self.SQUARE_SIZE + self.SQUARE_SIZE * 0.7,
                                                      end_r * self.SQUARE_SIZE + self.SQUARE_SIZE * 0.7,
                                                      fill="#A9A9A9", outline="", tags="highlight")
                    else:
                        self.board_canvas.create_rectangle(end_c * self.SQUARE_SIZE, end_r * self.SQUARE_SIZE,
                                                          (end_c + 1) * self.SQUARE_SIZE, (end_r + 1) * self.SQUARE_SIZE,
                                                          fill="#FF6347", outline="", tags="highlight", stipple="gray50")
            self.board_canvas.tag_raise("pieces")


    def highlight_last_move(self):
        if self.game_logic.move_log:
            last_move = self.game_logic.move_log[-1]
            for r, c in [(last_move.start_row, last_move.start_col), (last_move.end_row, last_move.end_col)]:
                self.board_canvas.create_rectangle(c * self.SQUARE_SIZE, r * self.SQUARE_SIZE,
                                                   (c + 1) * self.SQUARE_SIZE, (r + 1) * self.SQUARE_SIZE,
                                                   fill="#BACA44", outline="", tags="highlight_last")
            self.board_canvas.tag_lower("highlight_last")

    def highlight_check(self):
        if self.game_logic.in_check:
            king_pos = self.game_logic.white_king_location if self.game_logic.white_to_move else self.game_logic.black_king_location
            r, c = king_pos
            self.board_canvas.create_rectangle(c * self.SQUARE_SIZE, r * self.SQUARE_SIZE,
                                               (c + 1) * self.SQUARE_SIZE, (r + 1) * self.SQUARE_SIZE,
                                               fill="#DC143C", outline="", tags="highlight_check")
            self.board_canvas.tag_lower("highlight_check")

    def on_square_click(self, event):
        if not self.game_over and self.human_turn:
            col = event.x // self.SQUARE_SIZE
            row = event.y // self.SQUARE_SIZE
            if self.selected_square == (row, col):
                self.selected_square = ()
                self.player_clicks = []
            else:
                self.selected_square = (row, col)
                self.player_clicks.append(self.selected_square)

            self.draw_game_state()
            if len(self.player_clicks) == 1:
                self.highlight_squares()

            if len(self.player_clicks) == 2:
                move = Move(self.player_clicks[0], self.player_clicks[1], self.game_logic.board)
                for valid_move in self.valid_moves:
                    if move == valid_move:
                        self.process_move(valid_move)
                        break
                
                self.selected_square = ()
                self.player_clicks = []
                self.draw_game_state()

    def process_move(self, move):
        self.animate_move(move, self.post_move_processing)

    def animate_move(self, move, callback):
        self.board_canvas.delete("highlight")
        start_pos = (move.start_col * self.SQUARE_SIZE + self.SQUARE_SIZE//2, move.start_row * self.SQUARE_SIZE + self.SQUARE_SIZE//2)
        end_pos = (move.end_col * self.SQUARE_SIZE + self.SQUARE_SIZE//2, move.end_row * self.SQUARE_SIZE + self.SQUARE_SIZE//2)
        
        piece_image_key = self.game_logic.board[move.start_row][move.start_col]
        
        if piece_image_key == '--' or piece_image_key not in self.images:
             self.after(1, lambda: callback(move))
             return

        # Create a temporary animated piece on a new canvas item
        animated_piece = self.board_canvas.create_image(start_pos[0], start_pos[1], image=self.images[piece_image_key], tags="animated_piece")
        
        # Hide the static piece during animation
        self.board_canvas.itemconfig(f"piece_{move.start_row}_{move.start_col}", state='hidden')
        
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        num_steps = 15
        
        def animation_step(step):
            self.board_canvas.move(animated_piece, dx/num_steps, dy/num_steps)
            if step < num_steps:
                self.after(15, animation_step, step + 1)
            else:
                self.board_canvas.delete(animated_piece)
                callback(move)

        animation_step(1)

    def post_move_processing(self, move):
        self.game_logic.make_move(move)
        self.move_made = True
        self.valid_moves = self.game_logic.get_valid_moves()
        self.draw_game_state()
        self.update_history()
        self.check_game_over()
        if not self.game_over:
            self.human_turn = not self.human_turn
            if not self.human_turn and not self.auto_play:
                self.trigger_ai_move()

    def trigger_ai_move(self):
        self.ai_thinking = True
        self.update_status("AI is thinking...")
        self.undo_button.configure(state="disabled")
        self.new_game_button.configure(state="disabled")

        ai_thread = threading.Thread(target=self.ai_move_worker)
        ai_thread.start()

    def ai_move_worker(self):
        depth = MAX_DEPTH_DEFAULT
        ai_move = ChessAI.find_best_move_minimax(self.game_logic, self.valid_moves, depth)
        
        # Fallback to a simpler search if minimax returns nothing
        if ai_move is None:
            ai_move = ChessAI.find_best_move(self.game_logic, self.valid_moves, 1, human_like=False)

        self.after(0, self.execute_ai_move, ai_move)

    def execute_ai_move(self, ai_move):
        if ai_move:
            self.animate_move(ai_move, self.post_ai_move_processing)
        else: # Handle case where AI has no moves
            self.post_ai_move_processing(None)

    def post_ai_move_processing(self, move):
        if move:
             self.game_logic.make_move(move)
        self.move_made = True
        self.valid_moves = self.game_logic.get_valid_moves()
        self.draw_game_state()
        self.update_history()
        self.check_game_over()
        
        self.ai_thinking = False
        self.undo_button.configure(state="normal")
        self.new_game_button.configure(state="normal")
        
        if not self.game_over:
            self.human_turn = not self.human_turn
            self.update_status()

    def drag_piece(self, event):
        if self.drag_data["item"] is None:
            col = event.x // self.SQUARE_SIZE
            row = event.y // self.SQUARE_SIZE
            item_id = self.board_canvas.find_closest(event.x, event.y)[0]
            if "piece" in self.board_canvas.gettags(item_id):
                self.drag_data["item"] = item_id
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                self.selected_square = (row, col)
                self.player_clicks = [(row, col)]
                self.draw_game_state()
                self.highlight_squares()
        else:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.board_canvas.move(self.drag_data["item"], dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def drop_piece(self, event):
        if self.drag_data["item"] is not None:
            col = event.x // self.SQUARE_SIZE
            row = event.y // self.SQUARE_SIZE
            if 0 <= row < 8 and 0 <= col < 8:
                self.player_clicks.append((row, col))
                if len(self.player_clicks) == 2:
                    move = Move(self.player_clicks[0], self.player_clicks[1], self.game_logic.board)
                    for valid_move in self.valid_moves:
                        if move == valid_move:
                             self.game_logic.make_move(valid_move)
                             self.move_made = True
                             self.valid_moves = self.game_logic.get_valid_moves()
                             self.update_history()
                             self.check_game_over()
                             if not self.game_over:
                                 self.human_turn = not self.human_turn
                                 if not self.human_turn:
                                     self.trigger_ai_move()
                             break

            self.drag_data["item"] = None
            self.selected_square = ()
            self.player_clicks = []
            self.draw_game_state()
    
    def update_status(self, custom_text=None):
        if custom_text:
            self.status_label.configure(text=custom_text)
            return
            
        if self.game_over:
            if self.game_logic.checkmate:
                winner = "Black" if self.game_logic.white_to_move else "White"
                self.status_label.configure(text=f"Checkmate! {winner} wins.")
            elif self.game_logic.stalemate:
                self.status_label.configure(text="Stalemate! It's a draw.")
        else:
            turn = "White's Turn" if self.game_logic.white_to_move else "Black's Turn"
            self.status_label.configure(text=turn)

    def check_game_over(self):
        if self.game_logic.checkmate or self.game_logic.stalemate:
            self.game_over = True
            self.auto_play = False
            self.update_status()

    def update_history(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        
        for i, move in enumerate(self.game_logic.move_log):
            move_number = i // 2 + 1
            if i % 2 == 0:
                self.history_box.insert("end", f"{move_number}. {move} ")
            else:
                self.history_box.insert("end", f"{move}\n")
        self.history_box.see("end")
        self.history_box.configure(state="disabled")

    def new_game(self):
        self.game_logic.new_game()
        self.valid_moves = self.game_logic.get_valid_moves()
        self.selected_square = ()
        self.player_clicks = []
        self.move_made = False
        self.game_over = False
        self.human_turn = True
        self.ai_thinking = False
        self.auto_play = False
        self.draw_game_state()
        self.update_status()
        self.update_history()

    def undo_move_action(self):
        if self.ai_thinking or self.auto_play: return
        self.game_logic.undo_move()
        # If it was AI's turn, undo player's move as well
        if not self.human_turn:
            self.game_logic.undo_move()
        self.move_made = True
        self.game_over = False
        self.valid_moves = self.game_logic.get_valid_moves()
        self.draw_game_state()
        self.update_status()
        self.update_history()

    def toggle_autoplay(self):
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.autoplay_button.configure(text="Stop Auto Play")
            self.autoplay_loop()
        else:
            self.autoplay_button.configure(text="Auto Play")

    def autoplay_loop(self):
        if self.auto_play and not self.game_over:
            self.human_turn = False
            self.trigger_ai_move()
            # The callback from AI move will re-trigger this logic by flipping human_turn
            self.after(2000, self.autoplay_loop) # Loop with a delay


if __name__ == "__main__":
    app = ChessGUI()
    app.mainloop()