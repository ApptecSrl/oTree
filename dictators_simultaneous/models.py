# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
import otree.constants
import random
from otree import widgets
from otree.common import Currency as c, currency_range
from django.utils.translation import ugettext as _
# </standard imports>


doc = """
Players decides how to divide a certain amount between themselves and another
player (who does the same with a different partner).
"""

#source_code = "https://github.com/oTree-org/oTree/tree/master/dictator"


bibliography = (
    (
        'Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness '
        'and the assumptions of economics." Journal of business (1986): '
        'S285-S300.'
    ),
    (
        'Hoffman, Elizabeth, Kevin McCabe, and Vernon L. Smith. "Social '
        'distance and other-regarding behavior in dictator games." The '
        'American Economic Review(1996): 653-660.'
    )
)


links = {
    "Wikipedia": {
        "Dictator Game": "https://en.wikipedia.org/wiki/Dictator_game"
    }
}


keywords = ("Dictator Game", "Fairness", "Homo Economicus")


class Constants(otree.constants.BaseConstants):
    name_in_url = 'dictators_simultaneous'
    players_per_group = None
    num_rounds = 1
    bonus = c(0)
    # Initial amount allocated to the dictator
    allocated_amount = c(100)




class Subsession(otree.models.BaseSubsession):

    pass


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>



    def set_payoffs(self):
        players=self.get_players()
        num_players=len(players)
        for i in range(1,num_players+1):
            print ('numero giocatori ', num_players)
            p=self.get_player_by_id(i)
            prec= i-1
            if prec==0:
                prec = num_players
            p.offered = Constants.allocated_amount - self.get_player_by_id(prec).kept
            p.payoff = Constants.bonus + p.kept +p.offered
            print ('payoff ',i, p.payoff)


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    training_participant1_payoff = models.CurrencyField(
        verbose_name=(_("Your payoff would be")))
    training_participant2_payoff = models.CurrencyField(
        verbose_name=(_("The other participant's payoff would be")))

    kept = models.CurrencyField(
        doc="""Amount player decided to keep for himself""",
        min=0, max=Constants.allocated_amount,
        verbose_name=(_('I will keep (from 0 to %i)')) % Constants.allocated_amount
    )

    offered = models.CurrencyField(
        doc="""Amount player was offered by other""",
        min=0, max=Constants.allocated_amount
    )