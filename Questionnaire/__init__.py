from otree.api import *
from regex import D


doc = """
Justification and demographic questions
"""


class C(BaseConstants):
    NAME_IN_URL = 'Questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    justification =  models.LongStringField(label='Please justify briefly your decision in the task you just completed:')
    age = models.StringField(
        choices=[
            '18-24 years old', 
            '25-34 years old',
            '35-44 years old',
            '45-54 years old',
            '55-64 years old',
            '65-74 years old',
            '75 years or older'
        ]
    )

    gender = models.StringField(label='What gender do you identify as?',
        choices=[
                'Female',
                'Male',
                'Other',
                'Prefer not to answer'
        ]
    )
    education_level = models.StringField(label= 'Please choose the level of completed education that best applies to your case:',
        choices=[
            'No schooling completed',
            'High school graduate',
            'Trade/technical/vocational training',
            'Bachelor’s degree',
            'Master’s degree',
            'Professional degree',
            'Doctorate degree'

        ]
    )
    education_field = models.StringField(label= 'What is/was your primary field of studies if any?')
    autosubmit = models.BooleanField(blank=True)


# PAGES
class Justification(Page):
    form_model = 'player'
    form_fields = ['justification']

    timeout_seconds = 120

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.autosubmit = True



class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education_level', 'education_field']
    
    timeout_seconds = 15

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.autosubmit = True

page_sequence = [Justification, Demographics]
