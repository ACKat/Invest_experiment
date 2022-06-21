#from itertools import combinations
from otree.api import *
import numpy as np
import pandas as pd


doc = """
Create the main task
"""


class C(BaseConstants):
    NAME_IN_URL = 'InvestTask'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Parameters
    initial_endowment = 10 
    initial_inv_cost = [12,8]
    prob_success_chosen = [0.6, 0.4]
    prob_success_unchosen = [0.6, 0.4]
    revenue_gained = 8
    additional_revenue_if_successful = 8
    additional_cost = 4


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
# Variables to save at the player (and participant) level
    Prolific_ID         = models.StringField()

    # Decision on whether to continue the investment
    additional_invest   = models.BooleanField(
        choices=[
            [True, 'Invest'],
            [False, 'Do not invest']
            ]
            )

    # Attention 
    # I want the first button clicked, the number of times each button is 
    # clicked and the aggregate time it stays on
    sButtonClick        = models.LongStringField(blank=True) 
    sTimeClick          = models.LongStringField(blank=True)

    # Focus
    iFullscreenChange   = models.IntegerField(blank=True)

    # Attributes of the treatment presented to the participant
    sunk_cost           = models.IntegerField(blank=True)
    prob_chosen         = models.FloatField(blank=True)
    prob_unchosen       = models.FloatField(blank=True)
    current_endowment   = models.IntegerField(blank=True)


# FUNCTIONS

def creating_session(subsession):
    import itertools

    treatments = itertools.cycle(
        itertools.product(C.initial_inv_cost, C.prob_success_chosen, C.prob_success_unchosen)
    )
    for player in subsession.get_players():
        #p = player.participant
        treatment   = next(treatments)
        # print('treatment is', treatment)
        player.sunk_cost     = treatment[0]
        player.prob_chosen   = treatment[1]
        player.prob_unchosen = treatment[2]

    return player.sunk_cost, player.prob_chosen, player.prob_unchosen

def calculate_payoff(player):
    if player.additional_invest:
        rand_num = np.random.randn()
        if rand_num <= player.prob_chosen:
            player.payoff = C.initial_endowment-player.sunk_cost+C.revenue_gained-C.additional_cost + C.additional_revenue_if_successful
        else:
            player.payoff = C.initial_endowment-player.sunk_cost+C.revenue_gained-C.additional_cost
    else:
        player.payoff = C.initial_endowment-player.sunk_cost+C.revenue_gained

    return player.payoff        

# PAGES

class Initial_investment(Page):
    pass


class Project_information(Page):
    form_model = 'player'
    form_fields = [
        'additional_invest',
        'sButtonClick',
        'sTimeClick',
        'iFullscreenChange' 
    ]

    def vars_for_template(player):
        #current_endowment = C.initial_endowment-player.sunk_cost+C.revenue_gained
        return dict(
            sunk_cost     = player.sunk_cost,
            prob_success_chosen = player.prob_chosen,
            prob_success_unchosen = player.prob_unchosen
            #current_endowment = player.current_endowment
        )

class Additional_investment(Page):
    pass

class Results(Page):
    def vars_for_template(player):
        payoff = calculate_payoff(player)
        return dict(
            payoff = payoff
        )

page_sequence = [Project_information, Results]
