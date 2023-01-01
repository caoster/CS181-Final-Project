//
// Created by boynextdoor on 1/1/23.
//

#include "HumanAgent.h"

Action HumanAgent::step() {
	printf("Waiting for %s move...\n", direction == Player::Red ? "Red" : "Black");
	while (1) {
		int x1, y1, x2, y2;
		scanf("%d %d %d %d", &y1, &x1, &y2, &x2);
		Position from(x1, y1), to(x2, y2);
		if (direction == game->board()[from].getSide() && game->isValidMove(from, to)) {
			printf("Move from (%d, %d) to (%d, %d)\n", y1, x1, y2, x2);
			return Action(from, to);
		}
		printf("Invalid move, please try again\n");
	}
}