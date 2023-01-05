#include "../include/gameModel.h"
#include <algorithm>
#include <cassert>
#include <fstream>
#include <thread>


GameState GameState::getNextState(Action action) {
    auto [src, dst] = action;
    auto newState = GameState(*this);
    newState.board[dst.first][dst.second] = newState.board[src.first][src.second];
    newState.board[src.first][src.second] = Piece::NoneType;
    newState.swapDirection();
    return newState;
}

bool GameState::isValidMove(Position src, Position dst) {
    auto [src_x, src_y] = src;
    auto piece = board[src_x][src_y];
    if (piece == Piece::NoneType) {
        return false;
    } else {
        auto range = getRange(src);
        return std::find(range.begin(), range.end(), dst) != range.end();
    }
}

std::vector<Position> GameState::getRange(Position position) {
    auto [x_size_t, y_size_t] = position;
    auto pieceType = board[x_size_t][y_size_t];
    int x = (int) x_size_t;
    int y = (int) y_size_t;
    std::vector<Position> result{};
    if (pieceType == Piece::NoneType) { return result; }

    auto checkEmpty = [this](int loc_x, int loc_y) { return board[(size_t) loc_x][(size_t) loc_y] == Piece::NoneType; };
    auto inRange = [](int loc_x, int loc_y) { return 0 <= loc_x && loc_x < 9 && 0 <= loc_y && loc_y < 10; };
    auto inRangeAndEmpty = [this, inRange](int loc_x, int loc_y) {
        if (inRange(loc_x, loc_y)) {
            return board[(size_t) loc_x][(size_t) loc_y] == Piece::NoneType;
        } else
            return false;
    };
    auto checkForBlack = [this, &result](int loc_x, int loc_y) {
        if (board[(size_t) loc_x][(size_t) loc_y].getSide() != Player::Black) {
            result.emplace_back((size_t) loc_x, (size_t) loc_y);
        }
    };
    auto checkForRed = [this, &result](int loc_x, int loc_y) {
        if (board[(size_t) loc_x][(size_t) loc_y].getSide() != Player::Red) {
            result.emplace_back((size_t) loc_x, (size_t) loc_y);
        }
    };
    auto safeCheckForBlack = [inRange, checkForBlack](int loc_x, int loc_y) {
        if (inRange(loc_x, loc_y)) {
            checkForBlack(loc_x, loc_y);
        }
    };
    auto safeCheckForRed = [inRange, checkForRed](int loc_x, int loc_y) {
        if (inRange(loc_x, loc_y)) {
            checkForRed(loc_x, loc_y);
        }
    };

    switch (pieceType.value()) {
        case Piece::BGeneral: {
            if (position == Position{3, 0}) {
                checkForBlack(3, 1);
                checkForBlack(4, 0);
            } else if (position == Position{3, 1}) {
                checkForBlack(3, 0);
                checkForBlack(4, 1);
                checkForBlack(3, 2);
            } else if (position == Position{3, 2}) {
                checkForBlack(3, 1);
                checkForBlack(4, 2);
            } else if (position == Position{4, 0}) {
                checkForBlack(3, 0);
                checkForBlack(4, 1);
                checkForBlack(5, 0);
            } else if (position == Position{4, 1}) {
                checkForBlack(3, 1);
                checkForBlack(4, 0);
                checkForBlack(4, 2);
                checkForBlack(5, 1);
            } else if (position == Position{4, 2}) {
                checkForBlack(4, 1);
                checkForBlack(3, 2);
                checkForBlack(5, 2);
            } else if (position == Position{5, 0}) {
                checkForBlack(4, 0);
                checkForBlack(5, 1);
            } else if (position == Position{5, 1}) {
                checkForBlack(5, 0);
                checkForBlack(4, 1);
                checkForBlack(5, 2);
            } else if (position == Position{5, 2}) {
                checkForBlack(5, 1);
                checkForBlack(4, 2);
            }
            break;
        }
        case Piece::BAdvisor: {
            if (position == Position{3, 0} ||
                position == Position{5, 0} ||
                position == Position{3, 2} ||
                position == Position{5, 2}) {
                checkForBlack(4, 1);
            } else if (position == Position{4, 1}) {
                checkForBlack(3, 0);
                checkForBlack(5, 0);
                checkForBlack(3, 2);
                checkForBlack(5, 2);
            }
            break;
        }
        case Piece::BElephant: {
            if (inRangeAndEmpty(x - 1, y - 1) && 0 <= y - 2 && y - 2 <= 4)
                safeCheckForBlack(x - 2, y - 2);
            if (inRangeAndEmpty(x + 1, y - 1) && 0 <= y - 2 && y - 2 <= 4)
                safeCheckForBlack(x + 2, y - 2);
            if (inRangeAndEmpty(x - 1, y + 1) && 0 <= y + 2 && y + 2 <= 4)
                safeCheckForBlack(x - 2, y + 2);
            if (inRangeAndEmpty(x + 1, y + 1) && 0 <= y + 2 && y + 2 <= 4)
                safeCheckForBlack(x + 2, y + 2);
            break;
        }
        case Piece::BHorse: {
            if (inRangeAndEmpty(x + 1, y)) {
                safeCheckForBlack(x + 2, y - 1);
                safeCheckForBlack(x + 2, y + 1);
            }
            if (inRangeAndEmpty(x, y + 1)) {
                safeCheckForBlack(x + 1, y + 2);
                safeCheckForBlack(x - 1, y + 2);
            }
            if (inRangeAndEmpty(x - 1, y)) {
                safeCheckForBlack(x - 2, y + 1);
                safeCheckForBlack(x - 2, y - 1);
            }
            if (inRangeAndEmpty(x, y - 1)) {
                safeCheckForBlack(x - 1, y - 2);
                safeCheckForBlack(x + 1, y - 2);
            }
            break;
        }
        case Piece::BChariot: {
            // Direction: right
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x + i, y)) break;
                if (checkEmpty(x + i, y)) {
                    result.emplace_back(x + i, y);
                    continue;
                }
                checkForBlack(x + i, y);
                break;
            }
            // Direction: left
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x - i, y)) break;
                if (checkEmpty(x - i, y)) {
                    result.emplace_back(x - i, y);
                    continue;
                }
                checkForBlack(x - i, y);
                break;
            }
            // Direction: up
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y - i)) break;
                if (checkEmpty(x, y - i)) {
                    result.emplace_back(x, y - i);
                    continue;
                }
                checkForBlack(x, y - i);
                break;
            }
            // Direction: down
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y + i)) break;
                if (checkEmpty(x, y + i)) {
                    result.emplace_back(x, y + i);
                    continue;
                }
                checkForBlack(x, y + i);
                break;
            }
            break;
        }
        case Piece::BCannon: {
            // Direction: right
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x + i, y)) break;
                if (checkEmpty(x + i, y)) {
                    result.emplace_back(x + i, y);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x + j, y)) break;
                    if (!checkEmpty(x + j, y)) {
                        if (board[(size_t) x + (size_t) j][(size_t) y].getSide() == Player::Red)
                            result.emplace_back(x + j, y);
                        break;
                    }
                }
                break;
            }
            // Direction: left
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x - i, y)) break;
                if (checkEmpty(x - i, y)) {
                    result.emplace_back(x - i, y);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x - j, y))
                        break;
                    if (!checkEmpty(x - j, y)) {
                        if (board[(size_t) x - (size_t) j][(size_t) y].getSide() == Player::Red)
                            result.emplace_back(x - j, y);
                        break;
                    }
                }
                break;
            }
            // Direction: up
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y - i)) break;
                if (checkEmpty(x, y - i)) {
                    result.emplace_back(x, y - i);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x, y - j)) break;
                    if (!checkEmpty(x, y - j)) {
                        if (board[(size_t) x][(size_t) y - (size_t) j].getSide() == Player::Red)
                            result.emplace_back(x, y - j);
                        break;
                    }
                }
                break;
            }
            // Direction: down
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y + i)) break;
                if (checkEmpty(x, y + i)) {
                    result.emplace_back(x, y + i);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x, y + j)) break;
                    if (!checkEmpty(x, y + j)) {
                        if (board[(size_t) x][(size_t) y + (size_t) j].getSide() == Player::Red)
                            result.emplace_back(x, y + j);
                        break;
                    }
                }
                break;
            }
            break;
        }
        case Piece::BSoldier: {
            if (y <= 4) {
                checkForBlack(x, y + 1);
            } else {
                safeCheckForBlack(x, y + 1);
                safeCheckForBlack(x - 1, y);
                safeCheckForBlack(x + 1, y);
            }
            break;
        }
        case Piece::RGeneral: {
            if (position == Position{3, 9}) {
                checkForRed(3, 8);
                checkForRed(4, 9);
            } else if (position == Position{4, 9}) {
                checkForRed(3, 9);
                checkForRed(5, 9);
                checkForRed(4, 8);
            } else if (position == Position{5, 9}) {
                checkForRed(4, 9);
                checkForRed(5, 8);
            } else if (position == Position{3, 8}) {
                checkForRed(3, 7);
                checkForRed(4, 8);
                checkForRed(3, 9);
            } else if (position == Position{4, 8}) {
                checkForRed(3, 8);
                checkForRed(4, 9);
                checkForRed(5, 8);
                checkForRed(4, 7);
            } else if (position == Position{5, 8}) {
                checkForRed(4, 8);
                checkForRed(5, 7);
                checkForRed(5, 9);
            } else if (position == Position{3, 7}) {
                checkForRed(3, 8);
                checkForRed(4, 7);
            } else if (position == Position{4, 7}) {
                checkForRed(3, 7);
                checkForRed(4, 8);
                checkForRed(5, 7);
            } else if (position == Position{5, 7}) {
                checkForRed(4, 7);
                checkForRed(5, 8);
            }
            break;
        }
        case Piece::RAdvisor: {
            if (position == Position{3, 9} ||
                position == Position{3, 7} ||
                position == Position{5, 7} ||
                position == Position{5, 9}) {
                checkForRed(4, 8);
            } else if (position == Position{4, 8}) {
                checkForRed(3, 7);
                checkForRed(3, 9);
                checkForRed(5, 7);
                checkForRed(5, 9);
            }
            break;
        }
        case Piece::RElephant: {
            if (inRangeAndEmpty(x - 1, y - 1) && 5 <= y - 2 && y - 2 <= 9)
                safeCheckForRed(x - 2, y - 2);
            if (inRangeAndEmpty(x + 1, y - 1) && 5 <= y - 2 && y - 2 <= 9)
                safeCheckForRed(x + 2, y - 2);
            if (inRangeAndEmpty(x - 1, y + 1) && 5 <= y + 2 && y + 2 <= 9)
                safeCheckForRed(x - 2, y + 2);
            if (inRangeAndEmpty(x + 1, y + 1) && 5 <= y + 2 && y + 2 <= 9)
                safeCheckForRed(x + 2, y + 2);
            break;
        }
        case Piece::RHorse: {
            if (inRangeAndEmpty(x + 1, y)) {
                safeCheckForRed(x + 2, y - 1);
                safeCheckForRed(x + 2, y + 1);
            }
            if (inRangeAndEmpty(x, y + 1)) {
                safeCheckForRed(x + 1, y + 2);
                safeCheckForRed(x - 1, y + 2);
            }
            if (inRangeAndEmpty(x - 1, y)) {
                safeCheckForRed(x - 2, y + 1);
                safeCheckForRed(x - 2, y - 1);
            }
            if (inRangeAndEmpty(x, y - 1)) {
                safeCheckForRed(x - 1, y - 2);
                safeCheckForRed(x + 1, y - 2);
            }
            break;
        }
        case Piece::RChariot: {
            // Direction: right
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x + i, y)) break;
                if (checkEmpty(x + i, y)) {
                    result.emplace_back(x + i, y);
                    continue;
                }
                checkForRed(x + i, y);
                break;
            }
            // Direction: left
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x - i, y)) break;
                if (checkEmpty(x - i, y)) {
                    result.emplace_back(x - i, y);
                    continue;
                }
                checkForRed(x - i, y);
                break;
            }
            // Direction: up
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y - i)) break;
                if (checkEmpty(x, y - i)) {
                    result.emplace_back(x, y - i);
                    continue;
                }
                checkForRed(x, y - i);
                break;
            }
            // Direction: down
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y + i)) break;
                if (checkEmpty(x, y + i)) {
                    result.emplace_back(x, y + i);
                    continue;
                }
                checkForRed(x, y + i);
                break;
            }
            break;
        }
        case Piece::RCannon: {
            // Direction: right
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x + i, y)) break;
                if (checkEmpty(x + i, y)) {
                    result.emplace_back(x + i, y);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x + j, y)) break;
                    if (!checkEmpty(x + j, y)) {
                        if (board[(size_t) x + (size_t) j][(size_t) y].getSide() == Player::Black)
                            result.emplace_back(x + j, y);
                        break;
                    }
                }
                break;
            }
            // Direction: left
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x - i, y)) break;
                if (checkEmpty(x - i, y)) {
                    result.emplace_back(x - i, y);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x - j, y)) break;
                    if (!checkEmpty(x - j, y)) {
                        if (board[(size_t) x - (size_t) j][(size_t) y].getSide() == Player::Black)
                            result.emplace_back(x - j, y);
                        break;
                    }
                }
                break;
            }
            // Direction: up
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y - i)) break;
                if (checkEmpty(x, y - i)) {
                    result.emplace_back(x, y - i);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x, y - j)) break;
                    if (!checkEmpty(x, y - j)) {
                        if (board[(size_t) x][(size_t) y - (size_t) j].getSide() == Player::Black)
                            result.emplace_back(x, y - j);
                        break;
                    }
                }
                break;
            }
            // Direction: down
            for (int i = 1; i < 10; ++i) {
                if (!inRange(x, y + i)) break;
                if (checkEmpty(x, y + i)) {
                    result.emplace_back(x, y + i);
                    continue;
                }
                for (int j = i + 1; j < 10; ++j) {
                    if (!inRange(x, y + j)) break;
                    if (!checkEmpty(x, y + j)) {
                        if (board[(size_t) x][(size_t) y + (size_t) j].getSide() == Player::Black)
                            result.emplace_back(x, y + j);
                        break;
                    }
                }
                break;
            }
            break;
        }
        case Piece::RSoldier: {
            if (y >= 5) {
                checkForRed(x, y - 1);
            } else {
                safeCheckForRed(x, y - 1);
                safeCheckForRed(x - 1, y);
                safeCheckForRed(x + 1, y);
            }
            break;
        }
        case Piece::NoneType:
            break;
    }
    return result;
}

