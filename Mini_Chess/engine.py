class GameState():

    def __init__(self) -> None:

        self.board = [
            ['b_R', 'b_Kn', 'b_B', 'b_Q', 'b_K'],
            ['b_P', 'b_P', 'b_P', 'b_P', 'b_P'],
            ['--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--'],
            ['w_P', 'w_P', 'w_P', 'w_P', 'w_P'],
            ['w_R', 'w_Kn', 'w_B', 'w_Q', 'w_K'],
        ]

        self.whiteToMove = True
        self.movelog = []
