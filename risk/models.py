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
from random import randint
from django.utils.translation import ugettext as _

# </standard imports>

author = 'Domenico Colucci'

doc = """
Simple lottery to infer risk attitudes
"""


class Constants(BaseConstants):
    name_in_url = 'risk'
    players_per_group = None
    num_rounds = 1
    endowment = c(100)
    returnRate = 2.5
    prob = 0.5

    # define more constants here


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    # Question1
    training_my_profit_positive = models.CurrencyField(
        verbose_name=_('My profit in the case of a positive investment outcome would be'))
    training_my_profit_negative = models.CurrencyField(
        verbose_name=_('My profit in the case of a negative investment outcome would be'))

    def set_payoffs(self):
        randOutcome = randint(0,1)
        self.payoff=Constants.endowment-self.invested+self.invested*Constants.returnRate*randOutcome

    invested = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""Amount player chooses to invest in risky project"""
    )
    question = models.CurrencyField()

    #stringOutcome = models.BooleanField()