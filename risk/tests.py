# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):
        self.submit(views.Introduction)
        self.submit(views.Question1, {
            "training_my_profit_positive": random.randint(0, 100),
            "training_my_profit_negative": random.randint(0, 100),
        })
        self.submit(views.Feedback1)
        self.submit(views.Invest, {"invested": random.randint(0, 100)})
        self.submit(views.ResultsFinal)


    def validate_play(self):
        pass
