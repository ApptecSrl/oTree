# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random
import time
import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Domenico Colucci'

doc = """
Introduces and welcomes, but first of all acquires code received by the experimenters
"""


class Constants(BaseConstants):
    name_in_url = 'welcome_choice'
    players_per_group = None
    num_rounds = 1

    # define more constants here


class Subsession(BaseSubsession):
    def before_session_starts(self):
        self.session.vars['started_at'] = time.time()



class Group(BaseGroup):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Player(BasePlayer):
    # <built-in>
    subsession = models.ForeignKey(Subsession)
    group = models.ForeignKey(Group, null = True)
    # </built-in>

    kind = models.IntegerField(
        min=100, max=400,
        doc="""Label received by experimenters"""
    )

    kindCopy = models.IntegerField(
        min=100, max=400,
        doc="""Label received by experimenters"""
    )



    def get_partner(self):
        """Returns other player in group. Only valid for 2-player groups."""
        return self.get_others_in_group()[0]

    def role(self):
        # you can make this depend of self.id_in_group
        return ''
