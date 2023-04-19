import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sing = 1 if color == 'white' else -1
        self.value = value =value_sing
        self.move = []
        self.move = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'/home/lord/Documents/Proyectos2/python/chess-game/assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        
    def add_moves(self, move):
        self.move.append(move)
    
class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)
        
class Knight(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('knight', color, 3.0)
        
class Bishop(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('bishop', color, 3.001)
        
class Queen(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('queen', color, 9.0)
    
class King(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('king', color, 10000.0)      
    
class Rook(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('rook', color, 5.0)