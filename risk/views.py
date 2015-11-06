# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _

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
        outcome = payoff+invested-Constants.endowment
        if outcome==0:
            self.player.stringOutcome=_('bad')
        else:
            self.player.stringOutcome=_('well')

        stringOutcome=self.player.stringOutcome

class ResultsFinal(Page):

    template_name = 'global/ResultsTable.html'


    def vars_for_template(self):
        outcome = self.player.payoff+self.player.invested-Constants.endowment
        if outcome==0:
            self.player.stringOutcome=_('bad')
        else:
            self.player.stringOutcome=_('well')


        payment_result = {
            'invested': self.player.invested,
            'outcome': self.player.stringOutcome,
            'payoff': self.player.payoff
        }


        result_table = [
            (_('You decided to invest in the risky project'), payment_result['invested']),
            (_('The project went'), payment_result['outcome']),
        ]

        result_table.append((_('Your payoff in this activity'), payment_result['payoff']))

        game_results = {
            'label': 'Risky choice',
            'results': payment_result,
            'table': result_table,
        }

        # store dictator payment result in player session
        if 'applications_results' in self.player.participant.vars.keys():
            if game_results['label'] not in [app['label'] for app in self.player.participant.vars['applications_results']]:
                self.player.participant.vars['applications_results'].append(game_results)
        else:
            self.player.participant.vars['applications_results'] = [game_results]

        return {
            'table': [(_('This activity is over. Results will be shown later.'),)]
        }

page_sequence = [
    Introduction,
    Question,
    Invest,
    ResultsWaitPage,
    ResultsFinal
]
