# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
    template_name = 'welcome_choice/Welcome.html'

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass

class Choice(Page):
    pass


page_sequence = [
    Welcome,
    ResultsWaitPage,
    Choice
]
