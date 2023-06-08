import random

from Field import Field
from ChanceCard import ChanceCard


class Chance(Field):
    def __init__(self, name, position_x, position_y, type):
        super().__init__(name, position_x, position_y, type)
        self.cards = self.get_chance_cards()
        self.current_card_index = 0

    def add_card(self, card):
        self.cards.append(card)

    def get_chance_cards(self):
        return [ChanceCard("Card1", "Przejdź do Warszawa"),
                ChanceCard("Card2", "Przejdź na Start (Zabierz 200 $)"),
                ChanceCard("Card3", "Przejdź do Illinois Avenue. Jeśli zdasz Go, odbierz 200 $"),
                ChanceCard("Card4", "Przejdź do St. Charles Place. Jeśli zdasz Go, odbierz 200 $"),
                ChanceCard("Card5", "Przejdź do najbliższej linii kolejowej. Jeśli go nie posiadasz, możesz go kupić"
                                    " w banku. Jeśli są właścicielami, zapłaćcie podwójną kwotę czynszu, do którego są"
                                    " w inny sposób uprawnieni"),
                ChanceCard("Card6", "Żeton postępu do najbliższego Narzędzia. Jeśli go nie posiadasz, możesz go kupić"
                                    " w banku. Jeśli posiadasz, rzuć kostką i zapłać właścicielowi łącznie"
                                    " dziesięciokrotność wyrzuconej kwoty."),
                ChanceCard("Card7", "Bank wypłaca Ci dywidendę w wysokości 50 $"),
                ChanceCard("Card8", "Cofnij się o 3 pola"),
                ChanceCard("Card9", "Iść do więzienia. Idź bezpośrednio do więzienia, nie przechodź przez Start, nie "
                                    "zabieraj 200 $"),
                ChanceCard("Card10", "Dokonaj generalnych napraw całej swojej nieruchomości. Za każdy dom zapłać 25 $."
                                     " Za każdy hotel zapłać 100 $"),
                ChanceCard("Card11", "Kara za przekroczenie prędkości 15zł"),
                ChanceCard("Card12", "Wybierz się na wycieczkę do Reading Railroad. Jeśli przekroczysz Start,"
                                     " odbierz 200 $"),
                ChanceCard("Card13", "Otrzymałeś kredyt budowlany pobierz 150zł"),
                ChanceCard("Card14", "Zostałeś wybrany na Przewodniczącego Rady. Zapłać każdemu graczowi 50 $")]

    def get_current_card(self):
        return self.cards[self.current_card_index]

    def get_random_chance_cards(self):
        random_number = random.randint(0, len(self.cards) - 1)
        self.current_card_index = random_number
        return self.cards[random_number]

