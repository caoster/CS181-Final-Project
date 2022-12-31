#include "qlearningAgent.h"
#include <algorithm>

Action QlearningAgent::step() {
    Board board = game->getGameState().board;
    Action action = getAction(board);
    last_action = action;
    last_state = game->getGameState();
    myreward = getReward(last_state, last_action, direction);
    GameState nextstate = last_state.getNextState(last_action);
    nextstate.swapDirection();
    Player winner = nextstate.getWinner();
    if (winner == direction) {
        // hash for q_value
        float old_estimate = q_value[{board, last_action}];
        q_value.set({board, last_action}, (1 - myalpha) * old_estimate + myalpha * myreward);
    }
    return action;
}

Counter QlearningAgent::getQValueBoard() {
    return q_value;
}

void QlearningAgent::update(Action action) {
    Board lastboard = last_state.board;
    float old_estimate = getQValue(lastboard, last_action);
    Board board = game->getGameState().board;
    Action best_action = computeActionFromQValues(board);
    float max_q = getQValue(board, best_action);
    Player opponent = direction.reverse();
    float opponentReward = getReward(game->getGameState(), action, opponent);
    float reward = myreward - opponentReward;
    float sample = reward + mydiscount * max_q;
    // hash for q_value
    q_value.set({lastboard, last_action}, (1 - myalpha) * old_estimate + myalpha * sample);
}

float QlearningAgent::getQValue(const Board& current_board, Action action) {
    return q_value[{current_board, action}];
}

Action QlearningAgent::computeActionFromQValues(Board current_board) {
    std::vector<float> q_list;
    auto all_actions = game->getGameState().getLegalActionsBySide(direction);
    for (auto &action: all_actions) {
        float qvalue = getQValue(current_board, action);
        q_list.push_back(qvalue);
    }
    float max_q = *max_element(q_list.begin(), q_list.end());
    // to be finished
    // max_index = []
    // for i in range(len(q_list)):
    //     if q_list[i] == max_q:
    //         max_index.append(i)
    // index = random.choice(max_index)
    // return self.game.getLegalActionsBySide(self.direction)[index]
}

float QlearningAgent::getReward(GameState state, Action action, Player player) {

}

bool QlearningAgent::flipcoin() {

}

Action QlearningAgent::getAction(Board board) {

}
