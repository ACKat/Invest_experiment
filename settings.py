from os import environ

SESSION_CONFIGS = [
    # dict(
    #     name='public_goods',
    #     app_sequence=['public_goods'],
    #     num_demo_participants=3,
    # ),

    dict(
        name='InvestTask',
        app_sequence=['InvestTask'],
        num_demo_participants=8,
        iTimeOut=0,
        bRequireFS=True,
        bCheckFocus=True,
    ),

    dict(
        name='Questionnaire',
        app_sequence=['Questionnaire'],
        num_demo_participants=8,
    ),

    dict(
        name='Invest_experiment',
        app_sequence=['Instructions', 'InvestTask', 'Questionnaire'],
        num_demo_participants=8,
    ),   

    
    dict(
        name='Invest_experiment_NA',
        app_sequence=['Instructions', 'InvestTask_NA', 'Questionnaire', 'EndPage'],
        num_demo_participants=3,
    ),   

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = [ # Add the rest of the variables of interest here!!!!
    'ProlificID',
    'consent',
    ]

SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '1646885447672'
