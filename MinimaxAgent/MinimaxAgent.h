//
// Created by boynextdoor on 12/27/22.
//

#ifndef MINIMAXAGENT_H
#define MINIMAXAGENT_H

#include "../include/agent.h"
#include "../include/data.h"
#include "../include/include.h"
#include "../include/utils.h"
#include <cstdio>

class MinimaxAgent : public Agent, public EvaluationMatrix {
public:
	MinimaxAgent(Player player, int depth) : Agent(player), EvaluationMatrix(), max_depth(depth) {}
    ~MinimaxAgent() override = default;
	Action step() override;

private:
	int max_depth;
	double maxValue(GameState state, int depth, Player player, double &alpha, double &beta);
	double minValue(GameState state, int depth, Player player, double &alpha, double &beta);
	double evaluationFunction(GameState state);
};

#endif// MINIMAXAGENT_H