std::unordered_map<Position, std::vector<Position>> GameState::getThreatBySide(Player side) {
    // A very naive implementation, yet fast enough for C++
    std::unordered_map<Position, std::vector<Position>> result;
    for (auto piece: getSide(side)) {
        result[piece] = std::vector<Position>();
    }
    for (auto piece: getSide(side.reverse())) {
        for (auto position: getRange(piece)) {
            if (result.find(position) != result.end()) {
                result[position].push_back(piece);
            }
        }
    }
    return result;
}

std::vector<Position> GameState::getProtectorBySide(Player side, Position position) {
    std::vector<Position> result;
    for (auto piece: getSide(side)) {
        for (auto pos: getRange(piece)) {
            if (pos == position) {
                result.emplace_back(piece);
            }
        }
    }
    return result;
}

std::vector<Position> GameState::getSide(Player side) {
    std::vector<Position> result{};
    for (size_t i = 0; i < board.size(); ++i) {
        for (size_t j = 0; j < board[i].size(); ++j) {
            if (board[i][j].getSide() == side)
                result.emplace_back(i, j);
        }
    }
    return result;
}

std::vector<Position> GameState::findPiece(Piece piece) {
    std::vector<Position> result{};
    for (size_t i = 0; i < board.size(); ++i) {
        for (size_t j = 0; j < board[i].size(); ++j) {
            if (board[i][j] == piece)
                result.emplace_back(i, j);
        }
    }
    return result;
}

