import pickle
class QTable:
    def __init__(self):
        self._qtable = {}

    def __call__(self, state2d):
        return self._qtable.get(state2d, None)

    def save(self, filename):
        if not filename.endswith(".pkl"):
            filename = filename + ".pkl"

        with open(filename, 'ab') as f:
            pickle.dump(self._qtable, f)    

    def load(self, filename):
        if not filename.endswith(".pkl"):
            filename = filename + ".pkl"
     
        with open(filename, 'rb') as f:
            qt = pickle.load(f)   

        return qt