#ifndef GAMEMODEL_H
#define GAMEMODEL_H

#include <vector>
#include <unordered_map>
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

    // Returns a dict with {position1: [threat1, threat2], position2: [threat1, threat2, threat3]}
    std::unordered_map<Position, std::vector<Position>> getThreatBySide(Player side);

    std::vector<Position> getSide(Player side);

    // Return all locations of this kind of piece
    std::vector<Position> findPiece(Piece piece);

    std::vector<Action> getLegalActionsBySide(Player direction);

    Player getWinner();

    bool isMatchOver() { return getWinner() != Player::NoneType; }

    void init_with_start_game();

    std::vector<std::vector<Piece>> board;
    Player myself{Player::Red};
};

//    def __eq__(self, other):
//        # Allows two states to be compared.
//        return hasattr(other, 'board') and self.board == other.board
//
//    def __hash__(self):
//        # Allows gameModel to be keys of dictionaries.
//        return hash(tuple(tuple(x) for x in self.board))

#endif //GAMEMODEL_H
