
class GameStateManager:
    def __init__(self):
        self.current_state = 'mainmenu'
        self.states = {
            'mainmenu': '',
            'level': '',
        }

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state
