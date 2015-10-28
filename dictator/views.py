# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _


def vars_for_all_templates(self):
    return {'instructions': 'dictator/Instructions.html',
            'constants': Constants}


class Introduction(Page):

    template_name = 'global/Introduction.html'


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = [
        'training_participant1_payoff', 'training_participant2_payoff']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {'question_template': 'dictator/Question.html'}


class Feedback1(Page):
    template_name = 'dictator/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {'answers': {
                'participant 1': [p.training_participant1_payoff, 88],
                'participant 2': [p.training_participant2_payoff, 12]}}


class Offer(Page):

    form_model = models.Group
    form_fields = ['kept']

    def is_displayed(self):
        return self.player.id_in_group == 1


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        if self.player.id_in_group == 2:
            return "You are participant 2. \
                Waiting for participant 1 to decide."
        return 'Please wait'


class Results(Page):
    template_name = 'global/ResultsTable.html'

    def offer(self):
        return Constants.allocated_amount - self.group.kept

    def vars_for_template(self):

        payment_result = {
            'offer':Constants.allocated_amount - self.group.kept,
            'kept':self.group.kept,
            'payoff': self.player.payoff
        }

        if self.player.id_in_group == 1:
            result_table = [(_('You decided to keep'), payment_result['kept'])]
        else:
            result_table = [
                (_('Participant 1 decided to keep'), payment_result['kept']),
                (_('You got'), payment_result['offer']),
            ]

        result_table.append((_('Your total payoff is'), payment_result['payoff']))

        game_results = {
            'label': _('Dictator game'),
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
            'table': [('Gioco concluso, i risultati verranno mostrati in seguito',)]
        }


page_sequence = [
    Introduction,
    Question1,
    Feedback1,
    Offer,
    ResultsWaitPage,
    Results,
]
