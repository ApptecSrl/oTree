# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json

# </standard imports>

author = 'Your name here'

doc = """
Your app description
"""

class Constants:
    name_in_url = 'esperimento_di_prova'
    players_per_group = None
    num_rounds = 6

    # define more constants here


class Subsession(otree.models.BaseSubsession):
    pass


class Group(otree.models.BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs(self):
        for p in self.get_players():
            p.payoff = 0 # change to whatever the payoff should be


class Player(otree.models.BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    def other_player(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    def role(self):
        # you can make this depend of self.id_in_group
        return ''
