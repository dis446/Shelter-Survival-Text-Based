"""Module containing Player class."""

from Human import Human


class Player(Human):
    """Player class, inherits Human attributes."""

    def __init__(
            self, first_name, day_of_birth,
            parent_1, parent_2, age, gender):
        """Player class constructor.

        Arguments:
        first_name -- first name of Player
        day_of_birth -- day Player was born
        parent_1 -- name of Player's father
        parent_2 -- name of Player's mother
        age -- age of player
        gender -- gender of player
        """
        Human.___init__(
            self, first_name, day_of_birth,
            parent_1, parent_2, age, gender)
        self.medic = 0  # Improves healing capabilities of stimpacks
        self.crafting = 0  # Chance to not use components when crafting.
        self.tactician = 0  # Boosts defense.
        self.cooking = 0  # Boosts production level of kitchen.
        self.barter = 0  # Increases selling prices, decreases buying prices.
        self.inspiration = 0  # Boosts production and defense.
        self.scrapper = 0  # Boosts chance of bonus components when scrapping.
        self.electrician = 0  # Boosts power production
