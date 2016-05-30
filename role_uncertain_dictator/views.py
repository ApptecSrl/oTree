# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
from django.utils.translation import ugettext as _



def vars_for_all_templates(self):
    return {'instructions': 'role_uncertain_dictator/Instructions.html',
            'constants': Constants}

class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        ctx = super(Introduction, self).vars_for_template()
        name = 'role_uncertain_dictator'
        n = self.player.participant.session.config['app_sequence'].index(name)
        ctx['title'] = _(u'Activity n.{}').format(n)
        return ctx

class MatchingWaitPage(WaitPage):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):
        print 'Ora matching per dittatore role uncertain'
       # self.makeTheGroup()

    def makeTheGroup(self):
        for p in self.subsession.get_players():
            p.tipo=p.participant.vars['kind']
        for group in self.subsession.get_groups():
            players = random.shuffle(self.subsession.get_players())
            group.set_players(players)


class Offer(Page):

    form_model = models.Player
    form_fields = ['kept']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
            print 'ora valuto il payoff'
            self.group.set_payoffs()

class Results(Page):
    template_name = 'global/ResultsTable.html'

    timeout_seconds = Constants.timeout_r
    def vars_for_template(self):
        if self.player.payoff == self.player.kept:
            self.player.stringRole=_('decider')
        else:
            self.player.stringRole=_('receiver')
        payment_result = {
            'offered':self.player.offered,
            'kept':self.player.kept,
            'payoff': self.player.payoff,
            'role': self.player.stringRole
        }

        if self.player.payoff == self.player.kept:
            result_table = [
                (_('Your role in the game was chosen to be that of'), payment_result['role']),
                (_('You kept for yourself'), payment_result['kept']),

            ]
        else:
            result_table = [
                (_('Your role in the game was chosen to be that of'), payment_result['role']),
                (_('Another participant decided to offer you'), payment_result['offered']),
            ]


        result_table.append((_('Your payoff in this activity'), payment_result['payoff']))

        game_results = {
            'label': 'Dictator game',
            'results': payment_result,
            'table': result_table,
            'description': _(u'In this activity you chose how to split a given amount between yourself and another participant. In addition a third participant decided how to split the same amount between him/herself and you. '),
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


page_sequence = [MatchingWaitPage,
            Introduction,
            #Question1,
            #Feedback1,
            Offer,
            ResultsWaitPage,
            Results]
