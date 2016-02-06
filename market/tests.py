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
        self.submit(views.Question1,{
            'training_my_profit_1':100,
            'training_my_social_contribution_1':0
        })
        self.submit(views.Feedback1)
        self.submit(views.Question2,{
            'training_my_profit_2':60,
            'training_my_social_contribution_2':90
        })
        self.submit(views.Feedback2)
        self.submit(views.Question3, {'training_correct_answer_3':2})
        self.submit((views.Feedback3))

        for i in range(1,self.subsession.round_number):
            pr=c(random.randint(50,400))
            print 'stampo prezzo',pr, 'turno', i
            self.submit(views.Decide,{'price': pr,'quality': c(50)})
        self.submit(views.ResultsWaitPage)
        self.submit(views.ResultsTemp)
        self.submit(views.ResultsFinal)


    def validate_play(self):
        pass
