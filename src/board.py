from square import Square
from const import *
from piece import *
from move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True
        piece.clear_moves()

        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        """
        Calculate all posibles(valid) moves of an specific piece on a specific position
        """

        def pawn_moves():
            step = 1 if piece.moved else 2

            # vertical move
            start = row + piece.dir
            end = row + (piece.dir * (1 + step))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break

            # diagonal move
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_col, possible_move_row):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-2, col-1),
                (row+2, col+1),
                (row+2, col-1),
                (row-1, col+2),
                (row-1, col-2),
                (row+1, col+2),
                (row+1, col-2)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def king_moves():
            # 8 possible moves
            possible_moves = [
                (row-1, col+0),  # up
                (row-1, col-1),  # up-left
                (row-1, col+1),  # up-rigth
                (row-0, col+1),  # rigth
                (row+0, col-1),  # left
                (row+1, col+0),  # down
                (row+1, col+1),  # down-rigth
                (row+1, col-1)  # down-left
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            piece.add_move(move)

                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    else:
                        break

                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # up-rigth
                (-1, -1),  # up-left
                (1, 1),  # down-rigth
                (1, -1)  # down-left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # up
                (1, 0),  # down
                (0, 1),  # rigth
                (0, -1)  # left
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # up-rigth
                (-1, -1),  # up-left
                (1, 1),  # down-rigth
                (1, -1),  # down-left
                (-1, 0),  # up
                (1, 0),  # down
                (0, 1),  # rigth
                (0, -1),  # left
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knghts
        for col in range(COLS):
            self.squares[row_other][1] = Square(row_other, 1, Knight(color))
            self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishop
        for col in range(COLS):
            self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
            self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # queen
        for col in range(COLS):
            self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        for col in range(COLS):
            self.squares[row_other][4] = Square(row_other, 4, King(color))

        # rook
        for col in range(COLS):
            self.squares[row_other][0] = Square(row_other, 0, Rook(color))
            self.squares[row_other][7] = Square(row_other, 7, Rook(color))
