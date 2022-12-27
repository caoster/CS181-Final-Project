#ifndef RANDOMAGENT_H
#define RANDOMAGENT_H

#include "../include/include.h"
#include "../include/agent.h"


class RandomAgent : public Agent {
public:
    explicit RandomAgent(Player player) : Agent(player) {}

    Action step() override;

private:
    std::default_random_engine randomEngine{std::random_device()()};
};

#endif //RANDOMAGENT_H
