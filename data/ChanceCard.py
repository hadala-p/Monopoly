from resources.LoadSounds import play_sound


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
            play_sound("positive_card")
        elif self.title == "Card3":
            current_player.current_point = 24
            current_player.rect.center = fields[24].get_coordinates()
        elif self.title == "Card4":
            current_player.current_point = 11
            current_player.rect.center = fields[11].get_coordinates()
        elif self.title == "Card5":
            if current_player.current_point == 7:
                current_player.current_point = 5
                current_player.rect.center = fields[5].get_coordinates()
            if current_player.current_point == 22:
                current_player.current_point = 25
                current_player.rect.center = fields[25].get_coordinates()
            if current_player.current_point == 36:
                current_player.current_point = 35
                current_player.rect.center = fields[35].get_coordinates()
        elif self.title == "Card6":
            if current_player.current_point == 7:
                current_player.current_point = 12
                current_player.rect.center = fields[12].get_coordinates()
            if current_player.current_point == 22:
                current_player.current_point = 28
                current_player.rect.center = fields[28].get_coordinates()
            if current_player.current_point == 36:
                current_player.current_point = 38
                current_player.rect.center = fields[38].get_coordinates()
        elif self.title == "Card7":
            current_player.add_money(50)
            play_sound("positive_card")
        elif self.title == "Card8":
            current_player.current_point = current_player.current_point - 3
            current_player.rect.center = fields[current_player.current_point].get_coordinates()
        elif self.title == "Card9":
            current_player.current_point = 10
            current_player.rect.center = fields[10].get_coordinates()
            current_player.in_jail = True
            play_sound("jail")
        elif self.title == "Card10":
            pass
        elif self.title == "Card11":
            current_player.subtract_money(15)
            play_sound("subtract_money")
        elif self.title == "Card12":
            current_player.current_point = 5
            current_player.rect.center = fields[5].get_coordinates()
        elif self.title == "Card13":
            current_player.add_money(150)
            play_sound("positive_card")
        elif self.title == "Card14":
            for player in all_player:
                if player == current_player:
                    current_player.subtract_money((len(all_player) * 50) - 50)
                else:
                    player.add_money(50)
