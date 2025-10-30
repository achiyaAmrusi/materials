from materials.isotopes import Isotope, Element
from typing import Dict

class Material:

    def __init__(self, name:str, composition:Dict, fraction_type="atomic", density= 1.0):
        """
        A material composed of isotopes or elements.

        Parameters
        ----------
        name: str
        The name of the material
        composition : dict
            Keys are Isotope or Element objects.
            Values are numbers representing fractions (relative, not normalized).
        density : float, optional
            Material density in g/cm^3
        fraction_type : str
            "atomic" → fractions are atomic ratios
            "mass" → fractions are mass fractions
        """
        self.name=name
        self.composition = self._normalize_fractions(composition)
        self._fraction_type = fraction_type
        self.density = density


    def _expand(self):
        """Expand elements into the isotope natural abundance."""
        expanded = {}
        for component, value in self.composition.items():
            if isinstance(component, Element):
                for iso, abundance in component.abundance.items():
                    frac = abundance / 100 * value # weighted by abundance
                    expanded[iso] = expanded.get(component, 0)  + frac
            elif isinstance(component, Isotope):
                expanded[component] = expanded.get(component, 0) + value
            else:
                raise TypeError(f"Invalid component {component}")
        return expanded

    def _normalize_fractions(self, composition):
        """Normalize fractions according to fraction_type."""
        total = sum(composition.values())
        if total == 0:
            return composition
        return {iso: frac / total for iso, frac in composition.items()}

    def _average_mass(self):
        """Compute the weighted average mass of the material in amu."""
        mass = 0
        for iso, frac in self.composition .items():
            mass += iso.mass * frac
        return mass

    def __repr__(self):
        parts = [f"{iso.symbol}:{frac:.3f}" for iso, frac in self.composition.items()]
        return f"<Material name={self.name}, density={self.density} g/cm^3, composition={{{', '.join(parts)}}} [{self._fraction_type}]>"

    def get_mass_fraction(self, isotope):
        """Return mass fraction of a specific isotope in the material."""
        fraction = 0.0
        if isotope not in self.composition:
            return fraction

        if self._fraction_type == 'mass':
            fraction = self.composition[isotope]
        else:
            total_mass = sum(iso.mass * frac for iso, frac in self.composition.items())
            fraction =isotope.mass * self.composition[isotope] / total_mass

        return fraction

    def update_fraction_type(self, fraction_type):
        """Return a new Material object with composition converted to a new fraction type.

        Parameters
        ----------
        fraction_type : str
            "atomic" → fractions are atomic ratios
            "mass" → fractions are mass fractions
        """
        if fraction_type == self._fraction_type:
            return self  # already in this type

        if fraction_type == "mass" and self._fraction_type == "atomic":
            # atomic → mass fractions
            total_mass = sum(iso.mass * frac for iso, frac in self.composition.items())
            new_composition = {iso: iso.mass * frac / total_mass for iso, frac in self.composition.items()}

        elif fraction_type == "atomic" and self._fraction_type == "mass":
            # mass fractions → atomic fractions
            total_atoms = sum(frac / iso.mass for iso, frac in self.composition.items())
            new_composition = {iso: frac / iso.mass / total_atoms for iso, frac in self.composition.items()}
        else:
            raise ValueError(f"Unsupported fraction_type: {fraction_type}")

        # Return a new Material object
        return Material(
            name=self.name,
            composition=new_composition,
            fraction_type=fraction_type,
            density = self.density)
