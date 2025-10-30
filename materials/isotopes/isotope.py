class Isotope:
    def __init__(self, Z, A, mass, ZAID, symbol, excitation_level=None, abundance=None, decay=None):
        self.Z = Z
        self.A = A
        self.mass = mass              # Mass from Nubase
        self.ZAID = ZAID              # Nubase ID
        self.symbol = symbol              # e.g. "He4"
        self.abundance = abundance    # natural abundance in %
        self.decay = decay            # decay time

    def __repr__(self):
        return f"{self.symbol}"