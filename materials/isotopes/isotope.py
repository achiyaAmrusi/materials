class Isotope:
    def __init__(self, Z, A, mass, ZAID, symbol, excitation_level=None, abundance=None, decay=None):
        self.Z = Z
        self.A = A
        self.mass = mass              # Mass from Nubase
        self.ZAID = ZAID              # Nubase ID
        self.excitation_level = excitation_level   # excitation energy [keV], 0 for ground states
        self.symbol = symbol              # e.g. "He4"
        self.abundance = abundance    # natural abundance in %
        self.decay = decay            # decay time

    def lines(self, radiation=None):
        """Decay lines of this nuclide (emissions.lines): radiation, energy [eV], intensity."""
        from materials.isotopes import emissions
        return emissions.lines(self, radiation)

    def gamma_lines(self):
        """Gamma lines: energy [eV], intensity per decay (emissions.gamma_lines)."""
        from materials.isotopes import emissions
        return emissions.gamma_lines(self)

    def beta_endpoints(self):
        """Beta branches: radiation, endpoint energy [eV], intensity (emissions.beta_endpoints)."""
        from materials.isotopes import emissions
        return emissions.beta_endpoints(self)

    def alpha_lines(self):
        """Alpha lines: energy [eV], intensity per decay (emissions.alpha_lines)."""
        from materials.isotopes import emissions
        return emissions.alpha_lines(self)

    def __repr__(self):
        return f"{self.symbol}"