class EnemyClass:
    def __init__(self, x, y, x_change, y_change):
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def x(self):
        return self.x

    def y(self):
        return self.y

    def x_change(self):
        return self.x_change

    def y_change(self):
        return self.y_change

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_x_change(self, x_change):
        self.x_change = x_change

    def set_y_change(self, y_change):
        self.y_change = y_change
