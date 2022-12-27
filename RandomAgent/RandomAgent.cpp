#include <random>
#include "RandomAgent.h"


Action RandomAgent::step() {
    // First get all piece of Agent's side
    auto all_pieces = game->getSide(direction);
    while (true) {
        // Select one piece randomly
        std::shuffle(all_pieces.begin(), all_pieces.end(), randomEngine);
        auto pos = all_pieces[0];
        auto all_valid_move = game->getRange(pos);
        if (all_valid_move.empty()) continue;
        // Select a valid move randomly
        std::shuffle(all_valid_move.begin(), all_valid_move.end(), randomEngine);
        return std::make_pair(pos, all_valid_move[0]);
    }
}
