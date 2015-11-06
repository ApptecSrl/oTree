# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
from django.utils.translation import ugettext as _


def vars_for_all_templates(self):
    return {'instructions': 'dictators_simultaneous/Instructions.html',
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
        return {'question_template': 'dictators_simultaneous/Question.html'}


class Feedback1(Page):
    template_name = 'dictators_simultaneous/Feedback.html'

    def is_displayed(self):
        return self.subsession.round_number == 1

    def vars_for_template(self):
        p = self.player
        return {'answers': {
                'participant 1': [p.training_participant1_payoff, 88],
                'participant 2': [p.training_participant2_payoff, 12]}}


class Offer(Page):

    form_model = models.Player
    form_fields = ['kept']

    # def is_displayed(self):
    #     return self.player.id_in_group == 1


class MatchingWaitPage(WaitPage):

    def is_displayed(self):
        return self.subsession.round_number == 1

    def after_all_players_arrive(self):
        print 'Ora matching per dittatore simultaneo'
        self.makeTheGroup()

    def makeTheGroup(self):
        for p in self.subsession.get_players():
            p.tipo=p.participant.vars['kind']
            print p.tipo
        players = self.subsession.get_players()
        num_players = len(players)
        list_of_players = []
        firstFloorPlayers = []
        secondFloorPlayers = []
        self.build1st2ndFloor(players, firstFloorPlayers, secondFloorPlayers)
        min12 = min(len(firstFloorPlayers), len(secondFloorPlayers))
        for i in range(0, min12):
            list_of_players.append(firstFloorPlayers[i])
            list_of_players.append(secondFloorPlayers[i])
        print 'elenco (alterato) dei giocatori', list_of_players
        
        for group in self.subsession.get_groups():
            players = group.get_players()
            players.reverse()
            group.set_players(list_of_players)
        

    def build1st2ndFloor(self, players, firstFloorPlayers, secondFloorPlayers): #forma e rimescola i pari e dispari
        num_players=len(players)
        for i in range(0, num_players, 1):
            if (players[i].tipo) < 200:
                firstFloorPlayers.append(players[i])
            else:
                secondFloorPlayers.append(players[i])
        random.shuffle(firstFloorPlayers)
        random.shuffle(secondFloorPlayers)
        print 'primo piano', firstFloorPlayers
        print 'secondo piano', secondFloorPlayers

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        print 'ora valuto il payoff'
        self.group.set_payoffs()

class Results(Page):
    template_name = 'global/ResultsTable.html'


    def vars_for_template(self):

        payment_result = {
            'offered':self.player.offered,
            'kept':self.player.kept,
            'payoff': self.player.payoff
        }


        result_table = [
            (_('Another participant decided to offer you'), payment_result['offered']),
            (_('You kept for yourself'), payment_result['kept']),
        ]

        result_table.append((_('Your payoff in this activity'), payment_result['payoff']))

        game_results = {
            'label': 'Dictator game',
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
            'table': [(_('This activity is over. Results will be shown later.'),)]
        }


page_sequence = [Introduction,
            #Question1,
            #Feedback1,
            MatchingWaitPage,
            Offer,
            ResultsWaitPage,
            Results]
