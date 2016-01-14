# -*- coding: utf-8 -*-
from __future__ import division
from . import models
import random
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


def vars_for_all_templates(self):
    return {
        'total_q': 3,
        'instructions': 'marketInfo/Instructions.html',
        'short_instructions': 'marketInfo/Short_Instructions.html'
    }


class MatchingWaitPage(WaitPage):

    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):
        if self.subsession.round_number == 1:
            self.matching()
        for subsession in self.subsession.in_rounds(2, Constants.num_rounds):
            subsession.group_like_round(1)

    def matching(self):
        print 'Ora matching in corso'
        for p in self.subsession.get_players():
            p.tipo = p.participant.vars['kind']
            print p.tipo
        players = self.subsession.get_players()
        if len(players) > 5:
            newGr_mat = []
            evenPlayers = []
            oddPlayers = []
            self.buildEvenOdd(players, evenPlayers, oddPlayers)
            minEO = min(len(evenPlayers), len(oddPlayers))
            if minEO > 2:
                threshold = self.computeThreshold(evenPlayers, oddPlayers, minEO)
                self.makeGroups(evenPlayers, oddPlayers, newGr_mat, threshold)
            print 'Nuovi gruppi: ', newGr_mat
            self.subsession.set_groups(newGr_mat)
            # Check now the result
            self.check_inside_groups()

    def computeThreshold(self, evenPlayers, oddPlayers, minEO):
        threshold = minEO // 3 + minEO % 3
        print 'valore soglia = ',threshold
        return threshold

    def makeGroups(self, evenPlayers, oddPlayers, newGr_mat, threshold):
    #forma i gruppi con la logica: misti sino a threshold poi gli altri
        """

        :type newGr_mat: list of lists
        """
        for i in range(0, threshold ):
            newGr_mat.append([evenPlayers[i], oddPlayers[i]])
        for i in range(threshold, len(evenPlayers) - 1, 2):
            newGr_mat.append(evenPlayers[i:i + 2])
        for i in range(threshold, len(oddPlayers) - 1, 2):
            newGr_mat.append(oddPlayers[i:i + 2])

    def buildEvenOdd(self, players, evenPlayers, oddPLayers): #forma e rimescola i pari e dispari
        num_players=len(players)
        for i in range(0, num_players, 1):
            if (players[i].tipo) % 2 == 0:
                evenPlayers.append(players[i])
            else:
                oddPLayers.append(players[i])
        random.shuffle(evenPlayers)
        random.shuffle(oddPLayers)
        print 'pari', evenPlayers
        print 'dispari', oddPLayers

    def check_inside_groups(self):
            produced_groups = self.subsession.get_groups()
            for g in produced_groups:
                print 'Gruppo numero ', g
                pl1 = g.get_player_by_id(1)
                pl2 = g.get_player_by_id(2)
                print 'codice del primo giocatore', pl1.tipo
                print 'codice del secondo giocatore', pl2.tipo

class Info(Page):

    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):

        myType = self.player.participant.vars['kind']
        for p in self.player.get_others_in_group():
            other_type=p.participant.vars['kind']
        print 'My ', myType, ' Other ', other_type
        if (myType%2==other_type%2):
            esito=mark_safe(_('a student from the same field of studies as yourself'))
        else:
            if other_type%2==0:
                esito=mark_safe(_('a social studies student'))
            else:
                esito=mark_safe(_('a business studies student')
)
        return {
            'esito': esito
        }
class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        ctx = super(Introduction, self).vars_for_template()
        name = 'marketInfo'
        n = self.player.participant.session.config['app_sequence'].index(name)
        ctx['title'] = u'Attività n°{}'.format(n)
        return ctx


    def is_displayed(self):
        return self.subsession.round_number == 1



class Decide(Page):

    form_model = models.Player
    form_fields = ['price', 'quality']
    def vars_for_template(self):
        turn = self.subsession.round_number

    def error_message(self, values):
        if values["price"] < values["quality"]:
            return _(u'Il prezzo non può essere più basso della qualità')


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class ResultsTemp(Page):

    template_name = 'global/ResultsTable.html'

    def vars_for_template(self):
        return {
            'table': [
                (_('Turno numero'), self.subsession.round_number),
                (_('Il prezzo che hai scelto'), self.player.price),
                (_(u'La qualità che hai scelto'), self.player.quality),
                ('', ''),
                (_('Il prezzo scelto dall\'altro giocatore'), self.player.other_player().price),
                (_(u'La qualità scelta dall\'altro giocatore'), self.player.other_player().quality),
                ('', ''),
                (_('La tua quota di mercato'), format(self.player.share, '.2%')),
                (mark_safe(_('Il <strong>tuo guadagno</strong> eventualmente risultante se questo fosse il periodo pagato')), self.player.pot_payoff),
                (mark_safe(_('Il <strong>beneficio sociale generato dalle tue scelte</strong> se questo fosse il periodo pagato')), self.player.impact),
            ]
        }

class ResultsFinal(Page):

    template_name = 'global/ResultsTable.html'
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        p_paying_round = self.player.in_all_rounds()[self.session.vars['paying_round']-1]
        payment_result = {
            'price': p_paying_round.price,
            'quality': p_paying_round.quality,
            'impact': p_paying_round.impact,
            'share': p_paying_round.share,
            'payoff': p_paying_round.payoff,
            'payoff_sum': sum([p.payoff for p in self.player.in_all_rounds()]),
        }

        result_table = [
            (_('Periodo effettivamente pagato'), self.session.vars['paying_round']),
            (_('Il prezzo che hai scelto nel periodo pagato'), payment_result['price']),
            (_(u'La qualità che hai scelto nel periodo pagato'), payment_result['quality']),
            (mark_safe(_('Il beneficio sociale dovuto alle tue scelte')), payment_result['impact']),
            ('', ''),
            (_('La tua quota di mercato nel periodo pagato'), format(payment_result['share'], '.2%')),
            (mark_safe(_(u'Il tuo guadagno in questa attività')), payment_result['payoff_sum']),
        ]

        game_results = {
            'label': 'MarketInfo game',
            'results': payment_result,
            'table': result_table,
            'description': _(u'In this activity you chose a price and a quality in a market game. '),
        }

        # store marketInfo payment result in player session
        if 'applications_results' in self.player.participant.vars.keys():
            if game_results['label'] not in [app['label'] for app in self.player.participant.vars['applications_results']]:
                self.player.participant.vars['applications_results'].append(game_results)
        else:
            self.player.participant.vars['applications_results'] = [game_results]


        return {
            'table': [(_(u'Questa attività è conclusa. I risultati verranno mostrati in seguito.'),)]
        }

page_sequence = [MatchingWaitPage,
                 Introduction,
                 Info,
                 Decide,
                 ResultsWaitPage,
                 ResultsTemp,
                 ResultsFinal]
