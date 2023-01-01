#ifndef CS181_FINAL_PROJECT_CPP_QLEARNING_AGENT_H
#define CS181_FINAL_PROJECT_CPP_QLEARNING_AGENT_H

#include "../include/agent.h"
#include "../include/data.h"
#include "../include/include.h"
#include "../include/utils.h"
#include <cstdio>
#include <utility>
#include <random>

using Key = std::pair<Board, Action>;

class Counter {
public: // functions
    float operator[](const Key &idx) {
        if (auto it = dict.find(idx); it != dict.end()) {
            return it->second;
        }
        return 0.0f;
    }

    void set(const Key &idx, float value) {
        dict[idx] = value;
    }

public: // variables
    std::map<Key, float> dict;
};

class QlearningAgent : public Agent, public EvaluationMatrix {
public:
    QlearningAgent(Player player, float alpha, float gamma, float epsilon, Counter qvalue) : Agent(player), EvaluationMatrix(), myepsilon(epsilon), myalpha(alpha), mydiscount(gamma),
                                                                                             q_value(std::move(qvalue)), myreward(0) {}

    Action step() override;

    Counter getQValueBoard();

    void update(Action action);

private:
    float myepsilon;
    float myalpha;
    float mydiscount;
    Counter q_value;
    GameState last_state;
    Action last_action;
    float myreward;
    std::default_random_engine rng{std::random_device()()};

    float getQValue(const Board &current_board, Action action);

    Action computeActionFromQValues(const Board &current_board);

    float getReward(GameState state, Action action, Player player);

    bool flipcoin();

    Action getAction(const Board &board);
};

#endif