//
// Created by nick on 22-12-31.
//

#include "MCTSAgent.h"

bool MCTSNode::isAllExpanded() {
    return all_valid_action.empty();
}

void MCTSNode::setState(const GameState &other_state) {
    this->state = other_state;
}

//void MCTSNode::setParent(std::shared_ptr<MCTSNode> other_parent) {
//    this->parent = std::move(other_parent);
//}

void MCTSNode::setVisitTime(int other_visit_time) {
    this->visit_time = other_visit_time;
}

void MCTSNode::setQualityValue(float other_quality_value) {
    this->quality_value = other_quality_value;
}

void MCTSNode::find_all_valid_action() {
    this->all_valid_action = this->state.getLegalActionsBySide(this->state.myself);
    std::vector<Action> new_actions;
    Piece my_general = Piece::RGeneral;
    Piece other_general = Piece::BGeneral;
    Player other = this->state.myself.reverse();
    if (this->state.myself == Player::Black) {
        my_general = Piece::BGeneral;
        other_general = Piece::RGeneral;
    }
    auto my_piece_pos = this->state.findPiece(my_general);
    if (my_piece_pos.empty()) {
        this->all_valid_action.clear();
        this->num_all_valid_action = 0;
        return;
    }
    auto general_neighbour = this->state.getRange(my_piece_pos[0]);
    auto attack = this->state.getThreatBySide(other);
    auto other_piece_pos = this->state.findPiece(other_general);

    // checkmate opponent
    if (!other_piece_pos.empty() && !attack[other_piece_pos[0]].empty()) {
        for (const Position &pos: attack[other_piece_pos[0]]) {
            new_actions.emplace_back(pos, other_piece_pos[0]);
        }
        this->all_valid_action = new_actions;
        this->num_all_valid_action = this->all_valid_action.size();
        return;
    }

    // avoid action lead to checkmate
    for (const Action &action: this->all_valid_action) {
        auto new_state = this->state.getNextState(action);
        auto new_threats = new_state.getThreatBySide(this->state.myself);
        auto my_new_piece_pos = my_piece_pos[0];
        if (action.first == my_piece_pos[0]) {
            my_new_piece_pos = action.second;
        }
        if (!new_threats[my_new_piece_pos].empty()) {
            auto tmp = std::remove(this->all_valid_action.begin(), this->all_valid_action.end(), action);
            this->all_valid_action.erase(tmp, this->all_valid_action.end());
        }
    }
    this->num_all_valid_action = this->all_valid_action.size();

    // avoid direct checkmate
    auto threats = this->state.getThreatBySide(this->state.myself);
    if (!threats[my_piece_pos[0]].empty()) {
        for (const Action &action: this->all_valid_action) {
            auto new_state = this->state.getNextState(action);
            auto new_threats = new_state.getThreatBySide(this->state.myself);
            auto my_new_piece_pos = my_piece_pos[0];
            if (action.first == my_piece_pos[0]) {
                my_new_piece_pos = action.second;
            }
            if (new_threats[my_new_piece_pos].empty()) {
                new_actions.push_back(action);
            }
        }
        if (!new_actions.empty()) {
            this->all_valid_action = new_actions;
            this->num_all_valid_action = new_actions.size();
        }
    }

    // whether consider horse, cannon, chariot?
}

void MCTSNode::init_quality_value() {
    // whether and how to init quality value
    this->quality_value = 0.0f;
}

Action MCTSNode::randomChooseNextAction() {
    if (this->all_valid_action.empty()) {
        printf("all actions are expanded.\n");
        exit(-1);
    } else {
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(this->all_valid_action.begin(), this->all_valid_action.end(), g);
        auto action = this->all_valid_action[this->all_valid_action.size() - 1];
        this->all_valid_action.pop_back();
        return action;
    }
}

std::shared_ptr<MCTSNode> MCTSNode::expand() {
    auto action = this->randomChooseNextAction();
    auto next_state = this->state.getNextState(action);
    std::shared_ptr<MCTSNode> next_node = std::make_shared<MCTSNode>();
    next_node->setState(next_state);
    next_node->find_all_valid_action();
    next_node->init_quality_value();
    next_node->parent = this;
    this->children[action] = next_node;
    return next_node;
}

