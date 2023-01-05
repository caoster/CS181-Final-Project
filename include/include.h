#ifndef INCLUDE_H
#define INCLUDE_H

#include <string>

struct {
    int resolution = 1; // Must be 1/2/4
    float interval = 0;
    std::string red = "MinimaxAgent";
    std::string black = "RandomAgent";
    bool no_graphics = false;
    size_t num_of_matches = 50;
} m_config;

class Player;
class Piece;
class GameState;
class GameModel;
class Texture;
class GameView;
class Agent;
class RandomAgent;

#endif //INCLUDE_H
