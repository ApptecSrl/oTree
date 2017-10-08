# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

def vars_for_all_templates(self):
    return {'instructions': 'risk/Instructions.html',
            'constants': Constants}

class WaitOthers(WaitPage):
    def after_all_players_arrive(self):
        #print ('via')

class Introduction(Page):
    template_name = 'global/Introduction.html'
    def vars_for_template(self):
        ctx = super(Introduction, self).vars_for_template()
        name = 'risk'
        n = self.player.participant.session.config['app_sequence'].index(name)
        ctx['title'] = _(u'Activity n.{}').format(n)
        return ctx


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_profit_positive', 'training_my_profit_negative']
    question = mark_safe(_('''Consider the following situation.\
             You chose to invest 40 of your 100 points.<br><br>\
             Assuming the project went well, how many points\
             would you earn as a whole?<br>\
             If instead the project failed, how many points would you earn?'''))
    timeout_seconds = Constants.timeout_q
    timeout_submission = {'training_my_profit_positive': 160, 'training_my_profit_negative': 60}
    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
            'question': self.question
        }


class Feedback1(Page):
    template_name = 'global/Feedback.html'
    timeout_seconds = Constants.timeout_f
    def is_displayed(self):
        return self.subsession.round_number == 1
    def vars_for_template(self):
        p = self.player
        return {
            'num_q': 1,
            'answers': {
                _('"Amount earned in case of successful project"'): [p.training_my_profit_positive, 160],
                _('"Amount earned in case of failed project"'): [p.training_my_profit_negative, 60]
            },
            'explanation': mark_safe(
                _('''<br><strong>Question: </strong>''') + Question1.question\
                + _('''<br><br><strong>Solution: </strong><br>Amount earned in case of successful project = 160\
                <br>Amount earned in case of failed project = 60''')\
                + _('''<br><br><strong>Explanation: </strong> You earn the sum of the points\
                that you retained and those coming from the project. In this case if the project succeeded\
                <strong>(100 - 40) + 40 * 2.5 = 160</strong>, while if the project failed\
                <strong>(100 - 40) = 60 </strong>'''))
        }


class Invest(Page):

    form_model = models.Player
    form_fields = ['invested']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoffs()
            ##print p.payoff


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
    timeout_seconds = Constants.timeout_r

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
            'description': _(u'In this activity you chose how much to invest in a risky project'),
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
    WaitOthers,
    Introduction,
    Question1,
    Feedback1,
    Invest,
    ResultsWaitPage,
    ResultsFinal
]
