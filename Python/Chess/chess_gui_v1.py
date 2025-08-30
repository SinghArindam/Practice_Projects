import customtkinter as ctk
from PIL import Image, ImageTk
import base64
import io
import math
import random
import time
import threading
import os
import json
import requests

# --- Asset and Cache Configuration ---
ASSETS_DIR = "assets"
CACHE_FILE = os.path.join(ASSETS_DIR, "image_data.json")

def load_or_create_image_data():
    """
    Loads Base64 image data from a JSON cache if it exists.
    If not, it downloads images, processes them, saves them locally,
    and creates the JSON cache for future use.
    """
    if os.path.exists(CACHE_FILE):
        print(f"Loading cached image data from {CACHE_FILE}...")
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read cache file. Re-generating... Error: {e}")

    print("Image cache not found. Generating new image data...")
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

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

        if not os.path.exists(local_path):
            try:
                print(f"Downloading {image_filename}...")
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(response.content)
            except requests.exceptions.RequestException as e:
                print(f"Fatal: Could not download {name}. Please check your internet connection. Error: {e}")
                generated_image_data[name] = ""
                continue
        
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

    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(generated_image_data, f)
        print(f"Image data cache created at {CACHE_FILE}")
    except IOError as e:
        print(f"Warning: Could not save cache file. Error: {e}")

    return generated_image_data

# --- Load Image Data ---
IMAGE_DATA = load_or_create_image_data()

# --- AI and Game Logic Constants ---
PIECE_VALUES = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}
CHECKMATE_SCORE = 100000
STALEMATE_SCORE = 0
MAX_DEPTH_DEFAULT = 3

