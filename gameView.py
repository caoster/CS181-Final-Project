from tkinter import Frame, Canvas, Tk, Event, PhotoImage
from typing import Optional
from queue import Queue, Full

from utils import Piece, Player


class Texture:
    def __init__(self, scale: bool):
        self.textures = {
            "NoneType": PhotoImage(file="img/piece_0.png"),
            "BGeneral": PhotoImage(file="img/piece_1.png"),
            "BAdvisor": PhotoImage(file="img/piece_2.png"),
            "BElephant": PhotoImage(file="img/piece_3.png"),
            "BHorse": PhotoImage(file="img/piece_4.png"),
            "BChariot": PhotoImage(file="img/piece_5.png"),
            "BCannon": PhotoImage(file="img/piece_6.png"),
            "BSoldier": PhotoImage(file="img/piece_7.png"),
            "RGeneral": PhotoImage(file="img/piece_8.png"),
            "RAdvisor": PhotoImage(file="img/piece_9.png"),
            "RElephant": PhotoImage(file="img/piece_10.png"),
            "RHorse": PhotoImage(file="img/piece_11.png"),
            "RChariot": PhotoImage(file="img/piece_12.png"),
            "RCannon": PhotoImage(file="img/piece_13.png"),
            "RSoldier": PhotoImage(file="img/piece_14.png")
        }
        if scale:
            for i, j in self.textures.items():
                self.textures[i] = j.zoom(2, 2)

    def __getitem__(self, item: Piece):
        return self.textures[item.name]


class GameView:
    def __init__(self, scale: bool):
        self.root = Tk(className="Chinese Chess")
        self.root.resizable(False, False)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.model = None  # GameModel
        if scale:
            self.root.geometry("1100x1111")
            self.canvas = Canvas(self.frame, bg="black", width=1100, height=1111)
            self.background = PhotoImage(file="img/Board.png")
            self.canvas.create_image(1100 / 2, 1111 / 2, image=self.background, tags="bg")
            self.x_index = (111, 222, 333, 444, 555, 666, 777, 888, 999)
            self.y_index = (66, 176, 286, 396, 506, 616, 726, 836, 946, 1056)
        else:
            self.root.geometry("550x555")
            self.canvas = Canvas(self.frame, bg="black", width=550, height=555)
            self.background = PhotoImage(file="img/Board.png").subsample(2, 2)
            self.canvas.create_image(550 / 2, 555 / 2, image=self.background, tags="bg")
            self.x_index = (55, 111, 166, 222, 277, 333, 388, 444, 499)
            self.y_index = (33, 88, 143, 198, 253, 308, 363, 418, 473, 528)
        self.canvas.bind_all("<Button-1>", self.clickCallbackFunc)
        self.canvas.pack()

        self.texture = Texture(scale)
        for i, x in enumerate(self.x_index):
            for j, y in enumerate(self.y_index):
                self.canvas.create_image(x, y, image=self.texture[Piece.NoneType], tags=f"{i}-{j}")

        # Mouse control
        self.clickData: Optional[tuple[int, int]] = None
        self.red_queue: Optional[Queue] = None
        self.black_queue: Optional[Queue] = None

    def draw(self, grid):
        for i in range(9):
            for j in range(10):
                self.canvas.itemconfigure(self.canvas.find_closest(self.x_index[i], self.y_index[j])[0], image=self.texture[grid[i][j]])
        self.canvas.update()

    def clickCallbackFunc(self, event: Event):
        itemId = self.canvas.find_closest(event.x, event.y)
        if len(itemId) == 0:
            return
        itemTag = self.canvas.gettags(itemId[0])[0].split("-")
        if len(itemTag) == 1:
            return
        x = int(itemTag[0])
        y = int(itemTag[1])
        if self.clickData is None:
            self.clickData = (x, y)
        elif self.clickData == (x, y):
            self.clickData = None
        else:
            try:
                if self.red_queue is not None:
                    self.red_queue.put((self.clickData, (x, y)), block=False)
            except Full:
                pass
            try:
                if self.black_queue is not None:
                    self.black_queue.put((self.clickData, (x, y)), block=False)
            except Full:
                pass
            self.clickData = None

    def enableMouse(self, side: Player, tunnel: Queue):
        if side == Player.NoneType:
            print("Invalid side!")
        elif side == Player.Red:
            self.red_queue = tunnel
        else:
            self.black_queue = tunnel

    def setModel(self, model):
        self.model = model

    def startApp(self):
        self.root.mainloop()
