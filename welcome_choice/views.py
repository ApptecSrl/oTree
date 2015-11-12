# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _


class Welcome(Page):
    template_name = 'welcome_choice/Welcome.html'


class GetInputKind(Page):
    template_name = 'welcome_choice/InputKind.html'
    form_model = models.Player
    form_fields = ['kind','kindCopy']

    def error_message(self, values):
        if values["kind"] != values["kindCopy"]:
            return _(u'Inserisci il valore corretto in entrambi i campi')
        if self.player.participant.label:
            if values["kind"] != int(self.player.participant.label):
                print _(u'Controlla di aver preso posto al computer con il numero corretto: ')
                print 'label = ', int(self.player.participant.label)
                print 'kind = ', values["kind"]
                print 'type of label', type(self.player.participant.label)
                print 'type of kind', type(values["kind"])
                return _(u'Controlla di essere alla postazione corretta')
        else:
            self.player.participant.label = 'codice={}'.format(values['kind'])
        self.player.participant.vars['kind'] = values['kind']

    def is_displayed(self):
        return self.subsession.round_number == 1


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Choice(Page):
    pass


page_sequence = [
    GetInputKind,
    Welcome,
    ResultsWaitPage,
    ]
