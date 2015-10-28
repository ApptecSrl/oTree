# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
from otree import widgets
from otree.common import Currency as c, currency_range
import random
# </standard imports>

doc = """
This is a one-period public goods game with 3 players. Assignment to groups is
random.

"""


source_code = "https://github.com/oTree-org/oTree/tree/master/public_goods"


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
    efficiency_factor = 1.8
    base_points = c(10)

    question_correct = c(92)


class Subsession(otree.models.BaseSubsession):

    def before_session_starts(self):

        # Creates groups: possibly 4 each group otherwise 2 3-groups and the rest 4-groups
        if self.round_number == 1:

            # extract and mix the players
            players = self.get_players()
            random.shuffle(players)
            num_players = len(players)
            list_of_lists = []
            if (num_players < 6):
                list_of_lists.append(players)
            else:
                if (num_players % 4) == 0: #groups are all 4 players each
                    num_groups = num_players//4
                    for i in range(0, num_groups*4,4):
                        list_of_lists.append(players[i:i+4])

                if (num_players % 4) == 2: #2 groups are 3 each, rest are 4 players groups
                    num_4groups = num_players//4 - 1
                    for i in range(0, num_4groups*4,4):
                        list_of_lists.append(players[i:i+4])
                    list_of_lists.append(players[num_players-6:num_players-3])
                    list_of_lists.append(players[num_players-3:num_players])

            print list_of_lists

            self.set_groups(list_of_lists)
            print self.get_groups()


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share + Constants.base_points


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )

    question = models.CurrencyField()

    def question_correct(self):
        return self.question == Constants.question_correct
