import pygame
import pygame.locals
import logging


class Board(object):


    def __init__(self, width):

        self.surface = pygame.display.set_mode((width, width), 0, 32)
        pygame.display.set_caption('Kółko i Krzyżyk')

        
        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 48)

        
        self.markers = [None] * 9

    def draw(self, *args):

        background = (16, 52, 166)
        self.surface.fill(background)
        self.draw_net()
        self.draw_markers()
        self.draw_score()
        for drawable in args:
            drawable.draw_on(self.surface)


        pygame.display.update()

    def draw_net(self):

        color = (0, 0, 0)
        width = self.surface.get_width()
        for i in range(1, 3):
            pos = width / 3 * i
            
            pygame.draw.line(self.surface, color, (0, pos), (width, pos), 1)
            
            pygame.draw.line(self.surface, color, (pos, 0), (pos, width), 1)

    def player_move(self, x, y):

        cell_size = self.surface.get_width() / 3
        x /= cell_size
        y /= cell_size
        self.markers[int(x) + int(y) * 3] = player_marker(True)

    def draw_markers(self):
  
        box_side = self.surface.get_width() / 3
        for x in range(3):
            for y in range(3):
                marker = self.markers[x + y * 3]
                if not marker:
                    continue
                
                center_x = x * box_side + box_side / 2
                center_y = y * box_side + box_side / 2

                self.draw_text(self.surface, marker, (center_x, center_y))

    def draw_text(self, surface,  text, center, color=(0, 0, 0)):

        text = self.font.render(text, True, color)
        rect = text.get_rect()
        rect.center = center
        surface.blit(text, rect)

    def draw_score(self):
 
        if check_win(self.markers, True):
            score = f"Wygrałeś"
        elif check_win(self.markers, True):
            score = f"Przegrałeś"
        elif None not in self.markers:
            score = f"Remis!"
        else:
            return

        i = self.surface.get_width() / 2
        self.draw_text(self.surface, score, center=(i, i), color=(255, 26, 26))


class TicTacToeGame(object):


    def __init__(self, width, ai_turn=False):

        pygame.init()
      
        self.fps_clock = pygame.time.Clock()

        self.board = Board(width)
        self.ai = Ai(self.board)
        self.ai_turn = ai_turn

    def run(self):

        while not self.handle_events():
            # działaj w pętli do momentu otrzymania sygnału do wyjścia
            self.board.draw()
            if self.ai_turn:
                self.ai.make_turn()
                self.ai_turn = False
            self.fps_clock.tick(15)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True

            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                if self.ai_turn:
                    
                    continue
                
                x, y = pygame.mouse.get_pos()
                self.board.player_move(x, y)
                self.ai_turn = True


class Ai(object):

    def __init__(self, board):
        self.board = board

    def make_turn(self):
 
        if not None in self.board.markers:
            
            return
        logging.debug("Plansza: %s" % self.board.markers)
        move = self.next_move(self.board.markers)
        self.board.markers[move] = player_marker(False)

    @classmethod
    def next_move(cls, markers):
 
        # pobierz dostępne ruchy wraz z oceną
        moves = cls.score_moves(markers, False)
        # wybierz najlepiej oceniony ruch
        score, move = max(moves, key=lambda m: m[0])
        logging.info("Dostępne ruchy: %s", moves)
        logging.info("Wybrany ruch: %s %s", move, score)
        return move

    @classmethod
    def score_moves(cls, markers, x_player):

        
        available_moves = (i for i, m in enumerate(markers) if m is None)
        for move in available_moves:
            from copy import copy
           
            proposal = copy(markers)
            proposal[move] = player_marker(x_player)

            
            if check_win(proposal, x_player):
                
                score = -1 if x_player else 1
                yield score, move
                continue

            
            next_moves = list(cls.score_moves(proposal, not x_player))
            if not next_moves:
                yield 0, move
                continue

            
            scores, moves = zip(*next_moves)
            
            yield sum(scores), move


def player_marker(x_player):

    return "X" if x_player else "O"


def check_win(markers, x_player):

    win = [player_marker(x_player)] * 3
    seq = range(3)

    
    def marker(xx, yy):
        return markers[xx + yy * 3]

    
    for x in seq:
        row = [marker(x, y) for y in seq]
        if row == win:
            return True

    
    for y in seq:
        col = [marker(x, y) for x in seq]
        if col == win:
            return True

    
    diagonal1 = [marker(i, i) for i in seq]
    diagonal2 = [marker(i, abs(i-2)) for i in seq]
    if diagonal1 == win or diagonal2 == win:
        return True



if __name__ == "__main__":
    game = TicTacToeGame(300)
    game.run()
