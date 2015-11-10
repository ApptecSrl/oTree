# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _


class Welcome(Page):
    template_name = 'welcome_choice/Welcome.html'
    # def vars_for_template(self):
    #     self.player.participant.vars['kind']=[self.player.kind]

class GetInputKind(Page):
    template_name = 'welcome_choice/InputKind.html'
    form_model = models.Player
    form_fields = ['kind','kindCopy']
    def error_message(self, values):
        if values["kind"] != values["kindCopy"]:
            return _(u'Inserisci il valore corretto in entrambi i campi')
        #if values['kind']!=self.player.p
        self.player.participant.vars['kind']=values['kind']
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
    #ResultsWaitPage,
    ]