PST = {
    'P': [[0,0,0,0,0,0,0,0], [50,50,50,50,50,50,50,50], [10,10,20,30,30,20,10,10], [5,5,10,25,25,10,5,5], [0,0,0,20,20,0,0,0], [5,-5,-10,0,0,-10,-5,5], [5,10,10,-20,-20,10,10,5], [0,0,0,0,0,0,0,0]],
    'N': [[-50,-40,-30,-30,-30,-30,-40,-50], [-40,-20,0,0,0,0,-20,-40], [-30,0,10,15,15,10,0,-30], [-30,5,15,20,20,15,5,-30], [-30,0,15,20,20,15,0,-30], [-30,5,10,15,15,10,5,-30], [-40,-20,0,5,5,0,-20,-40], [-50,-40,-30,-30,-30,-30,-40,-50]],
    'B': [[-20,-10,-10,-10,-10,-10,-10,-20], [-10,0,0,0,0,0,0,-10], [-10,0,5,10,10,5,0,-10], [-10,5,5,10,10,5,5,-10], [-10,0,10,10,10,10,0,-10], [-10,10,10,10,10,10,10,-10], [-10,5,0,0,0,0,5,-10], [-20,-10,-10,-10,-10,-10,-10,-20]],
    'R': [[0,0,0,0,0,0,0,0], [5,10,10,10,10,10,10,5], [-5,0,0,0,0,0,0,-5], [-5,0,0,0,0,0,0,-5], [-5,0,0,0,0,0,0,-5], [-5,0,0,0,0,0,0,-5], [-5,0,0,0,0,0,0,-5], [0,0,0,5,5,0,0,0]],
    'Q': [[-20,-10,-10,-5,-5,-10,-10,-20], [-10,0,0,0,0,0,0,-10], [-10,0,5,5,5,5,0,-10], [-5,0,5,5,5,5,0,-5], [0,0,5,5,5,5,0,-5], [-10,5,5,5,5,5,0,-10], [-10,0,5,0,0,0,0,-10], [-20,-10,-10,-5,-5,-10,-10,-20]],
    'K': [[-30,-40,-40,-50,-50,-40,-40,-30], [-30,-40,-40,-50,-50,-40,-40,-30], [-30,-40,-40,-50,-50,-40,-40,-30], [-30,-40,-40,-50,-50,-40,-40,-30], [-20,-30,-30,-40,-40,-30,-30,-20], [-10,-20,-20,-20,-20,-20,-20,-10], [20,20,0,0,0,0,20,20], [20,30,10,0,0,10,30,20]]
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
        pins, checks, in_check = [], [], False
        ally_color, enemy_color = ("w", "b") if self.white_to_move else ("b", "w")
        start_row, start_col = self.white_king_location if self.white_to_move else self.black_king_location
        directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j, d in enumerate(directions):
            possible_pin = ()
            for i in range(1, 8):
                end_row, end_col = start_row + d[0] * i, start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != 'K':
                        if not possible_pin: possible_pin = (end_row,end_col,d[0],d[1])
                        else: break
                    elif end_piece[0] == enemy_color:
                        piece_type = end_piece[1]
                        is_orthogonal = 0<=j<=3
                        is_diagonal = 4<=j<=7
                        is_pawn = i==1 and piece_type=='P' and ((enemy_color=='w' and 6<=j<=7) or (enemy_color=='b' and 4<=j<=5))
                        if (is_orthogonal and piece_type=='R') or (is_diagonal and piece_type=='B') or \
                            (i==1 and piece_type=='K') or (piece_type=='Q') or is_pawn:
                            if not possible_pin:
                                in_check=True
                                checks.append((end_row,end_col,d[0],d[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else: break
                else: break
        knight_moves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knight_moves:
            end_row, end_col = start_row+m[0], start_col+m[1]
            if 0<=end_row<8 and 0<=end_col<8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0]==enemy_color and end_piece[1]=='N':
                    in_check=True
                    checks.append((end_row,end_col,m[0],m[1]))
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
        piece_pinned = any(pin[0] == r and pin[1] == c for pin in self.pins)
        pin_direction = next((pin[2], pin[3]) for pin in self.pins if pin[0] == r and pin[1] == c) if piece_pinned else ()
        move_amount = -1 if self.white_to_move else 1
        start_row = 6 if self.white_to_move else 1
        enemy_color = 'b' if self.white_to_move else 'w'

        if self.board[r + move_amount][c] == "--":
            if not piece_pinned or pin_direction in [(move_amount, 0), (-move_amount, 0)]:
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + 2 * move_amount][c] == "--":
                    moves.append(Move((r, c), (r + 2 * move_amount, c), self.board))

        if c-1 >= 0:
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r+move_amount][c-1][0] == enemy_color:
                    moves.append(Move((r,c), (r+move_amount, c-1), self.board))
                elif (r+move_amount,c-1) == self.enpassant_possible:
                    moves.append(Move((r, c), (r + move_amount, c-1), self.board, is_enpassant_move=True))
        if c+1 <= 7:
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[r+move_amount][c+1][0] == enemy_color:
                    moves.append(Move((r,c), (r+move_amount, c+1), self.board))
                elif (r+move_amount, c+1) == self.enpassant_possible:
                    moves.append(Move((r,c), (r+move_amount, c+1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, r, c, moves):
        self.get_straight_moves(r, c, moves, ((-1, 0), (0, -1), (1, 0), (0, 1)))

    def get_knight_moves(self, r, c, moves):
        piece_pinned = any(pin[0] == r and pin[1] == c for pin in self.pins)
        if piece_pinned: return
        knight_moves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        ally_color = 'w' if self.white_to_move else 'b'
        for m in knight_moves:
            end_row, end_col = r+m[0], c+m[1]
            if 0<=end_row<8 and 0<=end_col<8 and self.board[end_row][end_col][0] != ally_color:
                moves.append(Move((r,c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        self.get_straight_moves(r, c, moves, ((-1, -1), (-1, 1), (1, -1), (1, 1)))

    def get_queen_moves(self, r, c, moves):
        self.get_straight_moves(r, c, moves, ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)))

    def get_king_moves(self, r, c, moves):
        row_moves, col_moves = (-1,-1,-1,0,0,1,1,1), (-1,0,1,-1,1,-1,0,1)
        ally_color = 'w' if self.white_to_move else 'b'
        for i in range(8):
            end_row, end_col = r+row_moves[i], c+col_moves[i]
            if 0<=end_row<8 and 0<=end_col<8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    king_loc_backup = self.white_king_location if self.white_to_move else self.black_king_location
                    if self.white_to_move: self.white_king_location = (end_row,end_col)
                    else: self.black_king_location = (end_row,end_col)
                    in_check, _, _ = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r,c), (end_row,end_col), self.board))
                    if self.white_to_move: self.white_king_location = king_loc_backup
                    else: self.black_king_location = king_loc_backup

    def get_straight_moves(self, r, c, moves, directions):
        piece_pinned = any(pin[0] == r and pin[1] == c for pin in self.pins)
        pin_direction = next((pin[2], pin[3]) for pin in self.pins if pin[0] == r and pin[1] == c) if piece_pinned else ()
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for i in range(1, 8):
                end_row, end_col = r + d[0] * i, c + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    if not piece_pinned or pin_direction==d or pin_direction==(-d[0],-d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == "--":
                            moves.append(Move((r,c), (end_row,end_col), self.board))
                        elif end_piece[0] == enemy_color:
                            moves.append(Move((r,c), (end_row,end_col), self.board))
                            break
                        else: break
                else: break

    def get_castle_moves(self, r, c, moves):
        if self.in_check: return
        if (self.white_to_move and self.current_castling_rights['wks']) or \
           (not self.white_to_move and self.current_castling_rights['bks']):
            if self.board[r][c+1]=='--' and self.board[r][c+2]=='--' and \
               not self.is_square_attacked(r,c+1) and not self.is_square_attacked(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,is_castle_move=True))
        if (self.white_to_move and self.current_castling_rights['wqs']) or \
           (not self.white_to_move and self.current_castling_rights['bqs']):
            if self.board[r][c-1]=='--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--' and \
               not self.is_square_attacked(r,c-1) and not self.is_square_attacked(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,is_castle_move=True))

