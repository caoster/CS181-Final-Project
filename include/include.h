#ifndef INCLUDE_H
#define INCLUDE_H

#include <string>

struct {
    int resolution = 2; // Must be 1/2/4
    float interval = 1.0f;
    std::string red = "MinimaxAgent";
    std::string black = "MCTSAgent";
    bool no_graphics = false;
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
