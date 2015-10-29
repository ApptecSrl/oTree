# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from django.utils.translation import ugettext as _


class Introduction(Page):

    """Description of the game: How to play and returns expected"""
    pass


class Question(Page):

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['question']


class Feedback(Page):
    def is_displayed(self):
        return True


class Contribute(Page):

    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()

    def body_text(self):
        return _("Waiting for other participants to contribute.")


class Results(Page):

    """Players payoff: How much each has earned"""

    def vars_for_template(self):

        payment_result = {
            'total_earnings': self.group.total_contribution * Constants.efficiency_factor,
            'individual_earnings': self.player.payoff - Constants.base_points,
        }

        result_table = [
            (_('You contributed'), self.player.contribution),
            (_('Other participants contributed'),),
        ]
        for p in self.player.get_others_in_group():
            result_table.append(('', p.contribution))

        result_table.append((_('Total contribution'), self.group.total_contribution))
        result_table.append(('', ''))
        result_table.append((_('Total earnings from the project'), payment_result['total_earnings']))
        result_table.append((_('Your earnings from the project'), self.group.individual_share))
        result_table.append(('', ''))
        result_table.append((_('Thus in total you earned'), payment_result['individual_earnings']))
        result_table.append((_('In addition you get a participation fee of'), Constants.base_points))
        result_table.append(('', ''))
        result_table.append((_('So in sum you will get'), self.player.payoff))

        game_results = {
            'label': _('Public goods game'),
            'results': payment_result,
            'table': result_table,
        }

        # store public_goods payment result in player session
        if 'applications_results' in self.player.participant.vars.keys():
            if game_results['label'] not in [app['label'] for app in self.player.participant.vars['applications_results']]:
                self.player.participant.vars['applications_results'].append(game_results)
        else:
            self.player.participant.vars['applications_results'] = [game_results]

        return {
            'table': [(_('Gioco concluso, i risultati verranno mostrati in seguito'),)]
        }

page_sequence = [
    Introduction,
    Question,
    Feedback,
    Contribute,
    ResultsWaitPage,
    Results
]
