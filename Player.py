class Player:
    """Player class"""

    def __init__(self, name, starting_money, behaviour, simulation_conf, log):
        self.name = name
        self.log = log
        self.position = 0
        self.money = starting_money
        self.consequent_doubles = 0
        self.in_jail = False
        self.days_in_jail = 0
        self.has_jail_card_chance = False
        self.has_jail_card_community = False
        self.is_bankrupt = False
        self.has_mortgages = []
        self.plots_wanted = []
        self.plots_offered = []
        self.plots_to_build = []
        self.cash_limit = behaviour.unspendable_cash
        self.behaviour = behaviour
        self.sim_conf = simulation_conf

    def __str__(self):
        return (
            "Player: "
            + self.name
            + ". Position: "
            + str(self.position)
            + ". Money: $"
            + str(self.money)
        )

    def get_money(self):
        return self.money

    def get_name(self):
        return self.name

    # add money (salary, receive rent etc)
    def add_money(self, amount):
        self.money += amount

    # subtract money (pay reny, buy property etc)
    def take_money(self, amount, board, action_origin):
        amount_taken = min(self.money, amount)
        self.money -= amount
        final_account_balance = self.money
        self.check_bankruptcy(board, action_origin)
        if self.is_bankrupt:
            amount_taken += self.money - final_account_balance
        else:
            amount_taken = amount
        return amount_taken

    # subtract money (pay reny, buy property etc)
    def move_to(self, position):
        self.position = position
        self.log.write(self.name + " moves to cell " + str(position), 3)