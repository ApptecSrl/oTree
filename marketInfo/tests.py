# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        # compete price
        self.submit(views.Introduction)
        pr=c(random.randint(50,400))
        print pr
        self.submit(views.Decide,{'price': pr,'quality': c(50)})

        self.submit(views.ResultsWaitPage)
        self.submit(views.ResultsTemp)
        self.submit(views.ResultsFinal)


    def validate_play(self):
        pass
