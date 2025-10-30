import pandas as pd
from materials.isotopes.isotope import Isotope
from .element import Element
import importlib.resources as pkg_resources

_isotope_registry = {}
_element_registry = {}
nubase = None
elements = None

def _load_nubase():
    """Load Nubase only once."""
    global nubase
    with pkg_resources.path("materials.library", "nubase2020.csv") as nubase:
        nubase = pd.read_csv(nubase)
    return nubase

def _load_elements():
    """Load Nubase only once."""
    global elements
    with pkg_resources.path("materials.library", "elements.csv") as elements:
        elements = pd.read_csv(elements)
    return elements

def load_isotope(symbol: str):
    """Return Isotope object by e.g. 'He4' or 'H3'."""
    if symbol in _isotope_registry:
        return _isotope_registry[symbol]

    df = _load_nubase()
    row = df[df.symbol == symbol]
    if row.empty:
        raise AttributeError(f"No isotope {symbol}")
    row = row.squeeze()

    iso = Isotope(
        Z=row.Z,
        A=row.A,
        ZAID=row.ZAID,
        symbol=row.symbol,
        mass= row.mass,
        abundance=None if pd.isna(row.abundance) else row.abundance,
        decay=None if pd.isna(row.decay) else row.decay
    )
    _isotope_registry[symbol] = iso
    return iso


def load_element(symbol: str):
    """Return Element object (loads all isotopes of element)."""
    if symbol in _element_registry:
        return _element_registry[symbol]

    elements_df = _load_elements()
    element_row = elements_df[elements_df.element == symbol]

    if element_row.empty:
        raise AttributeError(f"No element {symbol}")

    nubase_df = _load_nubase()
    isotope_rows = nubase_df[nubase_df.Z == element_row.Z.item()]

    mass = 0
    abundance_dict = {}
    for _, row in isotope_rows.iterrows():
        iso = load_isotope(row.symbol)
        if not (iso.abundance is None):
            mass += iso.mass * iso.abundance/100
            abundance_dict[iso] = iso.abundance

    element = Element(
        Z = element_row.Z.item(),
        ZAID=element_row.Z.item() * 1000,
        symbol=element_row.element.item(),
        mass=mass,
        abundance=abundance_dict)

    _element_registry[element_row.element.item()] = element
    return element
