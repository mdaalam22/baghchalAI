from lib2to3.pgen2.token import AT
from qtable import QTable

qta = QTable()

qt_d = qta.load('/Users/md.mobasshiraalam/Documents/Personal Project/BaghchalPr/BaghchalV3/best_qtable_3.pkl')
tp = (1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, -1)
print(list(qt_d.values()))