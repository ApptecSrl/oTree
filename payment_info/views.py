# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
class PaymentInfo(Page):

    def vars_for_template(self):
        # retreive results from player's session
        sessions_results = self.player.participant.vars['applications_results']

        return {'applications_results': sessions_results}


page_sequence = [PaymentInfo]