std::vector<Action> GameState::getLegalActionsBySide(Player direction) {
    std::vector<Action> result{};
    auto pieces = getSide(direction);
    for (auto &piece: pieces) {
        auto range = getRange(piece);
        for (auto &j: range) {
            result.emplace_back(piece, j);
        }
    }
    return result;
}

Player GameState::getWinner() {
    if (!find_2D(board, {Piece::BGeneral})) return Player::Red;  // BlackGeneral captured, Red wins
    if (!find_2D(board, {Piece::RGeneral})) return Player::Black;// RedGeneral captured, Black wins
    auto [redG_x, redG_y] = findPiece(Piece::RGeneral)[0];
    auto [blackG_x, blackG_y] = findPiece(Piece::BGeneral)[0];
    if (redG_x == blackG_x) {
        bool fly = true;
        for (size_t i = blackG_y + 1; i < redG_y; ++i) {
            if (board[redG_x][i].getSide() != Player::NoneType) {
                fly = false;
                break;
            }
        }
        if (fly) return myself.reverse();
    }

    bool redLose = true;
    auto allRed = getSide(Player::Red);
    for (auto red: allRed) {
        if (!getRange(red).empty()) {
            redLose = false;
            break;
        }
    }
    if (redLose) return Player::Black;

    bool blackLose = true;
    auto allBlack = getSide(Player::Black);
    for (auto black: allBlack) {
        if (!getRange(black).empty()) {
            blackLose = false;
            break;
        }
    }
    if (blackLose) return Player::Red;

    return Player::NoneType;
}

