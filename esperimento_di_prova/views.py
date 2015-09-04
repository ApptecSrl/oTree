# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Introduction(Page):

    """Description of the game: How to play and returns expected"""
    def body_text(self):
        return "testo di prova"

    def is_displayed(self):
        return self.subsession.round_number == 1

class TheGame(Page):
    pass

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1
    pass


page_sequence = [
    Introduction,
    TheGame,
    ResultsWaitPage,
    Results
]
