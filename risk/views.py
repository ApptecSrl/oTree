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

class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        ctx = super(Introduction, self).vars_for_template()
        name = 'risk'
        n = self.player.participant.session.config['app_sequence'].index(name)
        ctx['title'] = u'Attività n°{}'.format(n)
        return ctx


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_profit_positive', 'training_my_profit_negative']
    question = mark_safe(_('''Considera la seguente situazione.\
                 Hai scelto di investire 40 punti dei 100 a tua disposizione.<br><br>\
                 Nell'ipotesi che il progetto avesse un esito positivo, quanti punti\
                 guadagneresti complessivamente?<br>\
                 Se, viceversa, il progetto avesse un esito negativo, quanti punti\
                 guadagneresti complessivamente?'''))

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 1,
            'question': self.question
        }


class Feedback1(Page):
    template_name = 'global/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {
            'num_q': 1,
            'answers': {
                _('"Guadagno complessivo in caso di esito positivo"'): [p.training_my_profit_positive, 160],
                _('"Guadagno complessivo in caso di esito negativo"'): [p.training_my_profit_negative, 60]
            },
            'explanation': mark_safe(
                _('''<br><strong>Domanda: </strong>''') + Question1.question\
                + _('''<br><br><strong>Soluzione: </strong><br>Guadagno in caso di esito positivo = 160\
                <br>Guadagno in caso di esito negativo = 60''')\
                + _('''<br><br><strong>Spiegazione: </strong> Il guadagno e\' dato dalla quota\
                di punti che si e\' deciso di non investire sommata ai punti che derivano\
                dall'investimento. In questo caso, nell'ipotesi di esito positivo si ha\
                <strong>(100 - 40) + 40 * 2.5 = 160</strong>, mentre nell'ipotesi di esito negativo\
                si ha <strong>(100 - 40) = 60 </strong>'''))
        }


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
    Introduction,
    Question1,
    Feedback1,
    Invest,
    ResultsWaitPage,
    ResultsFinal
]
