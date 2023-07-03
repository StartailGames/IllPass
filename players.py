import random


class Player:

    def __init__(self, name):
        self.name = "Player"
        self.name = name
        self.cards = set()
        self.chips = 0

    def decide_if_take(self, num: int, chips: int, game):
        return True

    def take_card(self, card, chips, silent):
        self.cards.add(card)
        self.chips += chips

        if not silent:
            print(self.name + " took " + str(card) + " with " + str(chips) + " chips!")
        #print("Current chips: " + str(self.chips))

    def is_free_number(self, num):
        return num - 1 in self.cards

    def get_score(self):
        score = 0
        #print("Scoring " + self.name)
        # cards
        for card in self.cards:
            if not self.is_free_number(card):
                #print('+' + str(card))
                score += card

        # chips
        score -= self.chips

        return score


class AlwaysPassPlayer(Player):
    def decide_if_take(self, num, chips, game):
        if self.chips > 0:
            return False
        return True


class TakeCostAtMost(Player):
    def __init__(self, name, max_take):
        super().__init__(name)
        self.max_take = max_take

    def decide_if_take(self, num, chips, game):
        # Chips add value
        cost = num - chips

        # Free take
        if self.is_free_number(num):
            #print(str(num) + " is free for " + self.name + "!")
            cost -= num

        if cost <= self.max_take:
            return True
        return False


class TakeIfWithin(Player):
    def __init__(self, name, distance):
        super().__init__(name)
        self.distance = distance

    def decide_if_take(self, num, chips, game):
        for i in range(-self.distance, self.distance):
            if num + i in self.cards:
                return True
        return False


class RandomPlayer(Player):
    def decide_if_take(self, num: int, chips: int, game):
        return random.randint(0, 1) == 0