void GameState::init_with_start_game() {
    board = {
            {Piece::BChariot,  Piece::NoneType, Piece::NoneType, Piece::BSoldier, Piece::NoneType, Piece::NoneType, Piece::RSoldier, Piece::NoneType, Piece::NoneType, Piece::RChariot},
            {Piece::BHorse,    Piece::NoneType, Piece::BCannon,  Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::RCannon,  Piece::NoneType, Piece::RHorse},
            {Piece::BElephant, Piece::NoneType, Piece::NoneType, Piece::BSoldier, Piece::NoneType, Piece::NoneType, Piece::RSoldier, Piece::NoneType, Piece::NoneType, Piece::RElephant},
            {Piece::BAdvisor,  Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::RAdvisor},
            {Piece::BGeneral,  Piece::NoneType, Piece::NoneType, Piece::BSoldier, Piece::NoneType, Piece::NoneType, Piece::RSoldier, Piece::NoneType, Piece::NoneType, Piece::RGeneral},
            {Piece::BAdvisor,  Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::RAdvisor},
            {Piece::BElephant, Piece::NoneType, Piece::NoneType, Piece::BSoldier, Piece::NoneType, Piece::NoneType, Piece::RSoldier, Piece::NoneType, Piece::NoneType, Piece::RElephant},
            {Piece::BHorse,    Piece::NoneType, Piece::BCannon,  Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::NoneType, Piece::RCannon,  Piece::NoneType, Piece::RHorse},
            {Piece::BChariot,  Piece::NoneType, Piece::NoneType, Piece::BSoldier, Piece::NoneType, Piece::NoneType, Piece::RSoldier, Piece::NoneType, Piece::NoneType, Piece::RChariot}};
    myself = Player::Red;
}

