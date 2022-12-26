#ifndef UTILS_H
#define UTILS_H


#include <ostream>

class Player {
public:
    enum Value {
        NoneType = 0, Red = 1, Black = -1, Draw = 10
    };

    Player() = delete;

    constexpr explicit Player(Value player) : value(player) {}

    constexpr bool operator==(Player that) const { return value == that.value; }

    constexpr bool operator!=(Player that) const { return value != that.value; }

    friend std::ostream &operator<<(std::ostream &os, const Player &player) {
        switch (player.value) {
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
        if (value == Red) {
            return Player(Black);
        } else if (value == Black) {
            return Player(Red);
        } else {
            return Player(NoneType);
        }
    }

private:
    Value value;
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

    constexpr explicit Piece(Value piece) : value(piece) {}

    constexpr bool operator==(Piece that) const { return value == that.value; }

    constexpr bool operator!=(Piece that) const { return value != that.value; }

    [[nodiscard]] Player getSide() const {
        switch (value) {
            case NoneType:
                return Player(Player::NoneType);
            case BGeneral:
            case BAdvisor:
            case BElephant:
            case BHorse:
            case BChariot:
            case BCannon:
            case BSoldier:
                return Player(Player::Black);
            case RGeneral:
            case RAdvisor:
            case RElephant:
            case RHorse:
            case RChariot:
            case RCannon:
            case RSoldier:
                return Player(Player::Red);
        }
    }

private:
    Value value;
};

// TODO: implement dict with unordered map
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
