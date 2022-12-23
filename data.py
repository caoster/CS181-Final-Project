from utils import Piece
import numpy as np


class EvaluationMatrix:
    def __init__(self):
        self.pieceValue = {
            Piece.BGeneral: 6000, Piece.RGeneral: 6000,
            Piece.BAdvisor: 120, Piece.RAdvisor: 120,
            Piece.BElephant: 120, Piece.RElephant: 120,
            Piece.BHorse: 270, Piece.RHorse: 270,
            Piece.BChariot: 600, Piece.RChariot: 600,
            Piece.BCannon: 300, Piece.RCannon: 300,
            Piece.BSoldier: 30, Piece.RSoldier: 30
        }
        self.RGeneralScore = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 3, 3, 3, 0, 0, 0]
        ])
        self.BGeneralScore = np.array([
            [0, 0, 0, 3, 3, 3, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.RAdvisorScore = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 3, 0, 0, 0]
        ])
        self.BAdvisorScore = np.array([
            [0, 0, 0, 3, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.RElephantScore = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 2, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 3, 0, 0]
        ])
        self.BElephantScore = np.array([
            [0, 0, 3, 0, 0, 0, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 2, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.RHorseScore = np.array([
            [4, 8, 16, 12, 4, 12, 16, 8, 4],
            [4, 10, 28, 16, 8, 16, 28, 10, 4],
            [12, 14, 16, 20, 18, 20, 16, 14, 12],
            [8, 24, 18, 24, 20, 24, 18, 24, 8],
            [6, 16, 14, 18, 16, 18, 14, 16, 6],
            [4, 12, 16, 14, 12, 14, 16, 12, 4],
            [2, 6, 8, 6, 10, 6, 8, 6, 2],
            [4, 2, 8, 8, 4, 8, 8, 2, 4],
            [0, 2, 4, 4, -2, 4, 4, 2, 0],
            [0, -4, 0, 0, 0, 0, 0, -4, 0]
        ])
        self.BHorseScore = np.array([
            [0, -4, 0, 0, 0, 0, 0, -4, 0],
            [0, 2, 4, 4, -2, 4, 4, 2, 0],
            [4, 2, 8, 8, 4, 8, 8, 2, 4],
            [2, 6, 8, 6, 10, 6, 8, 6, 2],
            [4, 12, 16, 14, 12, 14, 16, 12, 4],
            [6, 16, 14, 18, 16, 18, 14, 16, 6],
            [8, 24, 18, 24, 20, 24, 18, 24, 8],
            [12, 14, 16, 20, 18, 20, 16, 14, 12],
            [4, 10, 28, 16, 8, 16, 28, 10, 4],
            [4, 8, 16, 12, 4, 12, 16, 8, 4]
        ])
        self.RCannonScore = np.array([
            [6, 4, 0, -10, -12, -10, 0, 4, 6],
            [2, 2, 0, -4, -14, -4, 0, 2, 2],
            [2, 2, 0, -10, -8, -10, 0, 2, 2],
            [0, 0, -2, 4, 10, 4, -2, 0, 0],
            [0, 0, 0, 2, 8, 2, 0, 0, 0],
            [-2, 0, 4, 2, 6, 2, 4, 0, -2],
            [0, 0, 0, 2, 4, 2, 0, 0, 0],
            [4, 0, 8, 6, 10, 6, 8, 0, 4],
            [0, 2, 4, 6, 6, 6, 4, 2, 0],
            [0, 0, 2, 6, 6, 6, 2, 0, 0]
        ])
        self.BCannonScore = np.array([
            [0, 0, 2, 6, 6, 6, 2, 0, 0],
            [0, 2, 4, 6, 6, 6, 4, 2, 0],
            [4, 0, 8, 6, 10, 6, 8, 0, 4],
            [0, 0, 0, 2, 4, 2, 0, 0, 0],
            [-2, 0, 4, 2, 6, 2, 4, 0, -2],
            [0, 0, 0, 2, 8, 2, 0, 0, 0],
            [0, 0, -2, 4, 10, 4, -2, 0, 0],
            [2, 2, 0, -10, -8, -10, 0, 2, 2],
            [2, 2, 0, -4, -14, -4, 0, 2, 2],
            [6, 4, 0, -10, -12, -10, 0, 4, 6]
        ])
        self.RChariotScore = np.array([
            [14, 14, 12, 18, 16, 18, 12, 14, 14],
            [16, 20, 18, 24, 26, 24, 18, 20, 16],
            [12, 12, 12, 18, 18, 18, 12, 12, 12],
            [12, 18, 16, 22, 22, 22, 16, 18, 12],
            [12, 14, 12, 18, 18, 18, 12, 14, 12],
            [12, 16, 14, 20, 20, 20, 14, 16, 12],
            [6, 10, 8, 14, 14, 14, 8, 10, 6],
            [4, 8, 6, 14, 12, 14, 6, 8, 4],
            [8, 4, 8, 16, 8, 16, 8, 4, 8],
            [-2, 10, 6, 14, 12, 14, 6, 10, -2]
        ])
        self.BChariotScore = np.array([
            [-2, 10, 6, 14, 12, 14, 6, 10, -2],
            [8, 4, 8, 16, 8, 16, 8, 4, 8],
            [4, 8, 6, 14, 12, 14, 6, 8, 4],
            [6, 10, 8, 14, 14, 14, 8, 10, 6],
            [12, 16, 14, 20, 20, 20, 14, 16, 12],
            [12, 14, 12, 18, 18, 18, 12, 14, 12],
            [12, 18, 16, 22, 22, 22, 16, 18, 12],
            [12, 12, 12, 18, 18, 18, 12, 12, 12],
            [16, 20, 18, 24, 26, 24, 18, 20, 16],
            [14, 14, 12, 18, 16, 18, 12, 14, 14]
        ])
        self.RSoldierScore = np.array([
            [0, 3, 6, 9, 12, 9, 6, 3, 0],
            [18, 36, 56, 80, 120, 80, 56, 36, 18],
            [14, 26, 42, 60, 80, 60, 42, 26, 14],
            [10, 20, 30, 34, 40, 34, 30, 20, 10],
            [6, 12, 18, 18, 20, 18, 18, 12, 6],
            [2, 0, 8, 0, 8, 0, 8, 0, 2],
            [0, 0, -2, 0, 4, 0, -2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        self.BSoldierScore = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, -2, 0, 4, 0, -2, 0, 0],
            [2, 0, 8, 0, 8, 0, 8, 0, 2],
            [6, 12, 18, 18, 20, 18, 18, 12, 6],
            [10, 20, 30, 34, 40, 34, 30, 20, 10],
            [14, 26, 42, 60, 80, 60, 42, 26, 14],
            [18, 36, 56, 80, 120, 80, 56, 36, 18],
            [0, 3, 6, 9, 12, 9, 6, 3, 0]
        ])
        self.RGeneralScore = np.transpose(self.RGeneralScore)
        self.BGeneralScore = np.transpose(self.BGeneralScore)
        self.RAdvisorScore = np.transpose(self.RAdvisorScore)
        self.BAdvisorScore = np.transpose(self.BAdvisorScore)
        self.RElephantScore = np.transpose(self.RElephantScore)
        self.BElephantScore = np.transpose(self.BElephantScore)
        self.RHorseScore = np.transpose(self.RHorseScore)
        self.BHorseScore = np.transpose(self.BHorseScore)
        self.RChariotScore = np.transpose(self.RChariotScore)
        self.BChariotScore = np.transpose(self.BChariotScore)
        self.RCannonScore = np.transpose(self.RCannonScore)
        self.BCannonScore = np.transpose(self.BCannonScore)
        self.RSoldierScore = np.transpose(self.RSoldierScore)
        self.BSoldierScore = np.transpose(self.BSoldierScore)
        self.pieceScore = {
            Piece.RGeneral: self.RGeneralScore,
            Piece.BGeneral: self.BGeneralScore,
            Piece.RAdvisor: self.RAdvisorScore,
            Piece.BAdvisor: self.BAdvisorScore,
            Piece.RElephant: self.RElephantScore,
            Piece.BElephant: self.BElephantScore,
            Piece.RHorse: self.RHorseScore,
            Piece.BHorse: self.BHorseScore,
            Piece.RChariot: self.RChariotScore,
            Piece.BChariot: self.BChariotScore,
            Piece.RCannon: self.RCannonScore,
            Piece.BCannon: self.BCannonScore,
            Piece.RSoldier: self.RSoldierScore,
            Piece.BSoldier: self.BSoldierScore
        }
