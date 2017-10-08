# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
from django.utils.translation import ugettext as _
# </standard imports>

author = 'Domenico Colucci'

doc = """
Dictators with role uncertainty: each player is asked to play the dictator role.
Subjects know they belong to two different groups, one in which they'll be receivers and one in which they'll be dictators.
Chance will determine which groups will be paid, so that each subject will either be dictator or receiver.
"""


bibliography = (
    (
        'Iriberri, Nagore and Pedro Rey-Biel. "The role of role uncertainty '
        'in modified dictator games " Experimental Economics (2011) 14:160–180.'
    ),

)

class Constants(BaseConstants):


    name_in_url = 'role_uncertain_dictator'
    players_per_group = None
    num_rounds = 1
    bonus = c(0)
    allocated_amount = c(100)
    timeout_f = 60
    timeout_r = 20

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def set_payoffs(self):
        players=self.get_players()
        num_players=len(players)
        rndRoles=random.randint(0,1)
        print('rndRoles = ',rndRoles)
        for i in range(1,num_players+1):
            p=self.get_player_by_id(i)
            prec= i-1
            if prec==0:
                prec = num_players
            p.offered = Constants.allocated_amount - self.get_player_by_id(prec).kept
            if (i % 2) == rndRoles:
                isDictator = 1
                p.stringRole = 'giver'
                p.yourRole = True
            else:
                isDictator = 0
                p.stringRole = 'receiver'
                p.yourRole = False

            p.payoff = Constants.bonus + p.kept*isDictator +p.offered*(1-isDictator)
            print('is Dictator?', i, isDictator, p.stringRole)
            print('payoff ',i, p.payoff)


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null=True)
    # </built-in>
    kept = models.CurrencyField(
        doc="""Amount player decided to keep for himself""",
        min=0, max=Constants.allocated_amount,
        verbose_name=(_('I will keep (from 0 to %i)')) % Constants.allocated_amount
    )

    offered = models.CurrencyField(
        doc="""Amount player was offered by other""",
        min=0, max=Constants.allocated_amount
    )
    yourRole = models.BooleanField

    stringRole = models.TextField(max_length=100, default='no role')
