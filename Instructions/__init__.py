from otree.api import *


doc = """
This app includes the introduction page, consent form and instructions of the experiment.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Instructions'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField(
        choices= [
            [True, 'I agree'],
            [False, 'I do not agree']
        ],
        label = ' '
    )
    autosubmit = models.BooleanField(blank=True)


# PAGES
class Introduction(Page):
    timeout_seconds = 60

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.autosubmit = True


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.consent == False:
            return upcoming_apps[-1]

    timeout_seconds = 30

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.autosubmit = True


class Instructions(Page):
    def is_displayed(player):
        return player.consent == True
    
    timeout_seconds = 175

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.autosubmit = True
    
   




page_sequence = [Introduction, Consent, Instructions]
