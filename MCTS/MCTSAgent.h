//
// Created by nick on 22-12-31.
//

#ifndef CHINESE_CHESS_MCTSAGENT_H
#define CHINESE_CHESS_MCTSAGENT_H

#include "../include/agent.h"
#include "../include/data.h"
#include "../include/include.h"
#include "../include/utils.h"
#include <cstdio>
#include <random>

class MCTSNode
{
public:
    MCTSNode() = default;
    void setState(GameState other_state);
    void setParent(MCTSNode *parent);
    void setVisitTime(int visit_time);
    void setQualityValue(float quality_value);
    bool isAllExpanded();
    void find_all_valid_action();
    void init_quality_value();
    Action randomChooseNextAction();
    MCTSNode expand();
    MCTSNode randomExpand();
    float calUCB(float c, MCTSNode child);
    std::pair<Action, MCTSNode> bestChild(bool is_exploration);
    float quality_value = 0.0f;

private:
    int visit_time = 0;
    size_t num_all_valid_action = 0;
    MCTSNode *parent = nullptr;
    GameState state;
    std::vector<Action> all_valid_action;
    // changes in children construction
    std::map<Action, MCTSNode> children;
};

#endif// CHINESE_CHESS_MCTSAGENT_H
