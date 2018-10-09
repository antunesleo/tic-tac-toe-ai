import random


class MaxPlayersReached(Exception):
    pass


class MinPlayersNotReached(Exception):
    pass


class InvalidCell(Exception):
    pass


mark_translator = {
    'X': +1,
    'O': -1
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
                break
            self.toggle_current_player()

    def toggle_current_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1

    def check_if_games_ended(self):
        if self.board.check_for_consecutive_three_columns(mark_translator['X']):
            return True
        if self.board.check_for_consecutive_three_columns(mark_translator['O']):
            return True
        return False


class Player(object):

    @classmethod
    def create_a_new(cls, name, marker):
        raise NotImplemented

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
                cell_to_be_checked = input('Pass the x, y cell you want to check, ex: 1, 2:')
                self.current_match.board.mark_a_cell(cell_to_be_checked, self.marker)
                play_concluded = True
            except InvalidCell:
                pass


class MachinePlayer(Player):

    @classmethod
    def create_a_new(cls, name, marker):
        return cls(name, marker)

    def make_a_play(self):
        play_concluded = False
        while play_concluded is False:
            try:
                cell = (random.randint(0, 2), random.randint(0, 2))
                self.current_match.board.mark_a_cell(cell, self.marker)
                play_concluded = True
            except InvalidCell:
                pass


class Board(object):

    @classmethod
    def create_a_new(cls):
        return cls()

    def __init__(self):
        self.cells = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

    def mark_a_cell(self, cell, marker):
        if self.cells[cell[0]][cell[1]] == 0:
            self.cells[cell[0]][cell[1]] = mark_translator[marker]
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
            [self.cells[2][0], self.cells[1][1], self.cells[0][2]],
        ]
        if [cell_value, cell_value, cell_value] in win_board:
            return True
        return False

    def print_a_beautiful_board(self):
        print('/n')
        for index, line in enumerate(self.cells):
            if index == 0:
                print('_______________')
            line_to_be_printed = '| {} | {} | {} |'.format(line[0], line[1], line[2])
            print(line_to_be_printed)
            if index == 2:
                print('_______________')
        print('/n')


def run():
    match = Match.create_a_new()
    player1 = HumanPlayer.create_a_new('Breninho', 'X')
    player1.join_a_match(match)
    player2 = MachinePlayer.create_a_new('Dolores', 'O')
    player2.join_a_match(match)
    match.start_a_new_game()


if __name__ == "__main__":
    run()

