import os

class EnvManager:
    def __init__(self):
        self.envs = {}
    
    def get(self, value):
        if self.envs.get(value, None):
            return self.envs.get(value, None)
        self.envs[value] = os.environ.get(value, None)
        return self.envs[value]

