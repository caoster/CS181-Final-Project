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
#include <utility>

class MCTSNode : public std::enable_shared_from_this<MCTSNode> {
public:
    MCTSNode() = default;

    void setState(const GameState &other_state);

//    void setParent(std::shared_ptr<MCTSNode> parent);

    void setVisitTime(int visit_time);

    void setQualityValue(float quality_value);

    bool isAllExpanded();

    void find_all_valid_action();

    void init_quality_value();

    Action randomChooseNextAction();

    std::shared_ptr<MCTSNode> expand();

    std::shared_ptr<MCTSNode> randomExpand();

    float calUCB(float c, const std::shared_ptr<MCTSNode> &child) const;

    std::pair<Action, std::shared_ptr<MCTSNode>> bestChild(bool is_exploration);

    float calRewardFromState(Player direction);

private:
    friend class MCTSAgent;

    int visit_time = 0;
    size_t num_all_valid_action = 0;
    MCTSNode *parent = nullptr;
    GameState state;
    std::vector<Action> all_valid_action;
    // changes in children construction
    std::map<Action, std::shared_ptr<MCTSNode>> children;
    float quality_value = 0.0f;
};

class MCTSAgent : public Agent {
public:
    explicit MCTSAgent(Player player, int budget = 4000);

    ~MCTSAgent() override = default;

    Action step() override;

private:
    int computation_budget;
    int tie = 0;
    std::shared_ptr<MCTSNode> root;

    static std::shared_ptr<MCTSNode> treePolicy(std::shared_ptr<MCTSNode> node);

    std::pair<std::shared_ptr<MCTSNode>, float> defaultPolicy(std::shared_ptr<MCTSNode> node);

    void backup(const std::shared_ptr<MCTSNode>& node, float reward);
};

#endif// CHINESE_CHESS_MCTSAGENT_H
