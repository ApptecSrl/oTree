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
        x=random.randint(100, 400)
        self.submit(views.GetInputKind, {

            "kind": x,
            "kindCopy": x,
        })
        self.submit(views.Welcome)
    def validate_play(self):
        pass