std::shared_ptr<MCTSNode> MCTSNode::randomExpand() {
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(this->all_valid_action.begin(), this->all_valid_action.end(), g);
    auto action = this->all_valid_action.at(0);
    auto next_state = this->state.getNextState(action);
    if (auto it = this->children.find(action); it != this->children.end()) {
        auto next_node = this->children[action];
        return next_node;
    } else {
        std::shared_ptr<MCTSNode> next_node = std::make_shared<MCTSNode>();
        next_node->setState(next_state);
        next_node->find_all_valid_action();
        next_node->init_quality_value();
        next_node->parent = this;
        this->children[action] = next_node;
        return next_node;
    }
}

float MCTSNode::calUCB(float c, const std::shared_ptr<MCTSNode> &child) const {
    float UCB = 0.0f;
    if (child->visit_time != 0) {
        UCB = child->quality_value / (float) child->visit_time +
              c * sqrtf(2 * logf((float) this->visit_time) / (float) child->visit_time);
    }
    return UCB;
}

std::pair<Action, std::shared_ptr<MCTSNode>> MCTSNode::bestChild(bool is_exploration) {
    float c = 0.0f;
    float best_score = -1e9;
    Action best_action;
    std::shared_ptr<MCTSNode> best_child;
    if (is_exploration) {
        c = 1 / sqrtf(2.0f);
    }
    for (const auto &i: this->children) {
        float tmp = this->calUCB(c, i.second);
        if (tmp > best_score) {
            best_score = tmp;
            best_action = i.first;
        }
    }
    best_child = this->children[best_action];
    if (!is_exploration) {
        printf("choose child node with visit time %d\n", best_child->visit_time);
    }
    return {best_action, best_child};
}

float MCTSNode::calRewardFromState(Player direction) {
    auto winner = this->state.getWinner();
    if (winner == direction) {
        return 1.0f;
    } else {
        return -1.0f;
    }
    //    return 0;
}

MCTSAgent::MCTSAgent(Player player, int budget) : Agent(player), computation_budget(budget) {
    this->root = std::make_shared<MCTSNode>();
}

std::shared_ptr<MCTSNode> MCTSAgent::treePolicy(std::shared_ptr<MCTSNode> node) {
    if (!node->state.isMatchOver()) {
        if (node->isAllExpanded()) {
            node = node->bestChild(true).second;
        } else {
            node = node->expand();
        }
    }
    return node;
}

std::pair<std::shared_ptr<MCTSNode>, float> MCTSAgent::defaultPolicy(std::shared_ptr<MCTSNode> node) {
    int r = 0;
    while (!node->state.isMatchOver()) {
        node = node->randomExpand();
        r++;
        if (r > 200) {
            this->tie++;
            return {node, 0};
        }
    }
    node->state.swapDirection();
    float reward = node->calRewardFromState(this->direction);
    node->state.swapDirection();
    return {node, reward};
}

void MCTSAgent::backup(const std::shared_ptr<MCTSNode> &node, float reward) {
    MCTSNode* track = node.get();
    while (track->parent != nullptr) {
        track->visit_time++;
        if (track->state.myself == this->direction) {
            track->quality_value -= reward;
        } else {
            track->quality_value += reward;
        }
        track = track->parent;
    }
    track->visit_time++;
}

Action MCTSAgent::step() {
    printf("MCTS starts thinking.\n");
    auto new_game_state = this->game->getGameState();
    for (auto &iter: this->root->children) {
        if (iter.second->state == new_game_state) {
            this->root = iter.second;
            for (auto &i: this->root->children) {
                printf("erase action.\n");
                auto tmp = std::remove(this->root->all_valid_action.begin(), this->root->all_valid_action.end(),
                                       i.first);
                this->root->all_valid_action.erase(tmp, this->root->all_valid_action.end());
            }
            break;
        }
    }
    if (this->root->parent == nullptr) {
        this->root = std::make_shared<MCTSNode>();
        this->root->setState(new_game_state);
        this->root->init_quality_value();
        this->root->find_all_valid_action();
        this->root->state.myself = this->direction;
    }
    this->root->parent = nullptr;
    this->tie = 0;
    for (int i = 0; i < this->computation_budget; ++i) {
        auto expand_node = this->treePolicy(this->root);
        auto tmp = this->defaultPolicy(expand_node);
        this->backup(tmp.first, tmp.second);
    }
    printf("%d\n", this->tie);
    for (const auto &i: this->root->children) {
        printf("%d: %f\n", i.second->visit_time, i.second->quality_value / (float) i.second->visit_time);
    }
    auto result = this->root->bestChild(false);
    this->root = result.second;
    this->root->parent = nullptr;
    printf("MCTS stops thinking.\n");
    return result.first;
}
