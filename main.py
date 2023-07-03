"""
Copy of Thorsten Gimmler's 'No Thanks' for strategy analysis

Rules:
https://www.amigo.games/content/ap/rule/18414--014-NoThanks-Manual_001-LAYOUT.pdf
"""

import math
from typing import List
from players import *


class IllPassGame:
    default_chip_count = 7
    forced_chips_per_player = None
    burn_num = 9

    players = []
    cur_player_idx = 0

    chip_count_dict = {
        3: 11,
        4: 11,
        5: 11,
        6: 9,
        7: 7
    }
    cards = []
    min_val = 3
    max_val = 35
    current_card = None
    current_chips = 0

    def __init__(self):
        pass

    def set_players(self, players: List[Player]):
        self.players = players

    def set_card_range(self, minval, maxval):
        self.min_val = minval
        self.max_val = maxval

    def set_burn_num(self, num):
        self.burn_num = num

    def force_chips_per_player(self, num):
        self.forced_chips_per_player = num

    def advance_turn(self):
        self.cur_player_idx = (self.cur_player_idx + 1) % len(self.players)

    def setup_game(self, silent):
        # Give chips
        if self.forced_chips_per_player is not None:
            chips = self.forced_chips_per_player
        elif len(self.players) in self.chip_count_dict:
            chips = self.chip_count_dict[len(self.players)]
        else:
            chips = self.default_chip_count
        for player in self.players:
            player.chips = chips

        # Make cards
        for n in range(self.min_val, self.max_val + 1):
            self.cards.append(n)

        # Fisher-Yates shuffle
        n = len(self.cards)
        for i in range(n - 1, 1, -1):
            j = random.randint(0, i - 1)
            (self.cards[i], self.cards[j]) = (self.cards[j], self.cards[i])

        # Shuffle players too
        n = len(self.players)
        for i in range(n - 1, 1, -1):
            j = random.randint(0, i - 1)
            (self.players[i], self.players[j]) = (self.players[j], self.players[i])

        # Burn cards
        if not silent:
            print("Burns: ")
        for i in range(self.burn_num):
            card = self.cards.pop()
            if not silent:
                print(str(card) + ' ', end='')
        if not silent:
            print()

        # First card
        self.current_card = self.cards.pop()

    def cleanup_game(self):
        # Clear player cards
        for player in self.players:
            player.cards.clear()

    def play(self, silent=True):
        self.setup_game(silent)

        if not silent:
            print("Playing with " + str(len(self.players)) + " players and " + str(len(self.cards)) + " cards!")

        # Random starter
        self.cur_player_idx = random.randint(0, len(self.players) - 1)

        while True:
            cur_player = self.players[self.cur_player_idx]
            # print(cur_player.name + '\'s turn!')

            cur_card = self.current_card

            take = cur_player.decide_if_take(cur_card, self.current_chips, self)

            # Take
            if take or cur_player.chips == 0:
                cur_player.take_card(cur_card, self.current_chips, silent)
                self.current_chips = 0

                # Out of cards, done
                if len(self.cards) == 0:
                    break

                # Draw next
                self.current_card = self.cards.pop()
            # Pass
            else:
                # print(cur_player.name[0], end='')
                if not silent:
                    print('.', end='')

                self.current_chips += 1
                cur_player.chips -= 1

                self.advance_turn()

        # Game end
        winners = []
        best_score = math.inf

        if not silent:
            print("\nScores:")

        self.players.sort(key=lambda p: p.get_score())
        for player in self.players:
            score = player.get_score()

            if not silent:
                print(str(score) + " | " + player.name + " (" + str(player.chips) + " chips)")

            if score == best_score:
                # print("Add " + player.name)
                winners.append(player)

            elif score < best_score:
                # print("New best " + player.name)
                best_score = score
                winners.clear()
                winners.append(player)

        if not silent:
            print("\nWinners: ", end='')
            for winner in winners:
                print(winner.name + " ", end='')
            print()

        self.cleanup_game()

        return winners


def manual_run(game, silent=False):
    again = ''

    while again != 'q':
        game.play(silent)
        again = input('Press q to exit or any other key to play again')


def simulate_many(game, num, silent=True):
    results_dict = {}
    for i in range(num):
        winners = game.play(silent)
        winners.sort(key=lambda p: p.name)

        winner_text = ', '.join(winner.name for winner in winners)

        if winner_text in results_dict:
            results_dict[winner_text] += 1
        else:
            results_dict[winner_text] = 1

        if i % 1000 == 0:
            print('.', end='')

    # Done with sim
    print("Results (Omitting < 1% WR): ")
    print_list = list(results_dict.keys())
    print_list.sort(key=lambda r: results_dict[r], reverse=True)

    for key in print_list:
        # print(str(results_dict[key]/num))
        # Skip if less than 0.5%
        portion = results_dict[key] / num
        if portion < 0.01:
            continue
        print(key + ": " + str(results_dict[key]) + " (" + str(round(portion * 100, 3)) + "%)")


def main():
    game = IllPassGame()
    game.set_card_range(3, 35)
    game.set_burn_num(9)
    game.force_chips_per_player(7)

    game.set_players([
        # TakeCostAtMost("Val < 30", 30),
        # TakeCostAtMost("Val < 25", 25),
        TakeCostAtMost("Val < 15", 15),
        TakeCostAtMost("Val < 10", 10),
        # TakeCostAtMost("Val < 5", 5),
        TakeIfWithin("Within 2", 2),
        TakeIfWithin("Within 3", 3),
        # TakeIfWithin("Within 1", 1),
        # AlwaysPassPlayer("Always Pass"),
        # Player("Always Take"),
        # RandomPlayer("Random"),
    ])

    #manual_run(game)
    simulate_many(game, 20000)


if __name__ == '__main__':
    main()
