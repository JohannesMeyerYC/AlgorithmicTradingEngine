class RiskManager:
    def __init__(self, max_position=0.1):
        self.max_position = max_position

    def apply_risk(self, position_size):
        return min(position_size, self.max_position)
