#ifndef DATA_H
#define DATA_H

#include <unordered_map>
#include "include.h"
#include "utils.h"

class EvaluationMatrix {
public: // variables
    std::unordered_map<Piece::Value, int> pieceValue{
            {Piece::BGeneral,  600000},
            {Piece::RGeneral,  600000},
            {Piece::BAdvisor,  120},
            {Piece::RAdvisor,  120},
            {Piece::BElephant, 120},
            {Piece::RElephant, 120},
            {Piece::BHorse,    270},
            {Piece::RHorse,    270},
            {Piece::BChariot,  600},
            {Piece::RChariot,  600},
            {Piece::BCannon,   450},
            {Piece::RCannon,   450},
            {Piece::BSoldier,  30},
            {Piece::RSoldier,  30},
            {Piece::NoneType,  0}
    };

    std::unordered_map<Piece::Value, double> pieceFlexibility{
            {Piece::BGeneral,  0},
            {Piece::RGeneral,  0},
            {Piece::BAdvisor,  1},
            {Piece::RAdvisor,  1},
            {Piece::BElephant, 1},
            {Piece::RElephant, 1},
            {Piece::BHorse,    5},
            {Piece::RHorse,    5},
            {Piece::BChariot,  9},
            {Piece::RChariot,  9},
            {Piece::BCannon,   10},
            {Piece::RCannon,   10},
            {Piece::BSoldier,  1.5},
            {Piece::RSoldier,  1.5}
    };

