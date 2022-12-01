from tkinter import Frame, Canvas, Tk, Event, PhotoImage
from utils import Piece


class Texture:
    def __init__(self):
        self.textures = {
            "NoneType": PhotoImage(file="imgs/piece_0.png").zoom(2, 2),
            "BGeneral": PhotoImage(file="imgs/piece_1.png").zoom(2, 2),
            "BAdvisor": PhotoImage(file="imgs/piece_2.png").zoom(2, 2),
            "BElephant": PhotoImage(file="imgs/piece_3.png").zoom(2, 2),
            "BHorse": PhotoImage(file="imgs/piece_4.png").zoom(2, 2),
            "BChariot": PhotoImage(file="imgs/piece_5.png").zoom(2, 2),
            "BCannon": PhotoImage(file="imgs/piece_6.png").zoom(2, 2),
            "BSoldier": PhotoImage(file="imgs/piece_7.png").zoom(2, 2),
            "RGeneral": PhotoImage(file="imgs/piece_8.png").zoom(2, 2),
            "RAdvisor": PhotoImage(file="imgs/piece_9.png").zoom(2, 2),
            "RElephant": PhotoImage(file="imgs/piece_10.png").zoom(2, 2),
            "RHorse": PhotoImage(file="imgs/piece_11.png").zoom(2, 2),
            "RChariot": PhotoImage(file="imgs/piece_12.png").zoom(2, 2),
            "RCannon": PhotoImage(file="imgs/piece_13.png").zoom(2, 2),
            "RSoldier": PhotoImage(file="imgs/piece_14.png").zoom(2, 2)
        }

    def __getitem__(self, item: Piece):
        return self.textures[item.name]


class GameView:
    def __init__(self):
        self.root = Tk(className="Chinese Chess")
        self.root.geometry("1100x1111")
        self.frame = Frame(self.root)
        self.frame.pack()
        self.texture = Texture()
        self.canvas = Canvas(self.frame, bg="black", width=1100, height=1111)
        self.canvas.pack()
        self.background = PhotoImage(file="imgs/Board.png")
        self.canvas.create_image(1100 / 2, 1111 / 2, image=self.background)
        self.model = None  # GameModel

        self.canvas.bind_all("<Button-1>", self.clickCallbackFunc)
        self.x_index = (111, 222, 333, 444, 555, 666, 777, 888, 999)
        self.y_index = (66, 176, 286, 396, 506, 616, 726, 836, 946, 1056)

        for i in self.x_index:
            for j in self.y_index:
                self.canvas.create_image(i, j, image=self.texture[Piece.NoneType])

    def draw(self, grid):
        for i in range(9):
            for j in range(10):
                # print(self.canvas.find_closest(self.x_index[i], self.y_index[j])[0])
                self.canvas.itemconfigure(self.canvas.find_closest(self.x_index[i], self.y_index[j])[0], image=self.texture[grid[j][i]])
        self.canvas.update()

    def clickCallbackFunc(self, event: Event):
        pass

    def setModel(self, model):
        self.model = model

    def startApp(self):
        self.root.mainloop()
