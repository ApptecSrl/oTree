# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree.common import Currency as c, currency_range
from django.db import models as d_models
import random
# </standard imports>

from .share_calculator import calculator

doc = """
2 firms complete in a market by setting prices for homogenous goods.
"""


class Constants(otree.constants.BaseConstants):
    players_per_group = 2
    name_in_url = 'market'
    num_rounds = 1
    bonus = c(0)
    maximum_price = c(400)
    alpha = 2
    efficiency = 1.5


class Subsession(otree.models.BaseSubsession):

    pass


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    tmp_payoff = models.FloatField
    def set_payoffs(self):
        players = self.get_players()
        p1 = players[0].price
        p2 = players[1].price
        q1 = players[0].quality
        q2 = players[1].quality
        share1, share2 = calculator(q1, q2, p1, p2, Constants.alpha)
        print 'share 1: ', share1, 'type ', type(share1)
        print 'share 2: ', share2, 'type ', type(share2)
        imp1 = 	Constants.efficiency * (400 - q1)* share1
        imp2 = 	Constants.efficiency * (400 - q2)* share2
        tmp_payoff1 = float(p1 - q1) * float( share1 )
        tmp_payoff2 = float(p2 - q2) * float(share2)
        print 'payoff 1: ', tmp_payoff1, 'type', type(tmp_payoff1)
        print 'payoff 2: ', tmp_payoff2, 'type', type(tmp_payoff1)
        players[0].payoff = tmp_payoff1
        players[1].payoff = tmp_payoff2
        players[0].share = share1
        players[1].share = share2


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    training_my_profit = models.CurrencyField(
        verbose_name='My profit would be')

    price = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Price player chooses to sell product for"""
    )

    quality = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Price player chooses to produce with quality equal to"""
    )

    share = models.FloatField(min=0, max=1)

