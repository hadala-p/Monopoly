class ChanceCard:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def execute_action(self, current_player, all_player, fields):
        if self.title == "Card1":
            current_player.current_point = 1
            current_player.rect.center = fields[1].get_coordinates()
        elif self.title == "Card2":
            current_player.current_point = 0
            current_player.rect.center = fields[0].get_coordinates()
            current_player.add_money(200)
        elif self.title == "Card3":
            current_player.current_point = 1
            current_player.rect.center = fields[1].get_coordinates()
        elif self.title == "Card4":
            current_player.current_point = 1
            current_player.rect.center = fields[1].get_coordinates()
        elif self.title == "Card5":
            pass
        elif self.title == "Card6":
            pass
        elif self.title == "Card7":
            current_player.add_money(50)
        elif self.title == "Card8":
            current_player.current_point = current_player.current_point - 3
            current_player.rect.center = fields[current_player.current_point].get_coordinates()
        elif self.title == "Card9":
            current_player.current_point = 10
            current_player.rect.center = fields[10].get_coordinates()
            current_player.in_jail = True
        elif self.title == "Card10":
            pass
        elif self.title == "Card11":
            current_player.subtract_money(15)
        elif self.title == "Card12":
            current_player.current_point = 5
            current_player.rect.center = fields[5].get_coordinates()
        elif self.title == "Card13":
            current_player.add_money(150)
        elif self.title == "Card14":
            for player in all_player:
                if player == current_player:
                    current_player.subtract_money((len(all_player) * 50) - 50)
                else:
                    player.add_money(50)
