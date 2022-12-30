#ifndef CS181_FINAL_PROJECT_CPP_qlearningAgent_H
#define CS181_FINAL_PROJECT_CPP_qlearningAgent_H

#include "../include/agent.h"
#include "../include/data.h"
#include "../include/include.h"
#include "../include/utils.h"
#include <cstdio>

class QlearningAgent : public Agent, public EvaluationMatrix
{
public:
    QlearningAgent(Player player, float alpha, float gamma, float epsilon, Counter qvalue) : Agent(player), EvaluationMatrix(), myalpha(alpha), mygamma(gamma), myepsilon(epsilon), q_value(qvalue){}
    Action step() override;
    Counter getQValueBoard();
    void update(Action action);

private:
    float myepsilon;
    float myalpha;
    float mygamma;
    float mydiscount;
    Counter q_value;
    GameState last_state;
    Action last_action;
    float myreward;
    float getQValue(std::vector<std::vector<Piece>> current_board, Action action);
    Action computeActionFromQValues(std::vector<std::vector<Piece>> current_board);
    float getReward(GameState state, Action action, Player player);
    bool flipcoin();
    Action getAction(std::vector<std::vector<Piece>> board);
};

#endif