class Move:
    ranks_to_rows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant_move=False, is_castle_move=False):
        self.start_row, self.start_col = start_sq
        self.end_row, self.end_col = end_sq
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.is_pawn_promotion = (self.piece_moved=='wP' and self.end_row==0) or (self.piece_moved=='bP' and self.end_row==7)
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = 'wP' if self.piece_moved == 'bP' else 'bP'
        self.is_castle_move = is_castle_move
        self.is_capture = self.piece_captured != "--"
        self.move_id = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col

    def __eq__(self, other):
        return isinstance(other, Move) and self.move_id == other.move_id

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]
        
    def __str__(self):
        if self.is_castle_move: return "O-O" if self.end_col == 6 else "O-O-O"
        end_square = self.get_rank_file(self.end_row, self.end_col)
        if self.piece_moved[1] == 'P':
            if self.is_capture: return self.cols_to_files[self.start_col] + "x" + end_square
            else: return end_square
        return self.piece_moved[1] + ("x" if self.is_capture else "") + end_square

class ChessAI:
    @staticmethod
    def find_best_move_minimax(game_state, valid_moves, depth):
        if not valid_moves: return None
        global next_move
        next_move = None
        random.shuffle(valid_moves)
        ChessAI.minimax_alpha_beta(game_state, valid_moves, depth, -CHECKMATE_SCORE, CHECKMATE_SCORE, 1 if game_state.white_to_move else -1)
        return next_move

    @staticmethod
    def minimax_alpha_beta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
        global next_move
        if depth == 0:
            return turn_multiplier * ChessAI.score_board(game_state)

        max_score = -CHECKMATE_SCORE
        for move in valid_moves:
            game_state.make_move(move)
            next_moves = game_state.get_valid_moves()
            if game_state.checkmate:
                score = -CHECKMATE_SCORE
            elif game_state.stalemate:
                score = STALEMATE_SCORE
            else:
                score = -ChessAI.minimax_alpha_beta(game_state, next_moves, depth-1, -beta, -alpha, -turn_multiplier)
            
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
    def score_board(game_state):
        if game_state.checkmate: return -CHECKMATE_SCORE if game_state.white_to_move else CHECKMATE_SCORE
        if game_state.stalemate: return STALEMATE_SCORE
        
        score = 0
        for r in range(8):
            for c in range(8):
                square = game_state.board[r][c]
                if square != '--':
                    piece_pos_score = 0
                    if square[1] in PST:
                        piece_pos_score = PST[square[1]][r][c] if square[0]=='w' else PST[square[1]][7-r][c]
                    if square[0] == 'w': score += PIECE_VALUES[square[1]] + piece_pos_score
                    else: score -= PIECE_VALUES[square[1]] + piece_pos_score
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
        self.board_frame = ctk.CTkFrame(self.main_frame, width=self.BOARD_WIDTH, height=self.BOARD_HEIGHT)
        self.board_frame.pack(side="left", padx=10, pady=10)
        self.board_canvas = ctk.CTkCanvas(self.board_frame, width=self.BOARD_WIDTH, height=self.BOARD_HEIGHT, highlightthickness=0)
        self.board_canvas.pack()
        self.board_canvas.bind("<Button-1>", self.on_square_click)

        self.side_panel = ctk.CTkFrame(self.main_frame, width=250)
        self.side_panel.pack(side="right", fill="y", padx=10, pady=10)
        self.status_label = ctk.CTkLabel(self.side_panel, text="White's Turn", font=ctk.CTkFont(size=20, weight="bold"))
        self.status_label.pack(pady=10)
        
        controls_frame = ctk.CTkFrame(self.side_panel)
        controls_frame.pack(pady=10, fill="x", padx=10)
        self.new_game_button = ctk.CTkButton(controls_frame, text="New Game", command=self.new_game)
        self.new_game_button.pack(fill="x", pady=5)
        self.undo_button = ctk.CTkButton(controls_frame, text="Undo Move", command=self.undo_move_action)
        self.undo_button.pack(fill="x", pady=5)
        self.autoplay_button = ctk.CTkButton(controls_frame, text="Auto Play", command=self.toggle_autoplay)
        self.autoplay_button.pack(fill="x", pady=5)
        
        difficulty_frame = ctk.CTkFrame(self.side_panel)
        difficulty_frame.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(difficulty_frame, text="Difficulty Level").pack()
        self.difficulty_slider = ctk.CTkSlider(difficulty_frame, from_=1, to=10, number_of_steps=9, command=self.set_difficulty)
        self.difficulty_slider.set(MAX_DEPTH_DEFAULT)
        self.difficulty_slider.pack(fill="x", padx=5)
        self.difficulty_label = ctk.CTkLabel(difficulty_frame, text=f"Level: {MAX_DEPTH_DEFAULT}")
        self.difficulty_label.pack()
        
        history_frame = ctk.CTkFrame(self.side_panel)
        history_frame.pack(pady=10, fill="both", expand=True, padx=10)
        ctk.CTkLabel(history_frame, text="Move History", font=ctk.CTkFont(size=16)).pack()
        self.history_box = ctk.CTkTextbox(history_frame, state="disabled", font=ctk.CTkFont(size=14))
        self.history_box.pack(fill="both", expand=True, pady=5)

    def on_closing(self):
        self.auto_play = False
        self.destroy()

    def set_difficulty(self, value):
        global MAX_DEPTH_DEFAULT
        MAX_DEPTH_DEFAULT = int(value)
        self.difficulty_label.configure(text=f"Level: {MAX_DEPTH_DEFAULT}")

    def load_images(self):
        for piece, data in IMAGE_DATA.items():
            if not data:
                print(f"Warning: No image data for {piece}. It will not be displayed.")
                continue
            try:
                img_data = base64.b64decode(data)
                img = Image.open(io.BytesIO(img_data))
                img = img.resize((self.SQUARE_SIZE, self.SQUARE_SIZE), Image.Resampling.LANCZOS)
                self.images[piece] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image for {piece}: {e}")

    def draw_game_state(self):
        self.board_canvas.delete("all")
        self.draw_board()
        self.highlight_last_move()
        self.highlight_check()
        self.draw_pieces()

    def draw_board(self):
        colors = ["#DFE1E3", "#646D73"]
        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                self.board_canvas.create_rectangle(c*self.SQUARE_SIZE,r*self.SQUARE_SIZE,(c+1)*self.SQUARE_SIZE,(r+1)*self.SQUARE_SIZE,fill=color,outline="")

    def draw_pieces(self):
        self.board_canvas.delete("pieces")
        for r in range(8):
            for c in range(8):
                piece = self.game_logic.board[r][c]
                if piece != "--":
                    if piece in self.images:
                        self.board_canvas.create_image(c*self.SQUARE_SIZE+self.SQUARE_SIZE//2, r*self.SQUARE_SIZE+self.SQUARE_SIZE//2, image=self.images[piece], tags=("pieces",))
                    else:
                        # Placeholder for missing images
                        x_center = c * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                        y_center = r * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                        fill_color = "black" if piece[0] == 'b' else "white"
                        text_color = "white" if piece[0] == 'b' else "black"
                        self.board_canvas.create_rectangle(
                            c * self.SQUARE_SIZE, r * self.SQUARE_SIZE,
                            (c + 1) * self.SQUARE_SIZE, (r + 1) * self.SQUARE_SIZE,
                            fill=fill_color, outline="gray", tags="pieces"
                        )
                        self.board_canvas.create_text(
                            x_center, y_center, text=piece[1],
                            font=("Helvetica", 30, "bold"), fill=text_color, tags="pieces"
                        )


    def highlight_squares(self):
        if self.selected_square:
            r, c = self.selected_square
            self.board_canvas.create_rectangle(c*self.SQUARE_SIZE, r*self.SQUARE_SIZE, (c+1)*self.SQUARE_SIZE, (r+1)*self.SQUARE_SIZE, fill="#F6F669", outline="", tags="highlight")
            for move in self.valid_moves:
                if move.start_row == r and move.start_col == c:
                    end_r, end_c = move.end_row, move.end_col
                    if self.game_logic.board[end_r][end_c] == "--":
                        self.board_canvas.create_oval(end_c*self.SQUARE_SIZE+25, end_r*self.SQUARE_SIZE+25, end_c*self.SQUARE_SIZE+55, end_r*self.SQUARE_SIZE+55, fill="#A9A9A9", outline="", tags="highlight")
                    else:
                        self.board_canvas.create_rectangle(end_c*self.SQUARE_SIZE,end_r*self.SQUARE_SIZE,(end_c+1)*self.SQUARE_SIZE,(end_r+1)*self.SQUARE_SIZE,fill="#FF6347",outline="",tags="highlight",stipple="gray50")
            self.board_canvas.tag_raise("pieces")

    def highlight_last_move(self):
        if self.game_logic.move_log:
            last_move = self.game_logic.move_log[-1]
            for r, c in [(last_move.start_row, last_move.start_col), (last_move.end_row, last_move.end_col)]:
                self.board_canvas.create_rectangle(c*self.SQUARE_SIZE,r*self.SQUARE_SIZE,(c+1)*self.SQUARE_SIZE,(r+1)*self.SQUARE_SIZE,fill="#BACA44",outline="",tags="highlight_last")
            self.board_canvas.tag_lower("highlight_last")

    def highlight_check(self):
        if self.game_logic.in_check:
            king_pos = self.game_logic.white_king_location if self.game_logic.white_to_move else self.game_logic.black_king_location
            r, c = king_pos
            self.board_canvas.create_rectangle(c*self.SQUARE_SIZE,r*self.SQUARE_SIZE,(c+1)*self.SQUARE_SIZE,(r+1)*self.SQUARE_SIZE,fill="#DC143C",outline="",tags="highlight_check")
            self.board_canvas.tag_lower("highlight_check")

    def on_square_click(self, event):
        if not self.game_over and self.human_turn:
            col, row = event.x // self.SQUARE_SIZE, event.y // self.SQUARE_SIZE
            if self.selected_square == (row, col):
                self.selected_square, self.player_clicks = (), []
            else:
                self.selected_square = (row, col)
                self.player_clicks.append(self.selected_square)
            
            if len(self.player_clicks) == 2:
                move = Move(self.player_clicks[0], self.player_clicks[1], self.game_logic.board)
                for valid_move in self.valid_moves:
                    if move == valid_move:
                        self.process_move(valid_move)
                        break
                self.selected_square, self.player_clicks = (), []
            self.draw_game_state()
            if self.player_clicks: self.highlight_squares()

    def process_move(self, move):
        self.animate_move(move, self.post_move_processing)

    def animate_move(self, move, callback):
        start_pos = (move.start_col*self.SQUARE_SIZE, move.start_row*self.SQUARE_SIZE)
        end_pos = (move.end_col*self.SQUARE_SIZE, move.end_row*self.SQUARE_SIZE)
        piece_image_key = self.game_logic.board[move.start_row][move.start_col]
        
        if piece_image_key not in self.images:
            callback(move)
            return

        animated_piece = self.board_canvas.create_image(start_pos[0]+self.SQUARE_SIZE//2, start_pos[1]+self.SQUARE_SIZE//2, image=self.images[piece_image_key], tags="animated")
        self.draw_game_state()
        self.board_canvas.tag_raise(animated_piece)

        dx, dy = end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]
        num_steps = 15
        
        def animation_step(step):
            self.board_canvas.move(animated_piece, dx/num_steps, dy/num_steps)
            if step < num_steps: self.after(15, animation_step, step+1)
            else:
                self.board_canvas.delete(animated_piece)
                callback(move)
        animation_step(1)

    def post_move_processing(self, move):
        self.game_logic.make_move(move)
        self.move_made = True
        self.valid_moves = self.game_logic.get_valid_moves()
        self.check_game_over()
        self.update_history()
        self.draw_game_state()
        if not self.game_over:
            self.human_turn = not self.human_turn
            if not self.human_turn and not self.auto_play: self.trigger_ai_move()
            else: self.update_status()

    def trigger_ai_move(self):
        if self.ai_thinking: return
        self.ai_thinking = True
        self.update_status("AI is thinking...")
        self.undo_button.configure(state="disabled")
        self.new_game_button.configure(state="disabled")
        ai_thread = threading.Thread(target=self.ai_move_worker, daemon=True)
        ai_thread.start()

    def ai_move_worker(self):
        depth = MAX_DEPTH_DEFAULT
        ai_move = ChessAI.find_best_move_minimax(self.game_logic, self.valid_moves, depth)
        time.sleep(random.uniform(0.4, 0.8))
        self.after(0, self.execute_ai_move, ai_move)

    def execute_ai_move(self, ai_move):
        self.ai_thinking = False
        self.undo_button.configure(state="normal")
        self.new_game_button.configure(state="normal")
        if ai_move:
            self.animate_move(ai_move, self.post_ai_move_processing)
        else:
            self.post_ai_move_processing(None)

    def post_ai_move_processing(self, move):
        if move: self.game_logic.make_move(move)
        self.move_made = True
        self.valid_moves = self.game_logic.get_valid_moves()
        self.check_game_over()
        self.update_history()
        self.draw_game_state()
        if not self.game_over:
            self.human_turn = not self.human_turn
            self.update_status()

    def update_status(self, custom_text=None):
        if custom_text:
            self.status_label.configure(text=custom_text)
            return
        if self.game_over:
            winner = "Black" if self.game_logic.white_to_move else "White"
            self.status_label.configure(text=f"Checkmate! {winner} wins." if self.game_logic.checkmate else "Stalemate!")
        else:
            self.status_label.configure(text="White's Turn" if self.game_logic.white_to_move else "Black's Turn")

    def check_game_over(self):
        if self.game_logic.checkmate or self.game_logic.stalemate:
            self.game_over = True
            self.auto_play = False
            self.autoplay_button.configure(text="Auto Play")
            self.update_status()

    def update_history(self):
        self.history_box.configure(state="normal")
        self.history_box.delete("1.0", "end")
        for i, move in enumerate(self.game_logic.move_log):
            move_number = i//2+1
            self.history_box.insert("end", f"{move_number}. {move} " if i%2==0 else f"{move}\n")
        self.history_box.see("end")
        self.history_box.configure(state="disabled")

    def new_game(self):
        self.game_logic.new_game()
        self.valid_moves, self.selected_square, self.player_clicks = self.game_logic.get_valid_moves(), (), []
        self.move_made, self.game_over, self.human_turn, self.ai_thinking, self.auto_play = False, False, True, False, False
        self.draw_game_state()
        self.update_status()
        self.update_history()

    def undo_move_action(self):
        if self.ai_thinking or self.auto_play: return
        self.game_logic.undo_move()
        if not self.human_turn and self.game_logic.move_log: self.game_logic.undo_move()
        self.move_made, self.game_over, self.human_turn = True, False, True
        self.valid_moves = self.game_logic.get_valid_moves()
        self.draw_game_state()
        self.update_status()
        self.update_history()

    def toggle_autoplay(self):
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.autoplay_button.configure(text="Stop Auto Play")
            self.human_turn = False
            self.autoplay_loop()
        else:
            self.autoplay_button.configure(text="Auto Play")

    def autoplay_loop(self):
        if self.auto_play and not self.game_over:
            if self.game_logic.white_to_move == self.human_turn: return
            self.trigger_ai_move()
            self.after(2000, self.autoplay_loop)

if __name__ == "__main__":
    next_move = None
    app = ChessGUI()
    app.mainloop()