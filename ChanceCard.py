class ChanceCard:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def execute_action(self, current_player, all_player, fields):
        print(self.name)
        if self.name == "Card1":
            print("card1")
            current_player.current_point = 1
            current_player.rect.center = fields[1].get_coordinates()
        elif self.name == "Card2":
            print("card2")
            current_player.current_point = 0
            current_player.rect.center = fields[0].get_coordinates()
            current_player.add_money(200)
        elif self.name == "Card7":
            print("card7")
            current_player.add_money(50)
        elif self.name == "Card8":
            print(current_player.current_point)
            current_player.current_point = current_player.current_point - 3
            current_player.rect.center = fields[current_player.current_point].get_coordinates()
            pass
