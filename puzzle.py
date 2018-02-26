#!/usr/bin/env python3

import re
from copy import copy
from sys import exit

class Puzzle:
    """Represents a puzzle instance. This will act as the state of our tree node."""

    # regex to match three or more consecutive devices
    DIGIT_REGEX = re.compile('(\\d)\\1{2,}')

    def __init__(self, quota, max_swaps, num_device_types, width, height, pool_height, bonus_rules, board):
        """Initializes a puzzle instance.
        
        Args:
            quota: Our target score.
            max_swaps: The maximum number of swaps allowed.
            num_device_types: The number of device types.
            width: The width of the board.
            height: The height of the board.
            pool_height: The height of our pool.
            bonus_rules: 1, 2, 3, or 0 if no bonus ruleset is used.
            board: Our initial board state.
        
        Returns:
            A fully initialized Puzzle object.
        """

        self.swaps = []         # holds tuples representing swap moves
        self.falling = False    # whether or not the board is in a falling state
        self.score = 0          # total number of devices removed
        self.replaced = 0       # devices removed per match-fall-replace cycle

        self.quota = int(quota)
        self.max_swaps = int(max_swaps)
        self.num_device_types = int(num_device_types)
        self.width = int(width)
        self.height = int(height)
        self.pool_height = int(pool_height)
        self.bonus_rules = int(bonus_rules)
        self.board = [row.split() for row in board]

    def copy(self):
        """Copies a puzzle instance.
        
        Returns:
            A deep copy of the puzzle object.
        """

        new = copy(self)
        new.swaps = self.swaps[:]
        new.board = [row[:] for row in self.board]

        return new

    def print(self):
        """Prints the board."""

        for i, row in enumerate(self.board):
            # print line of asterisks to separate pool from board
            if i == self.pool_height:
                print('-' * (len(row)*2-1))

            print((' ').join(row))

    def swap(self, dev1, dev2):
        """Swaps the location of two devices on the board.
        
        Args:
            dev1: The first device.
            dev2: The second device.
        """

        # unpack devices into x, y coordinates
        x1, y1 = dev1
        x2, y2 = dev2

        # perform swap using python magic
        self.board[y1][x1], self.board[y2][x2] = self.board[y2][x2], self.board[y1][x1]

    def get_match(self, is_row, row_col, x_y, offset=0):
        """Given a row or column, perform a regex match using backreferences to
        determine if a series of matching devices exists.

        Args:
            is_row: True if matching a row, False if column.
            row_col: The row or column to match.
            x_y: The x or y constant that devices in the row/column share.
            offset: Necessary to compensate for pool height if we're searching
                a row, since we don't want to match rows inside the pool.
        
        Returns:
            A list of locations of matching devices within the row or column.
        """

        # perform regex match on row/column
        m = Puzzle.DIGIT_REGEX.search(''.join(row_col))

        if m:
            # if we're searching a row, loop over every matching x value
            if is_row:
                return [(x, x_y+offset) for x in range(m.start(), m.end())]
            # if we're searching a column, loop over every matching y value
            else:
                return [(x_y, y+offset) for y in range(m.start(), m.end())]
        # if no match found
        else:
            return []

    def get_matches(self, dev1, dev2):
        """Return just the matches that occur near the swapped devices. After a
        horizontal swap, matches can exist in each of the two columns that the
        devices are in and the one row that the devices share.

        Args:
            dev1: The first device.
            dev2: The second device.

        Returns:
            A list of locations of matching devices on the board.
        """

        matches = []

        # horizontal swap
        if dev1[0] != dev2[0]:
            x1, x2 = dev1[0], dev2[0]
            y = dev1[1]

            matches += self.get_match(True, self.board[y], y)

            col = [row[x1] for row in self.board[self.pool_height:]]
            matches += self.get_match(False, col, x1, self.pool_height)

            col = [row[x2] for row in self.board[self.pool_height:]]
            matches += self.get_match(False, col, x2, self.pool_height)
        # vertical swap
        else: 
            x = dev1[0]
            y1, y2 = dev1[1], dev2[1]

            matches += self.get_match(True, self.board[y1], y1)
            matches += self.get_match(True, self.board[y2], y2)

            col = [row[x] for row in self.board[self.pool_height:]]
            matches += self.get_match(False, col, x, self.pool_height)

        return matches

    def get_all_matches(self):
        """Returns all matches. A match can be defined as a horizontal or
        vertical series of three or more of the same device.

        Returns:
            A list of locations of matching devices on the board.
        """

        matches = []

        # check horizontal matches (pool excluded)
        for y, row in enumerate(self.board[self.pool_height:]):
            matches += self.get_match(True, row, y, self.pool_height)

        # check vertical matches the same way by transposing the list
        for x, col in enumerate(zip(*self.board[self.pool_height:])):
            matches += self.get_match(False, col, x, self.pool_height)
            
        return matches

    def remove_matches(self, matches):
        """Remove matches from the board. Begins a falling cycle.
        
        Args:
            matches: A list of locations of matches to be removed.
        """

        self.replaced = 0

        # end recursion if there are no more matches
        if not matches:
            return

        for x, y in matches:
            self.score += 1
            self.board[y][x] = 'E'
            self.falling = True

        while self.falling:
            self.simulate_falling()

        self.remove_matches(self.get_all_matches())

    def simulate_falling(self):
        """Account for devices falling into empty spaces on the board."""

        self.falling = False

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'E':
                    self.falling = True
                    self.replace_device(x, y)

    def get_new_device(self, x):
        """Formula for replacing devices at top of pool.
        
        Args:
            x: The x coordinate of the device.
        
        Returns:
            A string label of the new device.
        """

        return str((int(self.board[1][x]) + x + self.replaced) % self.num_device_types + 1)

    def replace_device(self, x, y):
        """Replace device either by falling or using the replacement formula.
        
        Args:
            x: The x coordinate of the device.
            y: The y coordinate of the device.
        """

        # if top row, replace via formula
        if y == 0:
            self.replaced += 1
            self.board[y][x] = self.get_new_device(x)
        else:
            self.swap((x, y), (x, y - 1))

            # if replaced by falling, immediately replace where it fell from
            self.replace_device(x, y - 1)

    def get_valid_moves(self):
        """Simulate swaps and return only those that would result in a match.
        
        Returns:
            A list of device locations. Swapping any of these will result in at
            least one match.
        """

        moves = []

        # check horizontal swaps
        for y in range(self.pool_height, self.height):
            for x in range(self.width - 1):
                self.swap((x, y), (x + 1, y))

                if self.get_matches((x, y), (x+1, y)):
                    moves.append(((x, y), (x + 1, y)))

                # undo swap
                self.swap((x, y), (x + 1, y))

        # check vertical swaps
        for y in range(self.pool_height, self.height - 1):
            for x in range(self.width):
                self.swap((x, y), (x, y + 1))

                if self.get_matches((x, y), (x, y+1)):
                    moves.append(((x, y), (x, y + 1)))

                # undo swap
                self.swap((x, y), (x, y + 1))

        return moves

    def __eq__(self, other):
        """Overload equal operator to define equality for puzzle instances.

        Args:
            other: The other puzzle instance.

        Returns:
            True if the board state and score are equal, False otherwise.
        """

        return self.board == other.board and self.score == other.score
