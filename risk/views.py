# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


def vars_for_all_templates(self):
    return {'instructions': 'risk/Instructions.html',
            'constants': Constants}

class Introduction(Page):

    template_name = 'global/Introduction.html'

class Question(Page):

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['question']


class Feedback(Page):
    def is_displayed(self):
        return True



class Invest(Page):
    form_model = models.Player
    form_fields = ['invested']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoffs()
            print p.payoff
class Results(Page):
    # def after_all_players_arrive(self):
    #     self.group.set_payoffs()
    def vars_for_template(self):
        payoff=self.player.payoff
        invested = self.player.invested




page_sequence = [
    Introduction,
    Question,
    Invest,
    ResultsWaitPage,
    Results
]
