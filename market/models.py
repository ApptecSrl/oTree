# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree.common import Currency as c, currency_range
from django.db import models as d_models
from django.utils.translation import ugettext as _

import random
# </standard imports>

from .share_calculator import calculator

doc = """
2 firms complete in a market by setting prices and quality for homogenous goods.
"""


class Constants(otree.constants.BaseConstants):
    players_per_group = 2
    name_in_url = 'market'
    num_rounds = 2
    bonus = c(0)
    maximum_price = c(400)
    alpha = 1.5
    efficiency = 1.5


class Subsession(otree.models.BaseSubsession):
#Al momento non funziona a meno di non avere un numero di giocatori che sia multiplo esatto di 6
    def match_to_create_groups(self):
        players = self.get_players()
        print 'players ha tipo', type(players)
        num_players = len(players)
        if num_players > 5:
            third=num_players//6
            newGr_mat = []
            pari = []
            dispari = []
            for i in range(0, num_players, 1):
                if (i) % 2 == 0:
                    pari.append(players[i])
                else:
                    dispari.append(players[i])
            if len(pari)==len(dispari):
                random.shuffle(pari)
                random.shuffle(dispari)
                for i in range(0,third):
                    newGr_mat.append([pari[i],dispari[i]])
                for i in range(third,len(pari),2):
                    newGr_mat.append(pari[i:i+2])
                for i in range(third,len(dispari),2):
                    newGr_mat.append(dispari[i:i+2])
                group_matrix = [g.get_players() for g in self.get_groups()]
                print 'matrice dei gruppi originari =', group_matrix
                print 'new groups matrix =', newGr_mat
                self.set_groups(newGr_mat)
            # else:
            #     minPD=min(len(pari),len(dispari))
            #     for i in range(0,minPD):
            #         newGr_mat.append([pari[i],dispari[i]])

            # group_matrix = [g.get_players() for g in self.get_groups()]
            # print 'matrice dei gruppi originari =', group_matrix
            # random.shuffle(players)
            # newGr_mat=[]
            # for i in range(0,len(players),2):
            #     newGr_mat.append(players[i:i+2])
            # print 'new groups matrix =', newGr_mat
            # self.set_groups(newGr_mat)


    def before_session_starts(self):
        if self.round_number == 1:
            paying_round = random.randint(Constants.num_rounds / 2, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            # matching:
            self.match_to_create_groups()


class Group(otree.models.BaseGroup):
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

        imp1 = Constants.efficiency * q1 * share1
        imp2 = Constants.efficiency * q2 * share2
        players[0].impact = imp1
        players[1].impact = imp2
        tmp_payoff1 = float(p1 - q1) * float(share1)
        tmp_payoff2 = float(p2 - q2) * float(share2)
        print 'payoff 1: ', tmp_payoff1, 'type', type(tmp_payoff1)
        print 'payoff 2: ', tmp_payoff2, 'type', type(tmp_payoff1)
        players[0].share = share1
        players[1].share = share2
        players[0].pot_payoff = tmp_payoff1
        players[1].pot_payoff = tmp_payoff2
        players[0].impact = imp1
        players[1].impact = imp2

        if self.subsession.round_number == self.session.vars['paying_round']:
            players[0].payoff = tmp_payoff1
            players[1].payoff = tmp_payoff2
        else:
            players[0].payoff = c(0)
            players[1].payoff = c(0)


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

    impact = models.CurrencyField(
        doc="""Positive impact due to quality chosen"""
    )

    def other_player(self):
        """Returns the opponent of the current player"""
        return self.get_others_in_group()[0]
