from structures import *
from renderer import *


class BaseGame(object):


    def __init__(self, dimension, color, board, graphics, heuristic):
        self.dimension = dimension
        self.color = color
        self.board = board
        self.graphics = graphics
        self.heuristic = heuristic


    def step_through(self):
        self.graphics.load(self.board)
        self.graphics.refresh()
        while not self.board.is_complete:
            self.step()


    def animate(self, time_step):
        while not self.board.is_complete:
            self.step(lambda: time.sleep(time_step))


    def complete(self):
        while not self.board.is_complete:
            self.step(lambda: time.sleep(0))


    def step(self, await=None):
        self.board = self.board.step_forward(self.heuristic, self.color)
        self.color = Color.opposite(self.color)
        self.graphics.load(self.board)
        self.graphics.refresh(await)


class Standard(BaseGame):


    def __init__(self, heuristic):
        super().__init__(8, Color.white, Board(16), Renderer(500, 'grey'), heuristic)




