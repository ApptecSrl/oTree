# -*- coding: utf-8 -*-
import matrix_symmetric.forms as forms
from matrix_symmetric._builtin import Page, MatchWaitPage


class Decision(Page):

    template_name = 'matrix_symmetric/Decision.html'

    def get_form_class(self):
        return forms.DecisionForm

    def variables_for_template(self):
        return {'self_A_other_A': self.treatment.self_A_other_A,
                'self_A_other_B': self.treatment.self_A_other_B,
                'self_B_other_A': self.treatment.self_B_other_A,
                'self_B_other_B': self.treatment.self_B_other_B}


class ResultsWaitPage(MatchWaitPage):

    def after_all_players_arrive(self):
        for p in self.match.players:
            p.set_payoff()

    def body_text(self):
        return "Waiting for the other player."


class Results(Page):

    template_name = 'matrix_symmetric/Results.html'

    def variables_for_template(self):

        return {'payoff': self.player.payoff,
                'my_choice': self.player.decision,
                'other_choice': self.player.other_player().decision,
                'same_choice': self.player.decision == self.player.other_player().decision}


def pages():

    return [Decision,
            ResultsWaitPage,
            Results]