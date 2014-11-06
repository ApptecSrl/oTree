# -*- coding: utf-8 -*-
from __future__ import division
from otree.session import SessionType
import os


def session_types():

    return [
        SessionType(
            name='demo_game',
            display_name="Demo Game",
            base_pay=0,
            num_demo_participants=1,
            num_bots=1,
            subsession_apps=['demo_game'],
            doc=""""""
        ),
        SessionType(
            name='public_goods',
            display_name="Public Goods",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=3,
            subsession_apps=['public_goods', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='prisoner',
            display_name="Prisoner's Dilemma",
            base_pay=4.00,
            num_demo_participants=2,
            num_bots=2,
            subsession_apps=['prisoner', 'survey_sample', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='cournot_competition',
            display_name="Cournot Competition",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['cournot_competition', 'survey_sample', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='trust',
            display_name="Trust Game",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['trust', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='dictator',
            display_name="Dictator Game",
            base_pay=10.00,
            num_bots=2,
            num_demo_participants=2,
            subsession_apps=['dictator', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='matching_pennies',
            display_name="Matching Pennies",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['matching_pennies', 'survey_sample', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='traveler_dilemma',
            display_name="Traveler's Dilemma",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['traveler_dilemma', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='survey',
            display_name="Survey",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=1,
            subsession_apps=['survey'],
            doc=""""""
        ),
        SessionType(
            name='bargaining',
            display_name="Bargaining Game",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['bargaining', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='beauty',
            display_name="Beauty Contest",
            base_pay=10.00,
            num_bots=10,
            num_demo_participants=5,
            subsession_apps=['beauty', 'survey_sample', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='common_value_auction',
            display_name="Common Value Auction",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=3,
            subsession_apps=['common_value_auction', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='stackelberg_competition',
            display_name="Stackelberg Competition",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['stackelberg_competition', 'survey_sample', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='vickrey_auction',
            display_name="Vickrey Auction",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=3,
            subsession_apps=['vickrey_auction', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='volunteer_dilemma',
            display_name="Volunteer's Dilemma",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=3,
            subsession_apps=['volunteer_dilemma', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='bertrand_competition',
            display_name="Bertrand Competition",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['bertrand_competition', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='principal_agent',
            display_name="Principal Agent",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['principal_agent', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='stag_hunt',
            display_name="Stag Hunt",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['stag_hunt', 'survey_sample', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='battle_of_the_sexes',
            display_name="Battle of the Sexes",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=[
                'battle_of_the_sexes', 'survey_sample', 'lab_results'
            ],
            doc=""""""
        ),
        SessionType(
            # in-progress
            name='asset_market',
            display_name="Asset Market",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=2,
            subsession_apps=['asset_market', 'feedback', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name = 'lemon_market',
            display_name="Lemon Market",
            base_pay=10.00,
            num_bots=12,
            num_demo_participants=3,
            subsession_apps=['lemon_market', 'feedback', 'lab_results'],
            doc=""""""
        ),

    ]


def show_on_demo_page(session_type_name):
    # set the below env var on servers that participants will see,
    # since they should not be able to access the demo page
    if os.environ.get('OTREE_PARTICIPANT_FACING_SITE'):
        return False
    return True


demo_page_intro_text = """
<ul>
    <li><a href="https://github.com/oTree-org/otree" target="_blank">Source code</a> for the below games.</li>
    <li><a href="http://www.otree.org/" target="_blank">oTree homepage</a>.</li>
</ul>
<p>
Below are various games implemented with oTree. These games are all open source,
and you can modify them as you wish to create your own variations. Click one to learn more and play.
</p>
"""