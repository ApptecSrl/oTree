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
        'instructions': 'market/Instructions.html',
        'short_instructions': 'market/Short_Instructions.html'
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

class Introduction(Page):

    template_name = 'global/Introduction.html'

    def vars_for_template(self):
        ctx = super(Introduction, self).vars_for_template()
        name = 'market'
        n = self.player.participant.session.config['app_sequence'].index(name)
        ctx['title'] = u'Attività n°{}'.format(n)
        return ctx


    def is_displayed(self):
        return self.subsession.round_number == 1


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_profit_1', 'training_my_social_contribution_1']
    question = _(u"Consider the following hypothetical scenario. Your chosen quality is 0,\
                 and your chosen price is 200. Also, as a consequence of your choices and\
                 of your opponent's you have a 50% market share.\
                 In this context, your profit and social contribution would be ...\
                 Considera la seguente situazione ipotetica. Hai scelto una qualità pari a 0\
                 e un prezzo pari a 200. Inoltre, come conseguenza delle scelte tue e\
                 dell’altro concorrente hai una quota di mercato pari al 50%.\
                 In questo contesto, il tuo profitto e la tua contribuzione sociale sarebbero ...")

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
                _('"Profit"'): [p.training_my_profit_1, 100],
                _('"Social contribution"'): [p.training_my_social_contribution_1, 0]
            },
            'explanation': mark_safe(
                _('''<br><strong>Question: </strong>''') + Question1.question\
                + _('''<br><br><strong>Solution: </strong>Your Profit would be equal to\
                100 points and your Social Contribution would be equal to 0 points.''')\
                + _('''<br><br><strong>Explanation: </strong> The Profit equals\
                the Total Markup (Price - Quality) multiplied by the Market Share.\
                In this case you have: <strong>(200 - 0) * 50 / 100 = 100 points</strong>.\
                The Social Contribution is obtained by multiplicating the Quality,\
                the Efficiency Factor and the Market Share. In this case it is:\
                <strong>1.5 * 0 * 50 / 100 = 0 points</strong>.'''))
        }

class Question2(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_profit_2', 'training_my_social_contribution_2']
    question = _(u"Consider the following hypothetical scenario. Your chosen quality is 200,\
                 and your chosen price is 400. Also, as a consequence of your choices and\
                 of your opponent's you have a 30% market share.\
                 In this context, your profit and social contribution would be ...\
                 Considera la seguente situazione ipotetica. Hai scelto una qualità pari a 200\
                 e un prezzo pari a 400. Inoltre, come conseguenza delle scelte tue e\
                 dell’altro concorrente hai una quota di mercato pari al 30%.\
                 In questo contesto, il tuo profitto e la tua contribuzione sociale sarebbero ...")

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 2,
            'question': self.question
        }


class Feedback2(Page):
    template_name = 'global/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {
            'num_q': 2,
            'answers': {
                _('"Profit"'): [p.training_my_profit_2, 60],
                _('"Social contribution"'): [p.training_my_social_contribution_2, 90]
            },
            'explanation': mark_safe(
                _('''<br><strong>Question: </strong>''') + Question2.question\
                + _('''<br><br><strong>Solution: </strong>Your Profit would be equal to\
                60 points and your Social Contribution would be equal to 90 points.''')\
                + _('''<br><br><strong>Explanation: </strong> The Profit equals\
                the Total Markup (Price - Quality) multiplied by the Market Share.\
                In this case you have: <strong>(400 - 200) * 30 / 100 = 60 points</strong>.\
                The Social Contribution is obtained by multiplicating the Quality,\
                the Efficiency Factor and the Market Share. In this case it is:\
                <strong>1.5 * 200 * 30 / 100 = 90 points</strong>.'''))
        }

class Question3(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_correct_answer_3']
    question = mark_safe(_(u'''Considera la seguente situazione ipotetica. Nel precedente periodo hai scelto una\
                 qualità pari a 100 e un prezzo pari a 300. La tua quota di mercato è stata pari a 0,2.\
                 Adesso scegli di ridurre il prezzo a 200 mantenendo la qualità uguale a 100.\
                 Quale delle seguenti affermazioni è vera?''') + ('''<br><br>\
                 <strong>(1)</strong> La mia quota di mercato e\' sicuramente cresciuta.<br>\
                 <strong>(2)</strong> La mia quota di mercato e\' maggiore di quella che otterrei\
                 mantenendo l\'offerta precedente.<br>\
                 <strong>(3)</strong> La mia quota di mercato puo\' essere diminuita solo se anche\
                 il rivale ha ridotto il suo prezzo.'''))

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        return {
            'num_q': 3,
            'question': self.question
        }


class Feedback3(Page):
    template_name = 'global/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {
            'num_q': 3,
            'answers': {
                _('"Affermazione corretta"'): [p.training_correct_answer_3, 2],
            },
            'explanation': mark_safe(
                _('''<br><strong>Question: </strong>''') + Question3.question\
                + _('''<br><br><strong>Solution: </strong>Answer nr. 2 is correct.''')\
                + _(u'''<br><br><strong>Explanation: </strong> La risposta n. 1 è falsa\
                perché la tua quota di mercato dipende anche dalle scelte del tuo concorrente.\
                La risposta n. 2 è vera perché per ogni possibile offerta del rivale,\
                una riduzione del tuo prezzo aumenta la tua quota di mercato.\
                La risposta n. 3 è falsa perché la tua quota di mercato può essere diminuita anche se\
                il tuo concorrente ha aumentato sufficientemente la qualità mantenendo\
                il prezzo invariato o aumentandolo di poco.'''))
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
            (_('La qualita\' che hai scelto nel periodo pagato'), payment_result['quality']),
            (mark_safe(_('Il beneficio sociale dovuto alle tue scelte')), payment_result['impact']),
            ('', ''),
            (_('La tua quota di mercato nel periodo pagato'), format(payment_result['share'], '.2%')),
            (mark_safe(_('Il tuo guadagno in questa attivita\'')), payment_result['payoff_sum']),
        ]

        game_results = {
            'label': 'Market game',
            'results': payment_result,
            'table': result_table,
            'description': _(u'In this activity you chose a price and a quality in a market game. '),
        }

        # store market payment result in player session
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
                 Question1,
                 Feedback1,
                 Question2,
                 Feedback2,
                 Question3,
                 Feedback3,
                 Decide,
                 ResultsWaitPage,
                 ResultsTemp,
                 ResultsFinal]
