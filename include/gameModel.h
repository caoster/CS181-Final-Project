#ifndef GAMEMODEL_H
#define GAMEMODEL_H

#include <vector>
#include <unordered_map>
#include <JuceHeader.h>
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

    GameState(const GameState &gameState) {
        myself = gameState.myself;
        board = gameState.board;
    }

    GameState &operator=(const GameState &gameState) = default;

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

    Piece operator[](Position position) const { return board[position.first][position.second]; }

    bool operator<(const GameState &rhs) const {
        return board < rhs.board;
    }

    bool operator==(const GameState &rhs) const {
        return board == rhs.board;
    }

public: // variables
    Board board;
    Player myself{Player::Red};
};


class GameModel : public juce::Thread {
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

    void run() override;

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
