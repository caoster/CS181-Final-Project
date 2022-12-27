//
// Created by boynextdoor on 12/27/22.
//

#ifndef CS181_FINAL_PROJECT_CPP_MINIMAXAGENT_H
#define CS181_FINAL_PROJECT_CPP_MINIMAXAGENT_H

#include "../include/include.h"
#include "../include/agent.h"
#include "../include/data.h"
#include "../include/utils.h"
#include <cstdio>

class MinimaxAgent : public Agent {
public:
	MinimaxAgent(Player player, int depth) : Agent(player), max_depth(depth) {}
	Action step() override;

private:
	int max_depth;
	int index;
	double maxValue(int depth, Player player, double alpha, double beta);
	double minValue(int depth, Player player, double alpha, double beta);
};

#endif// CS181_FINAL_PROJECT_CPP_MINIMAXAGENT_H
