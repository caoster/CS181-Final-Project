//
// Created by boynextdoor on 12/27/22.
//

#include "MinimaxAgent.h"


Action MinimaxAgent::step() {
	printf("Minimax starts thinking...\n");
	GameState gameState = game->getGameState();
	int totalPieces = gameState.getSide(direction).size() + gameState.getSide(Player::reverse(direction)).size();
	float fraction = 1 - ((float) totalPieces / 32.f);
	max_depth = 3 + (int) (fraction * 4);
	std::vector<Action> legalMoves = gameState.getLegalActionsBySide(direction);
	Action bestAction;
	double bestValue = -1e9;
	double alpha = -1e9;
	double beta = 1e9;
	for (const auto &action : legalMoves) {
		double value = minValue(gameState.getNextState(action), 1, Player::reverse(direction), alpha, beta);
		if (value > bestValue) {
			bestValue = value;
			bestAction = action;
		}
		if (value > beta)
			break;
		alpha = std::max(alpha, value);
	}
	printf("Minimax finished thinking...\n");
	return bestAction;
}

double MinimaxAgent::evaluationFunction(const GameState &state) {
	state.swapDirection();
	Player winner = state.getWinner();
	state.swapDirection();
	if (winner == direction)
		return 1e6;
	else if (winner == Player::reverse(direction))
		return -1e6;
	std::vector<Position> myPiece = state.getSide(direction);
	std::vector<Position> enemyPiece = state.getSide(Player::reverse(direction));
	double myScore = 0;
	double enemyScore = 0;
	std::unordered_map<Position, std::vector<Position>> myThreat = state.getThreatBySide(direction);
	for (auto piece: myPiece){
		size_t x = piece.first;
		size_t y = piece.second;
		Piece myPieceType = state[x][y];
		myScore += pieceValue[myPieceType] * pieceScore[myPieceType][x][y]
		myScore *= 0.1;

		std::vector<Position> attackPosition = state.getRange(piece);
		int flexibility = 0;
		for (auto &position: attackPosition){
			size_t x = position.first;
			size_t y = position.second;
			Piece pieceType = state[x][y];
			if (pieceType == Piece::NoneType)
				flexibility++;
		}
		myScore += flexibility * pieceFlexibility[myPieceType];
		myScore -= pieceValue[myPieceType] * myThreat[piece].size();
	}

}

double MinimaxAgent::maxValue(GameState state, int depth, Player player, double alpha, double beta) {
	if (depth == max_depth * 2 || state.isMatchOver())
		return evaluationFunction(state);
	double value = -1e9;
	std::vector<Action> legalActions = state.getLegalActionsBySide(player);
    for (auto &action: legalActions){
		value = std::max(value, minValue(state.getNextState(action), depth + 1, Player::reverse(player), alpha, beta));
		if (value > beta)
			return value;
		alpha = std::max(alpha, value);
	}
	return value;
}

double MinimaxAgent::minValue(GameState state, int depth, Player player, double alpha, double beta) {
	if (depth == max_depth * 2 || state.isMatchOver())
		return evaluationFunction(state);
	double value = 1e9;
	std::vector<Action> legalActions = state.getLegalActionsBySide(player);
	for (auto &action: legalActions){
		value = std::min(value, maxValue(state.getNextState(action), depth + 1, Player::reverse(player), alpha, beta));
		if (value < alpha)
			return value;
		beta = std::min(beta, value);
	}
	return value;
}