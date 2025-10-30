from materials.isotopes.isotope import Isotope
from materials.isotopes.element import Element
from materials.isotopes import registry
import re

def __getattr__(name: str):
    """
    Dynamically load isotopes or elements.
    If the name contains a number → isotope, else → element.
    """
    # Check if the name has any digits
    if re.search(r'\d', name):
        # It's an isotope
        try:
            return registry.load_isotope(name)
        except AttributeError:
            raise AttributeError(f"No isotope named '{name}' in registry")
    else:
        # It's an element
        try:
            return registry.load_element(name)
        except AttributeError:
            raise AttributeError(f"No element named '{name}' in registry")

def __dir__():
    """Return available isotopes and elements for tab-completion."""
    return list(registry._isotope_registry.keys()) + list(registry._element_registry.keys())