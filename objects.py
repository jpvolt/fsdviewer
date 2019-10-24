class Cone:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color



class Line:
    def __init__(self, cone1, cone2, color, size):
        self.cone1 = cone1
        self.cone2 = cone2
        self.color = color
        self.size = size



class LineMiddle:
    def __init__(self, cone1, cone2, cone3, cone4, color, size):
        self.cone1 = cone1
        self.cone2 = cone2
        self.cone3 = cone3
        self.cone4 = cone4
        self.color = color
        self.size = size


class Car:
    def __init__(self, x, y, rot):
        self.x = x
        self.y = y
        self.rot = rot
