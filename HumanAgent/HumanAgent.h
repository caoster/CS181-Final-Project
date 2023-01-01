//
// Created by boynextdoor on 1/1/23.
//

#ifndef HUMANAGENT_H
#define HUMANAGENT_H

#include "../include/agent.h"
#include "../include/utils.h"
#include "../include/include.h"
#include <cstdio>

class HumanAgent : public Agent {
public:
	explicit HumanAgent(Player player) : Agent(player) {}
	~HumanAgent() override = default;
	Action step() override;
};

#endif//HUMANAGENT_H
