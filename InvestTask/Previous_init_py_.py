#from itertools import combinations
from otree.api import *
import numpy as np
import pandas as pd


doc = """
Create the two-stage investment task
"""


class C(BaseConstants):
    NAME_IN_URL = 'InvestTask'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Parameters

    initial_endowment = 10 
    initial_inv_cost = [12,8]
    prob_success= [0.6, 0.4]
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

    # Initial investment decision

    initial_invest      = models.StringField(
        widget= widgets.RadioSelectHorizontal,
        choices= ['Project A', 'Project B', 'No investment']
    )

    # Decision on whether to continue the investment

    additional_invest   = models.BooleanField(
        widget= widgets.RadioSelectHorizontal,
        choices=[
            [True, 'Invest'],
            [False, 'Do not invest']
            ]
            )

    # Attention 
    # I want the first and last button clicked and number of clicks

    sButtonClick        = models.LongStringField(blank=True) 
    sTimeClick          = models.LongStringField(blank=True)

    # Focus

    iFullscreenChange   = models.IntegerField(blank=True)

    # Attributes of the treatment presented to the participant

    early_termination   = models.BooleanField(blank=True)
    sunk_cost           = models.IntegerField(blank=True)
    prob_chosen         = models.FloatField(blank=True)
    prob_unchosen       = models.FloatField(blank=True)
    current_endowment   = models.IntegerField(blank=True)


# FUNCTIONS

""" def creating_session(subsession):
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
"""

# create investmet details by randomly selecting a cost and probability of success
"""
def investment(sc, p): 
    investment = np.ones((2,))    # create a vector of ones 
    rand_num = np.random.randn(2) # create two random numbers from the [0,1) interval
    if rand_num[0] > 0.5:         # if the first random number exceeds 0.5 the cost will be 8 and 12 otherwise
        investment[0] = sc[0]
    else:
        investment[0] = sc[1]
    if rand_num[1] > 0.5:         # if the second random number exceeds 0.5 the probability will be 0.4 and 0.6 otherwise
        investment[1] = p[0]
    else:
        investment[1] = p[1]
    return investment

# allocate the details to the two investment options by calling the investment() function

inv_A = investment(C.initial_inv_cost, C.prob_success)
inv_B = investment(C.initial_inv_cost, C.prob_success)

def investment_selection(player):
    if   player.initial_invest == 'Project A':
        player.sunk_cost     = inv_A[0]
        player.prob_chosen   = inv_A[1]
        player.prob_unchosen = inv_B[1]
    elif player.initial_invest == 'Project B':
        player.sunk_cost     = inv_B[0]
        player.prob_chosen   = inv_B[1]
        player.prob_unchosen = inv_A[1]
    else:
        player.early_termination == True

"""
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
    form_model  = 'player'
    form_fields = ['initial_invest']

    # now 


class Project_information(Page): # Need to specify the right variables here!!!!!!!!!!!
    form_model  = 'player'
    form_fields = [
        'sButtonClick',
        'sTimeClick',
        'iFullscreenChange' 
    ]


    def before_next_page(player):

        # create investmet details by randomly selecting a cost and probability of success
        
        def investment(sc, p): 
            investment = np.ones((2,))    # create a vector of ones 
            rand_num = np.random.randn(2) # create two random numbers from the [0,1) interval
            if rand_num[0] > 0.5:         # if the first random number exceeds 0.5 the cost will be 8 and 12 otherwise
                investment[0] = sc[0]
            else:
                investment[0] = sc[1]
            if rand_num[1] > 0.5:         # if the second random number exceeds 0.5 the probability will be 0.4 and 0.6 otherwise
                investment[1] = p[0]
            else:
                investment[1] = p[1]
            return investment

    # allocate the details to the two investment options by calling the investment() function

        def investment_selection(player):
            inv_A = investment(C.initial_inv_cost, C.prob_success)
            inv_B = investment(C.initial_inv_cost, C.prob_success)
            if   player.initial_invest == 'Project A':
                player.sunk_cost     = inv_A[0]
                player.prob_chosen   = inv_A[1]
                player.prob_unchosen = inv_B[1]
            elif player.initial_invest == 'Project B':
                player.sunk_cost     = inv_B[0]
                player.prob_chosen   = inv_B[1]
                player.prob_unchosen = inv_A[1]
            else:
                player.early_termination == True

    def vars_for_template(player):
        #current_endowment = C.initial_endowment-player.sunk_cost+C.revenue_gained
        return dict(
            sunk_cost     = player.sunk_cost,
            prob_success_chosen = player.prob_chosen,
            prob_success_unchosen = player.prob_unchosen
            #current_endowment = player.current_endowment
        )

        
class Additional_investment(Page):
    form_model  = 'player'
    form_fields = ['additional_invest']


class Results(Page):
    def vars_for_template(player):
        payoff = calculate_payoff(player)
        return dict(
            payoff = payoff
        )

page_sequence = [Initial_investment, Project_information, Additional_investment, Results]
