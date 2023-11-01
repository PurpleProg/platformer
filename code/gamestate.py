
class GameStateManager:
    """manage the different states of the game, like menu or level for exemple"""
    def __init__(self):
        self.current_state = 'mainmenu'
        self.states = {
            'mainmenu': None,
            'level': None,
        }

    def get_state(self):
        """return the current state of the game"""
        # est-ce qu'on pourrait juste faire gamestate.current_state ?
        # cette fonction ne sert à rien enfaite
        return self.current_state

    def set_state(self, state):
        """change the state of the game"""

        # est-ce qu'on pourrait juste faire gamestate.current_state = new_state ?
        # cette fonction ne sert à rien enfaite
        # c'est peut-etre un peut plus clair comme ca
        self.current_state = state
