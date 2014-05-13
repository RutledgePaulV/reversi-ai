from structures import *
from renderer import *


class BaseGame(object):


    def __init__(self, color, board, graphics, heuristic1, heuristic2):
        self.start = color
        self.color = color
        self.board = board
        self.graphics = graphics
        self.heuristic1 = heuristic1
        self.heuristic2 = heuristic2


    def step_through(self):
        self.graphics.load(self.board)
        self.graphics.refresh()
        while not self.board.is_complete:
            self.step()


    def animate(self, time_step):
        while not self.board.is_complete:
            self.step(lambda: time.sleep(time_step))
        self.graphics.hang()


    def complete(self):
        while not self.board.is_complete:
            self.step(lambda: None, False)
        self.graphics.to_image()
        self.graphics.load(self.board)
        self.graphics.refresh()
        self.graphics.hang()


    def step(self, await=None, update=True):

        if self.color is self.start:
            self.board = self.board.step_forward(self.heuristic1, self.color)
        else:
            self.board = self.board.step_forward(self.heuristic2, self.color)

        self.color = Color.opposite(self.color)

        if update:
            self.graphics.load(self.board)
            self.graphics.refresh(await)


class Standard(BaseGame):


    def __init__(self, heuristic1, heuristic2):
        super().__init__(Color.black, Board(8), Renderer(500, 'grey'), heuristic1, heuristic2)




