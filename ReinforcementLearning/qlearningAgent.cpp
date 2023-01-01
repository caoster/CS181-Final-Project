#include "qlearningAgent.h"
#include <algorithm>
#include <random>

Action QlearningAgent::step()
{
    Board board = game->getGameState().board;
    Action action = getAction(board);
    last_action = action;
    last_state = game->getGameState();
    myreward = getReward(last_state, last_action, direction);
    GameState nextstate = last_state.getNextState(last_action);
    nextstate.swapDirection();
    Player winner = nextstate.getWinner();
    if (winner == direction)
    {
        float old_estimate = q_value[{board, last_action}];
        q_value.set({board, last_action}, (1 - myalpha) * old_estimate + myalpha * myreward);
    }
    return action;
}

Counter QlearningAgent::getQValueBoard()
{
    return q_value;
}

void QlearningAgent::update(Action action)
{
    Board lastboard = last_state.board;
    float old_estimate = getQValue(lastboard, last_action);
    Board board = game->getGameState().board;
    Action best_action = computeActionFromQValues(board);
    float max_q = getQValue(board, best_action);
    Player opponent = direction.reverse();
    float opponentReward = getReward(game->getGameState(), action, opponent);
    float reward = myreward - opponentReward;
    float sample = reward + mydiscount * max_q;
    q_value.set({lastboard, last_action}, (1 - myalpha) * old_estimate + myalpha * sample);
}

float QlearningAgent::getQValue(const Board &current_board, Action action)
{
    return q_value[{current_board, action}];
}

Action QlearningAgent::computeActionFromQValues(Board current_board)
{
    std::vector<float> q_list;
    auto all_actions = game->getGameState().getLegalActionsBySide(direction);
    for (auto &action : all_actions)
    {
        float qvalue = getQValue(current_board, action);
        q_list.push_back(qvalue);
    }
    float max_q = *max_element(q_list.begin(), q_list.end());
    std::vector<unsigned int> max_index;

    for (unsigned int i = 0; i < q_list.size(); i++)
    {
        if (q_list[i] == max_q)
        {
            max_index.push_back(i);
        }
    }
    auto len = max_index.size();
    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> dist(0, len);
    unsigned int index = dist(rng);
    return all_actions[index];
}

float QlearningAgent::getReward(GameState state, Action action, Player player)
{
    float score = 0;
    GameState nextstate = last_state.getNextState(last_action);
    nextstate.swapDirection();
    Player winner = nextstate.getWinner();
    if (winner == player)
    {
        score = 1000000;
    }
    else if (winner == player.reverse())
    {
        score = -1000000;
    }
    else
    {
        std::vector<Position> myPiece = state.getSide(player);
        for (Position &piece : myPiece)
        {
            auto x = piece.first;
            auto y = piece.second;
            Piece pieceType = state[piece];
            score += (pieceValue[pieceType.value()] * pieceScore[pieceType.value()][x][y]);
        }
        Piece eatenPieceType = state[action.second];
        switch (eatenPieceType.value())
        {
        case Piece::NoneType:
        {
            break;
        }
        case Piece::BSoldier:
        {
            score += 1;
            break;
        }
        case Piece::RSoldier:
        {
            score += 1;
            break;
        }
        case Piece::BAdvisor:
        {
            score += 2;
            break;
        }
        case Piece::RAdvisor:
        {
            score += 2;
            break;
        }
        case Piece::BElephant:
        {
            score += 2;
            break;
        }
        case Piece::RElephant:
        {
            score += 2;
            break;
        }
        case Piece::BHorse:
        {
            score += 4;
            break;
        }
        case Piece::RHorse:
        {
            score += 4;
            break;
        }
        case Piece::BCannon:
        {
            score += float(4.5);
            break;
        }
        case Piece::RCannon:
        {
            score += float(4.5);
            break;
        }
        case Piece::BChariot:
        {
            score += 9;
            break;
        }
        case Piece::RChariot:
        {
            score += 9;
            break;
        }
        case Piece::BGeneral:
        {
            break;
        }
        case Piece::RGeneral:
        {
            break;
        }
        }
    }
    return score;
}

bool QlearningAgent::flipcoin()
{
    std::random_device dev;
    std::mt19937 rng(dev());
    std::uniform_int_distribution<std::mt19937::result_type> dist(0, 100);
    float r = dist(rng) / float(100.0);
    return r < myepsilon;
}

Action QlearningAgent::getAction(Board board)
{
    std::vector<Action> all_actions = game->getGameState().getLegalActionsBySide(direction);
    Action action;
    if (flipcoin())
    {
        size_t len = all_actions.size();
        std::random_device dev;
        std::mt19937 rng(dev());
        std::uniform_int_distribution<std::mt19937::result_type> dist(0, len);
        action = all_actions[dist(rng)];
    }
    else
    {
        action = computeActionFromQValues(board);
    }
    return action;
}
