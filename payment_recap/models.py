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

from django.utils.translation import ugettext as _

author = ''

doc = """
This application provides a recap of all previous results
You need to save the results you want to display in a session user variable
"""


class Constants(BaseConstants):
    name_in_url = 'payment_recap'
    players_per_group = None
    num_rounds = 1

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
    group = models.ForeignKey(Group, null=True)
    # </built-in>

    total_payoff = models.RealWorldCurrencyField(
        doc="""Total player payoff""",
        verbose_name=(_("Total payoff")),
    )
    total_money_to_charity = models.RealWorldCurrencyField(
        doc="""Amount player's impact to charity organization""",
        verbose_name=(_('Charity amount')),
    )
