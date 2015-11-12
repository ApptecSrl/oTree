# -*- coding: utf-8 -*-
from __future__ import division
from django.utils.translation import ugettext as _

from otree.common import Currency as c
from ._builtin import Page, WaitPage


class PaymentRecap(Page):

    def retreive_charity_impact(self):
        money_to_charity = 0
        for app in self.player.participant.vars['applications_results']:
            money_to_charity += float(app['results'].get('impact', 0))
        return money_to_charity

    def vars_for_template(self):
        # retreive results from player's session
        sessions_results = self.player.participant.vars['applications_results']
        self.player.kind=self.player.participant.vars['kind']
        self.player.total_payoff = float(self.player.participant.money_to_pay())
        self.player.total_money_to_charity = c(self.retreive_charity_impact())\
            .to_real_world_currency(self.session)
        self.player.participant.vars['charity'] = self.player.total_money_to_charity
        self.player.invoice=self.player.total_payoff+self.player.total_money_to_charity
        self.player.save()

        return {
            'applications_results': sessions_results,
        }


class TotalPayoff(Page):

    def vars_for_template(self):
        if self.player.participant.vars.get('kind', None):
            table = [(
                _('Your code number is'),
                self.player.participant.vars['kind']
            )]
        else:
            table = []
        table.append((_('Your total payoff'), self.player.total_payoff))
        table.append((_('Money going to charity'), self.player.total_money_to_charity))
        return {
            'table': table
        }


page_sequence = [PaymentRecap, TotalPayoff]

#  c(10).to_real_world_currency(self.session)
