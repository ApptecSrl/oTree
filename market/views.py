# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _



def vars_for_all_templates(self):
    return {'instructions': 'market/Instructions.html'}


class Introduction(Page):

    template_name = 'global/Introduction.html'

    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_profit']
    question = '''Suppose that you set your price at 40 points and the other\
        firm at 50 points. What would be your profit?'''

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'question': self.question}


class Feedback1(Page):
    template_name = 'global/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {
            'answer': [p.training_my_profit, 40],
            'explanation': mark_safe(Question1.question + '''
                <strong>Solution: 40 points</strong>
                <strong>Explanation:</strong> Since your price was lower than\
                that of the other firm, the buyer bought from you. Hence your\
                profit would be your price, which was <strong>40\
                points</strong>.''')
        }


class Decide(Page):

    form_model = models.Player
    form_fields = ['price', 'quality']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'global/ResultsTable.html'

    def vars_for_template(self):
        self.player.participant.vars['share'] = self.player.share
        return {
            'table': [
                ('', 'Punti'),
                (_('Your price'), self.player.price),
                ('Your quality', self.player.quality),
                ('Your profit', self.player.payoff),
                ('Your share', self.player.share),
                #rendere share e impact visibili qui
            ]
        }


page_sequence = [Decide,
            ResultsWaitPage,
            Results]
