#ifndef UTILS_H
#define UTILS_H


#include <ostream>
#include <vector>
#include <algorithm>
#include <cassert>

#define NOT_REACHED assert(false && "This statement should not be reached!");

using Position = std::pair<size_t, size_t>;
using Action = std::pair<Position, Position>;
using ScoreMatrix = std::vector<std::vector<int>>;

template<>
struct std::hash<Position> {
    std::size_t operator()(const Position &k) const {
        return (std::hash<size_t>()(k.first) ^ (std::hash<size_t>()(k.second) << 1));
    }
};

// This function can transpose a matrix
template<typename T>
std::vector<std::vector<T>> transpose(std::vector<std::vector<T>> in) {
    std::vector<std::vector<T>> out(in[0].size(), std::vector<T>(in.size()));
    for (size_t i = 0; i < in.size(); ++i)
        for (size_t j = 0; j < in[0].size(); ++j)
            out[j][i] = in[i][j];
    return out;
}

// This function can find a value in vector<vector<int>>
template<typename T>
inline bool find_2D(std::vector<std::vector<T>> matrix, T value) {
    return std::find_if(matrix.begin(), matrix.end(), [value](const std::vector<T> &v) {
        return find(v.begin(), v.end(), value) != v.end();
    }) != matrix.end();
}

class Player {
public:
    enum Value {
        NoneType = 0, Red = 1, Black = -1, Draw = 10
    };

    Player() = delete;

    constexpr Player(Value player) : _value(player) {} // Let clang-tidy shut up, I need non-explicit here.

    constexpr bool operator==(Player that) const { return _value == that._value; }

    constexpr bool operator!=(Player that) const { return _value != that._value; }

    constexpr bool operator==(Player::Value that) const { return _value == that; }

    constexpr bool operator!=(Player::Value that) const { return _value != that; }

    friend std::ostream &operator<<(std::ostream &os, const Player &player) {
        switch (player._value) {
            case NoneType:
                return os << "NoneType";
            case Red:
                return os << "Red";
            case Black:
                return os << "Black";
            case Draw:
                return os << "Draw";
        }
    }

    [[nodiscard]] Player reverse() const {
        // Player.reverse should never be called upon Draw
        if (_value == Red) {
            return {Black};
        } else if (_value == Black) {
            return {Red};
        } else {
            return {NoneType};
        }
    }

private:
    Value _value;
};


class Piece {
// Black/Red
// General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
public:
    enum Value {
        NoneType = 0,
        BGeneral = 1,
        BAdvisor = 2,
        BElephant = 3,
        BHorse = 4,
        BChariot = 5,
        BCannon = 6,
        BSoldier = 7,
        RGeneral = 8,
        RAdvisor = 9,
        RElephant = 10,
        RHorse = 11,
        RChariot = 12,
        RCannon = 13,
        RSoldier = 14
    };

    Piece() = delete;

    constexpr Piece(Value piece) : _value(piece) {} // Let clang-tidy shut up, I need non-explicit here.

    constexpr bool operator==(Piece that) const { return _value == that._value; }

    constexpr bool operator!=(Piece that) const { return _value != that._value; }

    Value value() { return _value; }

    [[nodiscard]] Player getSide() const {
        switch (_value) {
            case NoneType:
                return {Player::NoneType};
            case BGeneral:
            case BAdvisor:
            case BElephant:
            case BHorse:
            case BChariot:
            case BCannon:
            case BSoldier:
                return {Player::Black};
            case RGeneral:
            case RAdvisor:
            case RElephant:
            case RHorse:
            case RChariot:
            case RCannon:
            case RSoldier:
                return {Player::Red};
        }
    }

    friend std::ostream &operator<<(std::ostream &os, const Piece &piece) {
        switch (piece._value) {
            case NoneType:
                return os << "NoneType";
            case BGeneral:
                return os << "BGeneral";
            case BAdvisor:
                return os << "BAdvisor";
            case BElephant:
                return os << "BElephant";
            case BHorse:
                return os << "BHorse";
            case BChariot:
                return os << "BChariot";
            case BCannon:
                return os << "BCannon";
            case BSoldier:
                return os << "BSoldier";
            case RGeneral:
                return os << "RGeneral";
            case RAdvisor:
                return os << "RAdvisor";
            case RElephant:
                return os << "RElephant";
            case RHorse:
                return os << "RHorse";
            case RChariot:
                return os << "RChariot";
            case RCannon:
                return os << "RCannon";
            case RSoldier:
                return os << "RSoldier";
        }
    }

    friend std::hash<Piece>;

private:
    Value _value;
};


template<>
struct std::hash<Piece> {
    std::size_t operator()(const Piece &k) const {
        return (std::hash<int>()(k._value));
    }
};

// TODO: implement dict with unordered map
// key = tuple[gameState, tuple[(int, int), (int, int)]]
// _value = float
//class Counter(dict):
//
//    def __getitem__(self, idx):
//        self.setdefault(idx, 0)
//        return dict.__getitem__(self, idx)
//
//    def copy(self):
//        """
//        Returns a copy of the counter
//        """
//        return Counter(dict.copy(self))
//

#endif //UTILS_H
