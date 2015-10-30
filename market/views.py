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
    return {'instructions': 'market/Instructions.html',
            'short_instructions': 'market/Short_Instructions.html'}

class GetInputKind(Page):
    template_name = 'market/InputKind.html'
    form_model = models.Player
    form_fields = ['kind']

    def is_displayed(self):
        return self.subsession.round_number == 1

class MatchingWaitPage(WaitPage):

    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1



    def after_all_players_arrive(self):

        print 'Ora matching in corso'
        for p in self.subsession.get_players():
            p.tipo=p.participant.vars['kind']
            print p.tipo
        players = self.subsession.get_players()

        if len(players) > 5:
            newGr_mat = []
            evenPlayers = []
            oddPlayers = []
            self.buildEvenOdd(players, evenPlayers, oddPlayers)
            minEO = min(len(evenPlayers),len(oddPlayers))
            if minEO>2:
                threshold = self.computeThreshold(evenPlayers, oddPlayers, minEO)
                self.makeGroups(evenPlayers, oddPlayers, newGr_mat, threshold)
            print 'Nuovi gruppi: ', newGr_mat
            self.subsession.set_groups(newGr_mat)
            #Check now the result
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

class Introduction(Page):

    template_name = 'global/Introduction.html'
    # def vars_for_template(self):
    #     tipo = self.player.participant.vars['kind']

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
                (_('La qualita\' che hai scelto'), self.player.quality),
                ('', ''),
                (_('Il prezzo scelto dall\'altro giocatore'), self.player.other_player().price),
                (_('La qualita\' scelta dall\'altro giocatore'), self.player.other_player().quality),
                ('', ''),
                (_('La tua quota di mercato'), format(self.player.share, '.2%')),
                (_('Il tuo profitto eventualmente risultante se questo fosse il periodo pagato'), self.player.pot_payoff),
                (_('Il tuo impatto positivo se questo fosse il periodo pagato'), self.player.impact),
            ]
        }

class ResultsFinal(Page):

    template_name = 'global/ResultsTable.html'
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        p_paying_round = self.player.in_all_rounds()[self.session.vars['paying_round']-1]
        payment_result = {
            'p_price': p_paying_round.price,
            'p_quality': p_paying_round.quality,
            'p_impact': p_paying_round.impact,
            'p_share': p_paying_round.share,
            'payoff_sum': sum([p.payoff for p in self.player.in_all_rounds()]),
        }

        result_table = [
            (_('Periodo effettivamente pagato'), self.session.vars['paying_round']),
            (_('Il prezzo che hai scelto nel periodo pagato'), payment_result['p_price']),
            (_('La qualita\' che hai scelto nel periodo pagato'), payment_result['p_quality']),
            (_('L\'impatto positivo dovuto alle tue scelte'), payment_result['p_impact']),
            ('', ''),
            (_('La tua quota di mercato nel periodo pagato'), format(payment_result['p_share'], '.2%')),
            (_('Il tuo profitto effettivo in questa attivita\''), payment_result['payoff_sum']),
        ]

        game_results = {
            'label': 'Market game',
            'results': payment_result,
            'table': result_table,
        }

        # store market payment result in player session
        if 'applications_results' in self.player.participant.vars.keys():
            if game_results['label'] not in [app['label'] for app in self.player.participant.vars['applications_results']]:
                self.player.participant.vars['applications_results'].append(game_results)
        else:
            self.player.participant.vars['applications_results'] = [game_results]


        return {
            'table': [('Gioco concluso, i risultati verranno mostrati in seguito',)]
        }

page_sequence = [#GetInputKind,
                MatchingWaitPage,
                Introduction,
                Decide,
                ResultsWaitPage,
                ResultsTemp,
                ResultsFinal]