    ScoreMatrix RGeneralScore{
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 1, 1, 1, 0, 0, 0},
            {0, 0, 0, 2, 2, 2, 0, 0, 0},
            {0, 0, 0, 3, 3, 3, 0, 0, 0}
    };
    ScoreMatrix BGeneralScore{
            {0, 0, 0, 3, 3, 3, 0, 0, 0},
            {0, 0, 0, 2, 2, 2, 0, 0, 0},
            {0, 0, 0, 1, 1, 1, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0}
    };


    ScoreMatrix RAdvisorScore{
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 1, 0, 1, 0, 0, 0},
            {0, 0, 0, 0, 3, 0, 0, 0, 0},
            {0, 0, 0, 3, 0, 3, 0, 0, 0}
    };
    ScoreMatrix BAdvisorScore{
            {0, 0, 0, 3, 0, 3, 0, 0, 0},
            {0, 0, 0, 0, 3, 0, 0, 0, 0},
            {0, 0, 0, 1, 0, 1, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0}
    };
    ScoreMatrix RElephantScore{
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 1, 0, 0, 0, 1, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {2, 0, 0, 0, 3, 0, 0, 0, 2},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 3, 0, 0, 0, 3, 0, 0}
    };
    ScoreMatrix BElephantScore{
            {0, 0, 3, 0, 0, 0, 3, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {2, 0, 0, 0, 3, 0, 0, 0, 2},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 1, 0, 0, 0, 1, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0},
            {0, 0, 0, 0, 0, 0, 0, 0, 0}
    };
    ScoreMatrix RHorseScore{
            {4,  8,  16, 12, 4,  12, 16, 8,  4},
            {4,  10, 28, 16, 8,  16, 28, 10, 4},
            {12, 14, 16, 20, 18, 20, 16, 14, 12},
            {8,  24, 18, 24, 20, 24, 18, 24, 8},
            {6,  16, 14, 18, 16, 18, 14, 16, 6},
            {4,  12, 16, 14, 12, 14, 16, 12, 4},
            {2,  6,  8,  6,  10, 6,  8,  6,  2},
            {4,  2,  8,  8,  4,  8,  8,  2,  4},
            {0,  2,  4,  4,  -2, 4,  4,  2,  0},
            {0,  -4, 0,  0,  0,  0,  0,  -4, 0}
    };
    ScoreMatrix BHorseScore{
            {0,  -4, 0,  0,  0,  0,  0,  -4, 0},
            {0,  2,  4,  4,  -2, 4,  4,  2,  0},
            {4,  2,  8,  8,  4,  8,  8,  2,  4},
            {2,  6,  8,  6,  10, 6,  8,  6,  2},
            {4,  12, 16, 14, 12, 14, 16, 12, 4},
            {6,  16, 14, 18, 16, 18, 14, 16, 6},
            {8,  24, 18, 24, 20, 24, 18, 24, 8},
            {12, 14, 16, 20, 18, 20, 16, 14, 12},
            {4,  10, 28, 16, 8,  16, 28, 10, 4},
            {4,  8,  16, 12, 4,  12, 16, 8,  4}
    };
    ScoreMatrix RCannonScore{
            {6,  4, 0,  -10, -12, -10, 0,  4, 6},
            {2,  2, 0,  -4,  -14, -4,  0,  2, 2},
            {2,  2, 0,  -10, -8,  -10, 0,  2, 2},
            {0,  0, -2, 4,   10,  4,   -2, 0, 0},
            {0,  0, 0,  2,   8,   2,   0,  0, 0},
            {-2, 0, 4,  2,   6,   2,   4,  0, -2},
            {0,  0, 0,  2,   4,   2,   0,  0, 0},
            {4,  0, 8,  6,   20,  6,   8,  0, 4},
            {0,  2, 4,  6,   6,   6,   4,  2, 0},
            {0,  0, 2,  6,   6,   6,   2,  0, 0}
    };
    ScoreMatrix BCannonScore{
            {0,  0, 2,  6,   6,   6,   2,  0, 0},
            {0,  2, 4,  6,   6,   6,   4,  2, 0},
            {4,  0, 8,  6,   20,  6,   8,  0, 4},
            {0,  0, 0,  2,   4,   2,   0,  0, 0},
            {-2, 0, 4,  2,   6,   2,   4,  0, -2},
            {0,  0, 0,  2,   8,   2,   0,  0, 0},
            {0,  0, -2, 4,   10,  4,   -2, 0, 0},
            {2,  2, 0,  -10, -8,  -10, 0,  2, 2},
            {2,  2, 0,  -4,  -14, -4,  0,  2, 2},
            {6,  4, 0,  -10, -12, -10, 0,  4, 6}
    };
    ScoreMatrix RChariotScore{
            {14, 14, 12, 18, 16, 18, 12, 14, 14},
            {16, 20, 18, 24, 26, 24, 18, 20, 16},
            {12, 12, 12, 18, 18, 18, 12, 12, 12},
            {12, 18, 16, 22, 22, 22, 16, 18, 12},
            {12, 14, 12, 18, 18, 18, 12, 14, 12},
            {12, 16, 14, 20, 20, 20, 14, 16, 12},
            {6,  10, 8,  14, 14, 14, 8,  10, 6},
            {4,  8,  6,  14, 12, 14, 6,  8,  4},
            {8,  4,  8,  16, 8,  16, 8,  4,  8},
            {-2, 10, 6,  14, 12, 14, 6,  10, -2}
    };
    ScoreMatrix BChariotScore{
            {-2, 10, 6,  14, 12, 14, 6,  10, -2},
            {8,  4,  8,  16, 8,  16, 8,  4,  8},
            {4,  8,  6,  14, 12, 14, 6,  8,  4},
            {6,  10, 8,  14, 14, 14, 8,  10, 6},
            {12, 16, 14, 20, 20, 20, 14, 16, 12},
            {12, 14, 12, 18, 18, 18, 12, 14, 12},
            {12, 18, 16, 22, 22, 22, 16, 18, 12},
            {12, 12, 12, 18, 18, 18, 12, 12, 12},
            {16, 20, 18, 24, 26, 24, 18, 20, 16},
            {14, 14, 12, 18, 16, 18, 12, 14, 14}
    };
    ScoreMatrix RSoldierScore{
            {0,  3,  6,  9,  12,  9,  6,  3,  0},
            {18, 36, 56, 80, 120, 80, 56, 36, 18},
            {14, 26, 42, 60, 80,  60, 42, 26, 14},
            {10, 20, 30, 34, 40,  34, 30, 20, 10},
            {6,  12, 18, 18, 20,  18, 18, 12, 6},
            {2,  0,  8,  0,  8,   0,  8,  0,  2},
            {0,  0,  -2, 0,  4,   0,  -2, 0,  0},
            {0,  0,  0,  0,  0,   0,  0,  0,  0},
            {0,  0,  0,  0,  0,   0,  0,  0,  0},
            {0,  0,  0,  0,  0,   0,  0,  0,  0}
    };
    ScoreMatrix BSoldierScore{
            {0,  0,  0,  0,  0,   0,  0,  0,  0},
            {0,  0,  0,  0,  0,   0,  0,  0,  0},
            {0,  0,  0,  0,  0,   0,  0,  0,  0},
            {0,  0,  -2, 0,  4,   0,  -2, 0,  0},
            {2,  0,  8,  0,  8,   0,  8,  0,  2},
            {6,  12, 18, 18, 20,  18, 18, 12, 6},
            {10, 20, 30, 34, 40,  34, 30, 20, 10},
            {14, 26, 42, 60, 80,  60, 42, 26, 14},
            {18, 36, 56, 80, 120, 80, 56, 36, 18},
            {0,  3,  6,  9,  12,  9,  6,  3,  0}
    };

    std::unordered_map<Piece::Value, ScoreMatrix> pieceScore = {
            {Piece::RGeneral,  RGeneralScore},
            {Piece::BGeneral,  BGeneralScore},
            {Piece::RAdvisor,  RAdvisorScore},
            {Piece::BAdvisor,  BAdvisorScore},
            {Piece::RElephant, RElephantScore},
            {Piece::BElephant, BElephantScore},
            {Piece::RHorse,    RHorseScore},
            {Piece::BHorse,    BHorseScore},
            {Piece::RChariot,  RChariotScore},
            {Piece::BChariot,  BChariotScore},
            {Piece::RCannon,   RCannonScore},
            {Piece::BCannon,   BCannonScore},
            {Piece::RSoldier,  RSoldierScore},
            {Piece::BSoldier,  BSoldierScore}
    };

public: // functions
    EvaluationMatrix() {
        RGeneralScore = transpose(RGeneralScore);
        BGeneralScore = transpose(BGeneralScore);
        RAdvisorScore = transpose(RAdvisorScore);
        BAdvisorScore = transpose(BAdvisorScore);
        RElephantScore = transpose(RElephantScore);
        BElephantScore = transpose(BElephantScore);
        RHorseScore = transpose(RHorseScore);
        BHorseScore = transpose(BHorseScore);
        RChariotScore = transpose(RChariotScore);
        BChariotScore = transpose(BChariotScore);
        RCannonScore = transpose(RCannonScore);
        BCannonScore = transpose(BCannonScore);
        RSoldierScore = transpose(RSoldierScore);
        BSoldierScore = transpose(BSoldierScore);
    }
};

#endif //DATA_H
