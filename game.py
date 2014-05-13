from structures import *
from renderer import *


class BaseGame(object):


    def __init__(self, color, board, graphics, heuristic):
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
        self.graphics.hang()


    def complete(self):
        while not self.board.is_complete:
            self.step(lambda: None, False)
        self.graphics.to_image()
        self.graphics.load(self.board)
        self.graphics.refresh()
        self.graphics.hang()


    def step(self, await=None, update=True):
        self.board = self.board.step_forward(self.heuristic, self.color)
        self.color = Color.opposite(self.color)

        if update:
            self.graphics.load(self.board)
            self.graphics.refresh(await)


class Standard(BaseGame):


    def __init__(self, heuristic):
        super().__init__(Color.white, Board(8), Renderer(500, 'grey'), heuristic)