GameModel::GameModel(GameView *canvas, Agent *RedAgent, Agent *BlackAgent) : juce::Thread("GameModel") {
    _board.init_with_start_game();
    _interval = m_config.interval;
    _canvas = canvas;
    _canvas->setModel(this);
    _red_agent = RedAgent;
    _red_agent->setGameModel(this);
    _black_agent = BlackAgent;
    _black_agent->setGameModel(this);
    _draw();
    // self._gameThread: Optional[Thread] = None
}

bool GameModel::isValidMove(Position src, Position dst) {
    return _board.isValidMove(src, dst);
}

GameState GameModel::getGameState() {
    return {_board};
}

std::vector<Position> GameModel::getRange(Position position) {
    return _board.getRange(position);
}

std::vector<Position> GameModel::getSide(Player side) {
    return _board.getSide(side);
}

std::vector<Position> GameModel::findPiece(Piece piece) {
    return _board.findPiece(piece);
}

std::vector<Action> GameModel::getLegalActionBySide(Player direction) {
    return _board.getLegalActionsBySide(direction);
}

std::pair<Player, size_t> GameModel::startGame() {
    size_t cnt = 0;
	size_t notEatPiece = 0;
    this->_board.init_with_start_game();
    std::this_thread::sleep_for(std::chrono::seconds(1));
    while (true) {
        Position src, dst;
        if (_board.myself == Player::Red) {
            std::tie(src, dst) = _red_agent->step();
        } else if (_board.myself == Player::Black) {
            std::tie(src, dst) = _black_agent->step();
        }
        if (!isValidMove(src, dst)) {
            assert(false && "Invalid move!");
        }
        if (_board.board[src.first][src.second].getSide() != _board.myself) {
            assert(false && "You should only move your own piece!");
        }
		if (_board.board[dst.first][dst.second] != Piece::NoneType) {
			notEatPiece = 0;
		}
		else {
			notEatPiece++;
		}
        _board.board[dst.first][dst.second] = _board.board[src.first][src.second];
        _board.board[src.first][src.second] = Piece::NoneType;
        cnt++;
        _draw();
        std::this_thread::sleep_for(std::chrono::nanoseconds((long) (_interval * 1e9)));

        auto result = _board.getWinner();
        _board.swapDirection();
		if (notEatPiece > 40) {
			result = Player::Draw;
		}
        if (result == Player::NoneType) continue;
        else if (result == Player::Red) {
            fprintf(stdout, "Red win!\n");
            return {Player::Red, cnt};
        } else if (result == Player::Black) {
            fprintf(stdout, "Black win!\n");
            return {Player::Black, cnt};
        } else if (result == Player::Draw) {
            fprintf(stdout, "Draw!\n");
            return {Player::Draw, cnt};
        } else {
            // Just in case
            NOT_REACHED
        }
    }
}


void GameModel::_draw() {
    juce::MessageManagerLock lock;
    _canvas->draw(_board.board);
}

void GameModel::run() {
    std::ofstream fout("result.txt", std::ios::app);
    for (size_t i = 0; i < m_config.num_of_matches; ++i) {
        auto [winner, cnt] = startGame();
		if (winner == Player::Draw) {
			fout << "Draw" << std::endl;
		}
		else
            fout << winner << " wins in " << cnt << " steps." << std::endl;
    }
    exit(0);
}
