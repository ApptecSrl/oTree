import os

import dj_database_url
from boto.mturk import qualification

import otree.settings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# OTREE_PRODUCTION just controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if os.environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# IS_OTREE_DOT_ORG is only used on demo.otree.org.
# you can assume it is None/''/0.
if os.environ.get('IS_OTREE_DOT_ORG') in {None, '', '0'}:
    ADMIN_PASSWORD = 'maremmaMaiala'
    # don't share this with anybody.
    # Change this to something unique (e.g. mash your keyboard),
    # and then delete this comment.
    SECRET_KEY = 'beeLabbe'
else:
    DEBUG = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'otree'
# don't share this with anybody.
# Change this to something unique (e.g. mash your keyboard),
# and then delete this comment.
SECRET_KEY = 'zzzzzzzzzzzzzzzzzzzzzzzzzzz'

PAGE_FOOTER = ''

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

ADMIN_USERNAME = 'admin'

# AUTH_LEVEL:
# If you are launching an experiment and want visitors to only be able to
# play your app if you provided them with a start link, set the
# environment variable OTREE_AUTH_LEVEL to EXPERIMENT.
# If you would like to put your site online in public demo mode where
# anybody can play a demo version of your game, set OTREE_AUTH_LEVEL
# to DEMO. This will allow people to play in demo mode, but not access
# the full admin interface.

AUTH_LEVEL = 'EXPERIMENT'
#AUTH_LEVEL = os.environ.get('OTREE_AUTH_LEVEL')

# ACCESS_CODE_FOR_DEFAULT_SESSION:
# If you have a "default session" set,
# then an access code will be appended to the URL for authentication.
# You can change this as frequently as you'd like,
# to prevent unauthorized server access.

ACCESS_CODE_FOR_DEFAULT_SESSION = 'stud_session'

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
#REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = True


# e.g. en-gb, de-de, it-it, fr-fr.
# see: https://docs.djangoproject.com/en/1.6/topics/i18n/
# LANGUAGE_CODE = 'en-gb'
LANGUAGE_CODE = 'it-it'

INSTALLED_APPS = [
    'otree',
]

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""

# from here on are qualifications requirements for workers
# see description for requirements on Amazon Mechanical Turk website:
# http://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_QualificationRequirementDataStructureArticle.html
# and also in docs for boto:
# https://boto.readthedocs.org/en/latest/ref/mturk.html?highlight=mturk#module-boto.mturk.qualification

#LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

