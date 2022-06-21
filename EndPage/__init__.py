from otree.api import *


doc = """
Goodbye page
"""


class C(BaseConstants):
    NAME_IN_URL = 'EndPage'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ProlificLink = "https://app.prolific.co/submissions/complete?cc=1EA38881"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    autosubmit = models.BooleanField(blank=True)


# PAGES

class EndPage(Page):
    timeout_seconds = 5

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.autosubmit = True


page_sequence = [EndPage]
