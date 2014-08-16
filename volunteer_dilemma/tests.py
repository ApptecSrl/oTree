import otree.test
from otree.common import Money, money_range
import volunteer_dilemma.views as views
from volunteer_dilemma.utilities import Bot
import random


class PlayerBot(Bot):

    def play(self):

        # decision
        self.submit(views.Decision, {"decision": random.choice(['Volunteer','Ignore'])})

        # results
        self.submit(views.Results)
