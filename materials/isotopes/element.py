class Element:
    def __init__(self, Z, ZAID, symbol, mass, abundance: dict):
        self.Z = Z
        self.ZAID = ZAID
        self.symbol = symbol
        self.mass = mass
        self.abundance = abundance

    def __repr__(self):
        return f"{self.symbol}"