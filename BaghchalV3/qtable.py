import numpy as np
import pandas as pd
import json
import pickle
class QTable:
    def __init__(self):
        self._qtable = {}

    def __call__(self, state2d):
        return self._qtable.get(state2d, None)

    def save(self, filename):
        if not filename.endswith(".pkl"):
            filename = filename + ".pkl"
        # np.savetxt(filename, self._qtable, delimiter=",")
        # df = pd.DataFrame.from_dict(self._qtable,) 
        # df.to_csv(filename, mode='a', index = True, header=False)
        # with open(filename, "a") as outfile:
        #     json.dump(self._qtable, outfile)
        with open(filename, 'ab') as f:
            pickle.dump(self._qtable, f)    

    def load(self, filename):
        if not filename.endswith(".pkl"):
            filename = filename + ".pkl"
        # self._qtable = np.loadtxt(filename, delimiter=",")
        # df = pd.read_csv(filename, header=None, index_col=0, squeeze = True)
        # qt = df.to_dict()
        # return qt
        # with open(filename) as json_file:
        #     qt = json.load(json_file) 
        # return qt      
        with open(filename, 'rb') as f:
            qt = pickle.load(f)   

        return qt