#include "gameModel.h"
#include <algorithm>


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
        } else return false;
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
