from states import *


class GameStateManager:
    """manage the different states of the game, like menu or level for exemple"""
    def __init__(self):
        self.current_state = 'mainmenu'

        self.states = {
            'mainmenu': Mainmenu(self),
            'level': None,
            'pause': None,
            'cutscene': Cutscene()
        }

        self.states['level'] = Level_state(0, self.states['mainmenu'].char_num, self)
        self.states['pause'] = Pause(self.states['level'], self)

    def set_state(self, state):
        """change the state of the game"""

        # on pourrait juste faire gamestate.current_state = the_new_state
        # cette fonction ne sert à rien, mais c'est plus comprehensible
        self.current_state = state
