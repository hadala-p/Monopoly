import random

from CommunityCard import CommunityCard
from Field import Field


class CommunityChest(Field):
    def __init__(self, name, position_x, position_y, type):
        super().__init__(name, position_x, position_y, type)
        self.cards = self.get_community_cards()
        self.current_card_index = 0

    def add_card(self, card):
        self.cards.append(card)

    def get_community_cards(self):
        return [CommunityCard("Card1", "Przejdź na Start (Zabierz 200 $)"),
                CommunityCard("Card2", "Błąd banku na Twoją korzyść. Zabierz 200 $"),
                CommunityCard("Card3", "Opłata lekarza. Zapłać 50 $"),
                CommunityCard("Card4", "Ze sprzedaży akcji otrzymujesz 50 $"),
                CommunityCard("Card5", "Idziesz do więzienia. Idź prosto do więzienia, nie przekraczasz Start,"
                                       " nie zabierasz 200 $"),
                CommunityCard("Card6", "Należy ci się fundusz urlopowy. Otrzymujesz 100 $"),
                CommunityCard("Card7", "Zwrot podatku dochodowego. Zabierz 20 $"),
                CommunityCard("Card8", "To są twoje urodziny. Zdobądź 10 $ od każdego gracza"),
                CommunityCard("Card9", "Ubezpieczenie na życie wypłaca Ci 100$"),
                CommunityCard("Card10", "Musisz zapłacić opłatę szpitalną w wysokości 100$"),
                CommunityCard("Card11", "Opłata za szkołę w wysokości 50 dolarów"),
                CommunityCard("Card12", "Otrzymajesz opłatę konsultacyjną w wysokości 25 USD"),
                CommunityCard("Card13", "Zostałeś ukarany za niszeczenie ulicy. Zapłać 40 dolarów za każdy dom oraz"
                                        " 115 USD za każdy hotel"),
                CommunityCard("Card14", "Dziedziczysz 100 dolarów"),
                CommunityCard("Card15", "Zdobyłaś drugą nagrodę w konkursie piękności. Zbierz 10 $")]

    def get_current_card(self):
        return self.cards[self.current_card_index]

    def get_random_chance_cards(self):
        random_number = random.randint(0, len(self.cards) - 1)
        self.current_card_index = random_number
        return self.cards[random_number]