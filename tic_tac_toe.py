import copy
import random
from math import inf as infinity
import ai_services


class MaxPlayersReached(Exception):
    pass


class MinPlayersNotReached(Exception):
    pass


class InvalidCell(Exception):
    pass


MARK_TRANSLATOR = {
    'X': -1,
    'O': +1
}


class Match(object):

    @classmethod
    def create_a_new(cls):
        return cls()

    def __init__(self):
        self.players = []
        self.board = Board.create_a_new()
        self.current_player = None
        self.winner = None

    @property
    def player1(self):
        return self.players[0]

    @property
    def player2(self):
        return self.players[1]

    def add_a_new_player(self, player):
        if len(self.players) > 1:
            raise MaxPlayersReached('Cannot add the player to the match because the max players was reached')
        self.players.append(player)

    def start_a_new_game(self):
        if len(self.players) < 2:
            raise MinPlayersNotReached('Cannot start a match because we need at least two players')

        self.current_player = self.player1

        while self.winner is None:
            self.current_player.make_a_play()
            self.board.print_a_beautiful_board()
            if self.check_if_games_ended():
                print('THE GAME IS OVER')
                break
            self.toggle_current_player()

    def toggle_current_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1

    def check_if_games_ended(self):
        if self.board.check_for_consecutive_three_columns(MARK_TRANSLATOR['X']):
            return True
        if self.board.check_for_consecutive_three_columns(MARK_TRANSLATOR['O']):
            return True
        return False

    def who_wins_x_or_o(self):
        if self.board.check_for_consecutive_three_columns(MARK_TRANSLATOR['X']):
            return MARK_TRANSLATOR['X']
        if self.board.check_for_consecutive_three_columns(MARK_TRANSLATOR['O']):
            return MARK_TRANSLATOR['O']
        return 0


class Player(object):
    MOVE_DICT = {
        '1': (0, 0),
        '2': (0, 1),
        '3': (0, 2),
        '4': (1, 0),
        '5': (1, 1),
        '6': (1, 2),
        '7': (2, 0),
        '8': (2, 1),
        '9': (2, 2),
    }


    @classmethod
    def create_a_new(cls, name, marker):
        raise NotImplemented

    @property
    def marker_value(self):
        return MARK_TRANSLATOR[self.marker]

    def __init__(self, name, marker):
        self.name = name
        self.current_match = None
        self.marker = marker

    def join_a_match(self, match):
        match.add_a_new_player(self)
        self.current_match = match


class HumanPlayer(Player):

    @classmethod
    def create_a_new(cls, name, marker):
        return cls(name, marker)

    def make_a_play(self):
        play_concluded = False

        while play_concluded is False:
            try:
                input_number = input('Pass type a number between 1 and 9:  ')
                cell_to_be_checked = self.MOVE_DICT[input_number]
                self.current_match.board.mark_a_cell(cell_to_be_checked, self.marker)
                play_concluded = True
            except InvalidCell:
                pass


class MachinePlayer(Player):

    @classmethod
    def create_a_new(cls, name, marker):
        return cls(name, marker)

    def __init__(self, name, marker):
        super().__init__(name, marker)

    def make_a_play(self):
        play_concluded = False
        while play_concluded is False:
            try:
                depth = len(self.current_match.board.empty_cells)
                simulation_match = copy.deepcopy(self.current_match)
                best_move_and_winner = ai_services.MinimaxService.minimax_tic_tac_toe(simulation_match, depth, self.marker_value)
                cell = best_move_and_winner[:-1]
                self.current_match.board.mark_a_cell(cell, self.marker)
                play_concluded = True
            except InvalidCell:
                pass


class Board(object):

    @classmethod
    def create_a_new(cls):
        return cls()

    @classmethod
    def find_mark_by_value(cls, value):
        for mark, current_value in MARK_TRANSLATOR.items():
            if value == current_value:
                return mark
        return None

    def __init__(self):
        self.cells = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

    @property
    def empty_cells(self):
        cells = []

        for x, row in enumerate(self.cells):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])
        return cells

    def mark_a_cell(self, cell, marker):
        if self.cells[cell[0]][cell[1]] == 0:
            self.cells[cell[0]][cell[1]] = MARK_TRANSLATOR[marker]
        else:
            raise InvalidCell('Cannot make this play because the cell given does not exists')
    
    def check_for_consecutive_three_columns(self, cell_value):
        win_board = [
            [self.cells[0][0], self.cells[0][1], self.cells[0][2]],
            [self.cells[1][0], self.cells[1][1], self.cells[1][2]],
            [self.cells[2][0], self.cells[2][1], self.cells[2][2]],
            [self.cells[0][0], self.cells[1][0], self.cells[2][0]],
            [self.cells[0][1], self.cells[1][1], self.cells[2][1]],
            [self.cells[0][2], self.cells[1][2], self.cells[2][2]],
            [self.cells[0][0], self.cells[1][1], self.cells[2][2]],
            [self.cells[0][0], self.cells[1][1], self.cells[2][2]],
            [self.cells[2][0], self.cells[1][1], self.cells[0][2]]
        ]
        if [cell_value, cell_value, cell_value] in win_board:
            return True
        return False

    def print_a_beautiful_board(self):
        print('\n')
        for index, line in enumerate(self.cells):
            if index == 0:
                print('_______________')
            first_cell = self.find_mark_by_value(line[0])
            first_cell = ' ' if first_cell is None else first_cell
            second_cell = self.find_mark_by_value(line[1])
            second_cell = ' ' if second_cell is None else second_cell
            third_cell = self.find_mark_by_value(line[2])
            third_cell = ' ' if third_cell is None else third_cell
            line_to_be_printed = '| {} | {} | {} |'.format(first_cell, second_cell, third_cell)
            print(line_to_be_printed)
            if index == 2:
                print('--------------')
        print('\n')


def run():
    match = Match.create_a_new()
    player1 = HumanPlayer.create_a_new('Breninho', 'X')
    player1.join_a_match(match)
    player2 = MachinePlayer.create_a_new('Dolores', 'O')
    player2.join_a_match(match)
    match.start_a_new_game()


if __name__ == "__main__":
    run()
