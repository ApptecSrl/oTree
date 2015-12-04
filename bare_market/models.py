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
# </standard imports>
from .share_calculator import calculator
from django.utils.translation import ugettext as _

author = 'Domenico Colucci'

doc = """
A market game version with no charities
"""
# TODO: ripulire i templates

class Constants(BaseConstants):
    players_per_group = 2
    name_in_url = 'bare_market'
    num_rounds = 2
    bonus = c(0)
    maximum_price = c(400)
    alpha = 1.5
    efficiency = 1.5

    # define more constants here


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            paying_round = random.randint(Constants.num_rounds / 2, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round

class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>
    tmp_payoff = models.FloatField

    def set_payoffs(self):
        players = self.get_players()
        print 'players =', players
        p1 = players[0].price
        p2 = players[1].price
        q1 = players[0].quality
        q2 = players[1].quality
        share1, share2 = calculator(q1, q2, p1, p2, Constants.alpha)
        tmp_payoff1 = float(p1 - q1) * float(share1)
        tmp_payoff2 = float(p2 - q2) * float(share2)

        players[0].share = share1
        players[1].share = share2
        players[0].pot_payoff = tmp_payoff1
        players[1].pot_payoff = tmp_payoff2

        if self.subsession.round_number == self.session.vars['paying_round']:
            players[0].payoff = tmp_payoff1
            players[1].payoff = tmp_payoff2
        else:
            players[0].payoff = c(0)
            players[1].payoff = c(0)


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null=True)
    # </built-in>

    # Question1
    training_my_profit_1 = models.CurrencyField(
        verbose_name=_('My profit would be'))
    training_my_social_contribution_1 = models.CurrencyField(
        verbose_name=_('My social contribution would be'))
    # Question2
    training_my_profit_2 = models.CurrencyField(
        verbose_name=_('My profit would be'))
    training_my_social_contribution_2 = models.CurrencyField(
        verbose_name=_('My social contribution would be'))
    # Question3
    training_correct_answer_3 = models.PositiveIntegerField(
        min = 1,
        max = 3,
        verbose_name=_('The correct answer is'))

    price = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Price player chooses to sell product for"""
    )

    maxQ = min(price, Constants.maximum_price)

    # print 'price = ', price

    quality = models.CurrencyField(
        min=0, max=maxQ,
        doc="""Price player chooses to produce with quality equal to"""
    )

    pot_payoff = models.CurrencyField(
        min=0, max=Constants.maximum_price,
        doc="""Potential payoff in the period"""
    )

    share = models.FloatField(min=0, max=1)



    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]
