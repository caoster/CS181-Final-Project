#ifndef GAMEMODEL_H
#define GAMEMODEL_H

#include <vector>
#include <unordered_map>
#include "include.h"
#include "utils.h"
#include "agent.h"
#include "gameView.h"

class GameState {
public: // functions
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

	std::vector<Position> getProtectorBySide(Player side, Position position);

    std::vector<Position> getSide(Player side);

    // Return all locations of this kind of piece
    std::vector<Position> findPiece(Piece piece);

    std::vector<Action> getLegalActionsBySide(Player direction);

    Player getWinner();

    bool isMatchOver() { return getWinner() != Player::NoneType; }

    void init_with_start_game();

public: // variables
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


class GameModel {
public: // functions
    GameModel() = delete;

    GameModel(GameView *canvas, Agent *RedAgent, Agent *BlackAgent);

    // Note that this function do not care which side you are
    bool isValidMove(Position src, Position dst);

    // Getter of board
    const GameState &board() { return _board; }

    GameState getGameState();

    std::vector<Position> getRange(Position position);

    std::vector<Position> getSide(Player side);

    // Return all locations of this kind of piece
    std::vector<Position> findPiece(Piece piece);

    std::vector<Action> getLegalActionBySide(Player direction);

    Player startGame();

    Player startApp();

private: // functions
    void _draw();

private: // variables
    GameState _board;
    float _interval;
    GameView *_canvas;
    Agent *_red_agent;
    Agent *_black_agent;
    // self._gameThread: Optional[Thread] = None
};

#endif //GAMEMODEL_H
