from tkinter import Frame, Canvas, Tk, Event, PhotoImage

from utils import Piece


class Texture:
    def __init__(self, scale: bool):
        self.textures = {
            "NoneType": PhotoImage(file="imgs/piece_0.png"),
            "BGeneral": PhotoImage(file="imgs/piece_1.png"),
            "BAdvisor": PhotoImage(file="imgs/piece_2.png"),
            "BElephant": PhotoImage(file="imgs/piece_3.png"),
            "BHorse": PhotoImage(file="imgs/piece_4.png"),
            "BChariot": PhotoImage(file="imgs/piece_5.png"),
            "BCannon": PhotoImage(file="imgs/piece_6.png"),
            "BSoldier": PhotoImage(file="imgs/piece_7.png"),
            "RGeneral": PhotoImage(file="imgs/piece_8.png"),
            "RAdvisor": PhotoImage(file="imgs/piece_9.png"),
            "RElephant": PhotoImage(file="imgs/piece_10.png"),
            "RHorse": PhotoImage(file="imgs/piece_11.png"),
            "RChariot": PhotoImage(file="imgs/piece_12.png"),
            "RCannon": PhotoImage(file="imgs/piece_13.png"),
            "RSoldier": PhotoImage(file="imgs/piece_14.png")
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
            self.background = PhotoImage(file="imgs/Board.png")
            self.canvas.create_image(1100 / 2, 1111 / 2, image=self.background)
            self.x_index = (111, 222, 333, 444, 555, 666, 777, 888, 999)
            self.y_index = (66, 176, 286, 396, 506, 616, 726, 836, 946, 1056)
        else:
            self.root.geometry("550x555")
            self.canvas = Canvas(self.frame, bg="black", width=550, height=555)
            self.background = PhotoImage(file="imgs/Board.png").subsample(2, 2)
            self.canvas.create_image(550 / 2, 555 / 2, image=self.background)
            self.x_index = (55, 111, 166, 222, 277, 333, 388, 444, 499)
            self.y_index = (33, 88, 143, 198, 253, 308, 363, 418, 473, 528)
        self.canvas.bind_all("<Button-1>", self.clickCallbackFunc)
        self.canvas.pack()

        self.texture = Texture(scale)
        for i in self.x_index:
            for j in self.y_index:
                self.canvas.create_image(i, j, image=self.texture[Piece.NoneType])

    def draw(self, grid):
        for i in range(9):
            for j in range(10):
                self.canvas.itemconfigure(self.canvas.find_closest(self.x_index[i], self.y_index[j])[0], image=self.texture[grid[i][j]])
        self.canvas.update()

    def clickCallbackFunc(self, event: Event):
        pass

    def setModel(self, model):
        self.model = model

    def startApp(self):
        self.root.mainloop()
