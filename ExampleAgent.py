from agent import Agent


class ExampleAgent(Agent):
    def __init__(self, direction: bool):
        super().__init__(direction)

    def step(self) -> tuple[tuple[int, int], tuple[int, int]]:
        # TODO: implement basic step()
        pass
