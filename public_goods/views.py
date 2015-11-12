# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from django.utils.translation import ugettext as _
import random

class MatchingWaitPage(WaitPage):

    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):

        print 'Ora matching public goods in corso'

        players = self.subsession.get_players()
        num_players = len(players)
        random.shuffle(players)
        list_of_lists = []

        if (num_players < 6):
                list_of_lists.append(players)
        else:
            if (num_players % 4) == 0: #groups are all 4 players each
                num_groups = num_players//4
                for i in range(0, num_groups*4,4):
                    list_of_lists.append(players[i:i+4])

            if (num_players % 4) == 2: #2 groups are 3 each, rest are 4 players groups
                num_4groups = num_players//4 - 1
                for i in range(0, num_4groups*4,4):
                    list_of_lists.append(players[i:i+4])
                list_of_lists.append(players[num_players-6:num_players-3])
                list_of_lists.append(players[num_players-3:num_players])

            print list_of_lists

        self.subsession.set_groups(list_of_lists)

        print self.subsession.get_groups()
        #Check now the result
       # self.check_inside_groups()

    def check_inside_groups(self):
            produced_groups = self.subsession.get_groups()
            for g in produced_groups:
                print 'Gruppo numero ', g
                print 'lunghezza gruppo', len(g)

class Introduction(Page):

    """Description of the game: How to play and returns expected"""

    def vars_for_template(self):
        ctx = super(Introduction, self).vars_for_template()
        name = 'public_goods'
        n = self.player.participant.session.config['app_sequence'].index(name)
        ctx['title'] = u'Attività n°{}'.format(n)
        return ctx

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
        result_table.append((_('Your payoff in this activity'), self.player.payoff))

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
            'table': [(_('This activity is over. Results will be shown later.'),)]
        }

page_sequence = [
    MatchingWaitPage,
    Introduction,
    Question,
    Feedback,
    Contribute,
    ResultsWaitPage,
    Results
]
