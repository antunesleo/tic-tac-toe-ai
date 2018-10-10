from math import inf as infinity


class MinimaxService(object):

    @classmethod
    def minimax_tic_tac_toe(cls, simulation_match, depth, marker_value):
            if marker_value == 1:
                best = [-1, -1, -infinity]
            else:
                best = [-1, -1, +infinity]

            if depth == 0 or simulation_match.check_if_games_ended():
                score = simulation_match.who_wins_x_or_o()
                return [-1, -1, score]

            for cell in simulation_match.board.empty_cells:
                x, y = cell[0], cell[1]
                simulation_match.board.cells[x][y] = marker_value
                score = cls.minimax_tic_tac_toe(simulation_match, depth - 1, -marker_value)
                simulation_match.board.cells[x][y] = 0
                score[0], score[1] = x, y

                if marker_value == 1:
                    if score[2] > best[2]:
                        best = score
                else:
                    if score[2] < best[2]:
                        best = score

            return best