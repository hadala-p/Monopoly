from LoadSounds import play_sound
class CommunityCard:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def execute_action(self, current_player, all_player, fields):
        if self.title == "Card1":
            current_player.current_point = 0
            current_player.rect.center = fields[0].get_coordinates()
            current_player.add_money(200)
            play_sound("positive_card")
        elif self.title == "Card2":
            current_player.add_money(200)
            play_sound("positive_card")
        elif self.title == "Card3":
            current_player.subtract_money(50)
            play_sound("subtract_money")
        elif self.title == "Card4":
            current_player.add_money(50)
            play_sound("positive_card")
        elif self.title == "Card5":
            current_player.current_point = 10
            current_player.rect.center = fields[10].get_coordinates()
            current_player.in_jail = True
            play_sound("jail")
        elif self.title == "Card6":
            current_player.add_money(100)
            play_sound("positive_card")
        elif self.title == "Card7":
            current_player.add_money(20)
            play_sound("positive_card")
        elif self.title == "Card8":
            for player in all_player:
                if player == current_player:
                    current_player.add_money((len(all_player) * 10) - 10)
                else:
                    player.subtract_money(10)
            play_sound("positive_card")
        elif self.title == "Card9":
            current_player.add_money(100)
            play_sound("positive_card")
        elif self.title == "Card10":
            current_player.subtract_money(100)
            play_sound("subtract_money")
        elif self.title == "Card11":
            current_player.subtract_money(50)
            play_sound("subtract_money")
        elif self.title == "Card12":
            current_player.add_money(25)
            play_sound("positive_card")
        elif self.title == "Card13":
            pass
        elif self.title == "Card14":
            current_player.add_money(100)
            play_sound("positive_card")
        elif self.title == "Card15":
            current_player.add_money(10)
            play_sound("positive_card")