mturk_hit_settings = {
    'keywords': ['easy', 'bonus', 'choice', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7 * 24,  # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': [
        qualification.LocaleRequirement("EqualTo", "US"),
        qualification.PercentAssignmentsApprovedRequirement("GreaterThanOrEqualTo", 50),
        qualification.NumberHitsApprovedRequirement("GreaterThanOrEqualTo", 5),
        #qualification.Requirement('YOUR_QUALIFICATION_ID_HERE', 'DoesNotExist')
    ]
}

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.05,
    'participation_fee': 3.00,
    'num_bots': 12,
    'doc': "",
    'group_by_arrival_time': False,
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [
    {
         'name': 'public_goods',
         'display_name': "Public Goods",
         'num_demo_participants': 3,
         'app_sequence': ['public_goods'],
    },
    # {
    #     'name': 'bare_market',
    #     'display_name': "Bare Market game",
    #     #'real_world_currency_per_point': 0.25,
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'welcome_noCharity','bare_market', 'payment_recap'
    #     ],
    # },
     {
        'name': 'risk',
        'display_name': "Risky choice",
        'num_demo_participants': 1,
        'app_sequence': ['risk'],
    },
    # {
    #     'name': 'risk_final_info',
    #     'display_name': "Risky choice with final recap",
    #     'num_demo_participants': 1,
    #     'app_sequence': ['welcome_noCharity','risk', 'payment_recap'],
    # },
    # {
    #     'name': 'dictator',
    #     'display_name': "Dictator Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['dictator', 'payment_recap'],
    # },
    # {
    #     'name': 'dic_sim',
    #     'display_name': "Simultaneous Dictator Game",
    #     'num_demo_participants': 2,
    #     'app_sequence': ['welcome_noCharity','dictators_simultaneous', 'payment_recap'],
    # },
    {
        'name': 'welcome',
        'display_name': "Welcome",
        'num_demo_participants': 1,
        'app_sequence': ['welcome_choice'],
    },
    {
        'name': 'unc_role_dic',
        'display_name': "Role Uncertain Dictators",
        'num_demo_participants': 2,
        'random_start_order': True,
        'app_sequence': ['welcome_choice','role_uncertain_dictator', 'payment_recap'],
    },
    {
        'name': 'marketInfo',
        'display_name': "Informed Market game",
        'num_demo_participants': 2,
        'real_world_currency_per_point': 0.1,
        'participation_fee': 0.00,
        'treatment': 'imprenditori',
        'iftherestime': True,
        'app_sequence': ['welcome_choice','marketInfo','payment_recap'],
    },
        {
        'name': 'Test_market',
        'display_name': "Market game, Welcome and recap",
        #'real_world_currency_per_point': 0.25,
        'num_demo_participants': 2,
        'app_sequence': [
            'welcome_choice', 'market', 'payment_recap'
        ],
    },
    # {
    #     'name': 'welcome_noCharity',
    #     'display_name': "Welcome",
    #     'num_demo_participants': 1,
    #     'app_sequence': [
    #         'welcome_noCharity'
    #     ],
    # },
    # {
    #     'name': 'Entrepreneurs_UK_session',
    #     'display_name': "Entrepreneurs, UK session",
    #     'num_demo_participants': 2,
    #     'real_world_currency_per_point': 0.076923077,
    #     'participation_fee': 27.00,
    #     'app_sequence': [
    #         'welcome_choice','market','risk','public_goods','role_uncertain_dictator','payment_recap'
    #     ],
    # },

    {
        'name': 'Imprenditori',
        'display_name': "Sessione imprenditori completa con Charity",
        'num_demo_participants': 2,
        'real_world_currency_per_point': 0.1,
        'participation_fee': 35.00,
        'app_sequence': [
            'welcome_choice', 'market', 'risk', 'public_goods', 'role_uncertain_dictator', 'payment_recap'
        ],
    },
    {
        'name': 'Imprenditori_lunga',
        'display_name': "Sessione lunga imprenditori",
        'num_demo_participants': 2,
        'real_world_currency_per_point': 0.1,
        'participation_fee': 35.00,
        'treatment': 'imprenditori',
        'iftherestime': True,
        'app_sequence': [
            'welcome_choice', 'market', 'risk', 'public_goods', 'role_uncertain_dictator', 'marketInfo','payment_recap'
        ],
    },
    # {
    #     'name': 'sequenza_corta_conCharity',
    #     'display_name': "Sessione studenti corta con Charity",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'welcome_choice','market','role_uncertain_dictator','payment_recap'
    #     ],
    # },
    # {
    #     'name': 'sequenza_noCharity',
    #     'display_name': "Sessione studenti senza charity, bare_market, public_goods e ru_dictator",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'welcome_noCharity','bare_market','public_goods','role_uncertain_dictator','payment_recap'
    #     ],
    # },
    # {
    #     'name': 'sequenza_Market_MarketInfo',
    #     'display_name': "Sessione studenti con Market seguito da MarketInfo e RU_Dict",
    #     'num_demo_participants': 2,
    #     'app_sequence': [
    #         'welcome_choice','market','marketInfo','role_uncertain_dictator','payment_recap'
    #     ],
    # },
]

otree.settings.augment_settings(globals())
if 'SENTRY_DSN' in os.environ:
    SENTRY_DSN = os.environ['SENTRY_DSN']
else:
    SENTRY_DSN = 'http://70fb2d62c5de48739cbaca564d2c855e:29ebb03040ee4eb79eca7e359f26b627@pingu.pin.unifi.it:8002/9'
