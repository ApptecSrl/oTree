# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree.common import Currency as c, currency_range
from django.utils.translation import ugettext as _
import random
# </standard imports>

doc = """
This is a one-period public goods game with 4 players or 3 players depending on the number of subjects actually available.
An even number of subjects is assumed. Assignment to groups is random.

"""


#source_code = "https://github.com/oTree-org/oTree/tree/master/public_goods"


bibliography = ()


links = {
    "Wikipedia": {
        "Public Goods Game": "https://en.wikipedia.org/wiki/Public_goods_game"
    }
}


keywords = ("Public Goods",)


class Constants(otree.constants.BaseConstants):

    name_in_url = 'public_goods'
    players_per_group = None
    num_rounds = 1

    #"""Amount allocated to each player"""
    endowment = c(100)
    efficiency_factor = 2
    base_points = c(0)

    question_correct = c(100)
    timeout_q=80
    timeout_f=60
    timeout_r = 20

class Subsession(otree.models.BaseSubsession):

    pass

class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()



    def set_payoffs(self):
        players_in_the_group=len(self.get_players())
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / players_in_the_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share + Constants.base_points


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>


    # Question1
    training_profit = models.CurrencyField(
        verbose_name=_('The payoff of the participant who contributed 80 points would be'))

    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    question = models.CurrencyField()

    def question_correct(self):
        return self.question == Constants.question_correct
