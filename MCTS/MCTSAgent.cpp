//
// Created by nick on 22-12-31.
//

#include "MCTSAgent.h"

bool MCTSNode::isAllExpanded()
{
    return all_valid_action.empty();
}

void MCTSNode::setState(GameState other_state)
{
    this->state = other_state;
}

void MCTSNode::setParent(MCTSNode *other_parent)
{
    this->parent = other_parent;
}

void MCTSNode::setVisitTime(int other_visit_time)
{
    this->visit_time = other_visit_time;
}

void MCTSNode::setQualityValue(float other_quality_value)
{
    this->quality_value = other_quality_value;
}

void MCTSNode::find_all_valid_action()
{
    this->all_valid_action = this->state.getLegalActionsBySide(this->state.myself);
    std::vector<Action> new_actions;
    Piece my_general = Piece::RGeneral;
    Piece other_general = Piece::BGeneral;
    Player other = this->state.myself.reverse();
    if (this->state.myself == Player::Black)
    {
        my_general = Piece::BGeneral;
        other_general = Piece::RGeneral;
    }
    auto my_piece_pos = this->state.findPiece(my_general);
    if (my_piece_pos.empty())
    {
        this->all_valid_action.clear();
        this->num_all_valid_action = 0;
        return;
    }
    auto general_neighbour = this->state.getRange(my_piece_pos[0]);
    auto attack = this->state.getThreatBySide(other);
    auto other_piece_pos = this->state.findPiece(other_general);

    // checkmate opponent
    if (!other_piece_pos.empty() && !attack[other_piece_pos[0]].empty())
    {
        for (const Position &pos: attack[other_piece_pos[0]])
        {
            new_actions.emplace_back(pos, other_piece_pos[0]);
        }
        this->all_valid_action = new_actions;
        this->num_all_valid_action = this->all_valid_action.size();
        return;
    }

    // avoid action lead to checkmate
    for (const Action &action: this->all_valid_action)
    {
        auto new_state = this->state.getNextState(action);
        auto new_threats = new_state.getThreatBySide(this->state.myself);
        auto my_new_piece_pos = my_piece_pos[0];
        if (action.first == my_piece_pos[0])
        {
            my_new_piece_pos = action.second;
        }
        if (!new_threats[my_new_piece_pos].empty())
        {
            auto tmp = std::remove(this->all_valid_action.begin(), this->all_valid_action.end(), action);
            this->all_valid_action.erase(tmp, this->all_valid_action.end());
        }
    }
    this->num_all_valid_action = this->all_valid_action.size();

    // avoid direct checkmate
    auto threats = this->state.getThreatBySide(this->state.myself);
    if (!threats[my_piece_pos[0]].empty())
    {
        for (const Action &action: this->all_valid_action)
        {
            auto new_state = this->state.getNextState(action);
            auto new_threats = new_state.getThreatBySide(this->state.myself);
            auto my_new_piece_pos = my_piece_pos[0];
            if (action.first == my_piece_pos[0])
            {
                my_new_piece_pos = action.second;
            }
            if (new_threats[my_new_piece_pos].empty())
            {
                new_actions.push_back(action);
            }
        }
        if (!new_actions.empty())
        {
            this->all_valid_action = new_actions;
            this->num_all_valid_action = new_actions.size();
        }
    }

    // whether consider horse, cannon, chariot?
}

void MCTSNode::init_quality_value()
{
    // whether and how to init quality value
    this->quality_value = 0.0f;
}

Action MCTSNode::randomChooseNextAction()
{
    if (this->all_valid_action.empty())
    {
        printf("all actions are expanded.");
        exit(-1);
    }
    else
    {
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(this->all_valid_action.begin(), this->all_valid_action.end(), g);
        auto action = this->all_valid_action[this->all_valid_action.size() - 1];
        this->all_valid_action.pop_back();
        return action;
    }
}

MCTSNode MCTSNode::expand()
{
    auto action = this->randomChooseNextAction();
    auto next_state = this->state.getNextState(action);
    MCTSNode next_node;
    next_node.setState(next_state);
    next_node.find_all_valid_action();
    next_node.init_quality_value();
    next_node.parent = this;
    this->children[action] = next_node;
    return next_node;

    // Python: if a in dict:
    // C++:
    // if (auto it = children.find(GameState()); it != children.end())
    // {
    //     auto gameState = it->first;
    //     auto a_huge_pair = it->second;
    // }
    // Python: a = dict[g]
    // C++
    // auto g = GameState();
    // auto a = children[g];
    // Python: dict[g] = a;
    // C++
    // children[g] = a;
}

MCTSNode MCTSNode::randomExpand()
{
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(this->all_valid_action.begin(), this->all_valid_action.end(), g);
    auto action = this->all_valid_action.at(0);
    auto next_state = this->state.getNextState(action);
    if (auto it = this->children.find(action); it != this->children.end())
    {
        auto next_node = this->children[action];
        return next_node;
    }
    else
    {
        MCTSNode next_node;
        next_node.setState(next_state);
        next_node.find_all_valid_action();
        next_node.init_quality_value();
        next_node.parent = this;
        this->children[action] = next_node;
        return next_node;
    }
}

float MCTSNode::calUCB(float c, MCTSNode child)
{

}

std::pair<Action, MCTSNode> MCTSNode::bestChild(bool is_exploration)
{
    float c = 0.0f;
    if (is_exploration)
    {
        c = 1 / sqrt(2.0);
    }
}
