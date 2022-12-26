#ifndef GAMEMODEL_H
#define GAMEMODEL_H

#include <vector>
#include "utils.h"

class GameState {
public:
    GameState() = default;

    GameState(GameState &gameState) {
        myself = gameState.myself;
        board = gameState.board;
    }

    [[nodiscard]] Player opponent() const { return myself.reverse(); }

    void swapDirection() { myself = myself.reverse(); }

    [[nodiscard]] GameState getNextState(Action action);

    // Note that this function do not care which side you are
    bool isValidMove(Position src, Position dst);

    std::vector<Position> getRange(Position position);

    std::vector<std::vector<Piece>> board;
    Player myself{Player::Red};
};

#endif //GAMEMODEL_H
