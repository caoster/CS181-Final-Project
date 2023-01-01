//
// Created by boynextdoor on 1/1/23.
//

#include "HumanAgent.h"

Action HumanAgent::step() {
	printf("Waiting for %s move...\n", direction == Player::Red ? "Red" : "Black");
	while (true) {
		int x1, y1, x2, y2;
		std::cin >> x1 >> y1 >> x2 >> y2;
		Position from(x1, y1), to(x2, y2);
		if (direction == game->board()[from].getSide() && game->isValidMove(from, to)) {
			fprintf(stdout, "Move from (%d, %d) to (%d, %d)\n", y1, x1, y2, x2);
			return {from, to};
		}
		fprintf(stdout, "Invalid move, please try again\n");
	}
}