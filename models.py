class RobotScore(object):
    def __init__(self, treebranchcloser = False, treebranchintact = False, cargoplane = 0):
        self.treebranchcloser = treebranchcloser
        self.treebranchintact = treebranchintact
        self.cargoplane = cargoplane

    def getScore(self):
        score = 0
        if self.treebranchcloser and self.treebranchintact:
            print 'tree success'
            score += 30
        score += self.get_plane_score(self.cargoplane)
        return score

    def get_plane_score(self, argument):
        switcher = {
            0: 0,
            1: 20,
            2: 30,
            }
        return switcher.get(argument, 0)
