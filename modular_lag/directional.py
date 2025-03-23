class Directional:
    def __init__(self):
        self.x_up = []
        self.x_down = []
        self.z_up = []
        self.z_down = []
        self.y_up = []
        self.y_down = []
    def fill_colors(self, dim):
        for _ in range(dim):
            self.x_up.append([0] * dim)
            self.x_down.append([1] * dim)
            self.z_up.append([2] * dim)
            self.z_down.append([3] * dim)
            self.y_up.append([4] * dim)
            self.y_down.append([5] * dim)
