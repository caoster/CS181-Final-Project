#include "qlearningAgent.h"

Action QlearningAgent::step()
{
    std::vector<std::vector<Piece>> board = game->getGameState().board;
    Action action = getAction(board);
    last_action = action;
    last_state = game->getGameState();
    myreward = getReward(last_state, last_action, direction);
    GameState nextstate = last_state.getNextState(last_action);
    nextstate.swapDirection();
    Player winner = nextstate.getWinner();
    if (winner == direction)
    {
        // hash for q_value
        float old_estimate = q_value[(board, last_action)];
        q_value[(board, last_action)] = (1 - myalpha) * old_estimate + myalpha * myreward
    }
    return action;
}

Counter QlearningAgent::getQValueBoard()
{
    return q_value;
}

void QlearningAgent::update(Action action)
{
    float old_estimate = getQValue(last_state, self.last_action)
    # compute max Q
    state = tuple(tuple(x) for x in self.game.getGameState().getBoard())
    # best_action=self.computeActionFromQValues(self.game)
    best_action = self.computeActionFromQValues(state)
    # max_q = self.getQValue(self.game, best_action)
    max_q = self.getQValue(state, best_action)
    opponentReward = self.getReward(self.game.getGameState(), current_action, Player.reverse(self.playerSide))
    reward = self.myreward - opponentReward
    sample = reward + self.discount * max_q
    # update the q_value
    laststate = tuple(tuple(x) for x in self.last_state.getBoard())
    self.q_value[(laststate, self.last_action)] = (1 - self.alpha) * old_estimate + self.alpha * sample

}

float QlearningAgent::getQValue(current_board, Action action)
{
}
Action QlearningAgent::computeActionFromQValues(current_board)
{
}
float QlearningAgent::getReward(GameState state, Action action, Player player)
{
}
bool QlearningAgent::flipcoin()
{
}
Action QlearningAgent::getAction(std::vector<std::vector<Piece>> board)
{
}
