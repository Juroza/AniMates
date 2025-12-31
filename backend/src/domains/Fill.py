from dataclasses import dataclass

@dataclass
class Fill:
    def __init__(self, color: str, startX: float, startY: float):
        self.color = color
        self.startX = startX
        self.startY = startY

    def to_dict(self):
        return {"color": self.color, "startX": self.startX, "startY": self.startY}