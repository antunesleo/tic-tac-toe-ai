from numpy import numpy as np


class MaxPlayersReached(Exception):
    pass


class MinPlayersNotReached(Exception):
    pass


class InvalidCell(Exception):
    pass


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
            if self.check_if_games_ended():
                break
            self.toggle_current_player()

    def toggle_current_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1

    def mark_a_cell_on_board_for_a_player(self, player, cell):
        if player in self.players:
            self.board.mark_a_cell(cell, player.marker)

    def check_if_games_ended(self):
        pass


class Player(object):

    @classmethod
    def create_a_new(cls, name):
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
    def create_a_new(cls, name):
        return cls(name)

    def make_a_play(self):
        cell_to_be_checked = input('Pass the x, y cell you want to check, ex: 1, 2:')
        if any(item > 2 or item < 0 for item in cell_to_be_checked):
            raise InvalidCell('Cannot make this play because the cell given does not exists')
        self.current_match.mark_a_cell_on_board_for_a_player(cell_to_be_checked, self)


class MachinePlayer(object):

    @classmethod
    def create_a_new(cls, name):
        return cls(name)

    def make_a_play(self):
        pass


class Board(object):

    @classmethod
    def create_a_new(cls):
        return cls()

    def __init__(self):
        self.cells = np.array(
            [None, None, None],
            [None, None, None],
            [None, None, None])

    def mark_a_cell(self, cell, marker):
        self.cells.item_set(cell, marker)


def start_menu():
    pass


if __name__ == "__main__":
    start_menu()

