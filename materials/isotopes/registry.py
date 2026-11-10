import math

import pandas as pd
from materials.isotopes.isotope import Isotope
from .element import Element
import importlib.resources as pkg_resources

_isotope_registry = {}
_element_registry = {}
nubase = None

def _load_nubase():
    """Load Nubase only once; adds the element symbol of each row (column 'element')."""
    global nubase
    if nubase is None:
        with pkg_resources.path("materials.library", "nubase2020.csv") as path:
            nubase = pd.read_csv(path)
        nubase["element"] = nubase.symbol.str.extract(r"^([A-Z][a-z]?)")[0]
    return nubase


def _decay_constant(half_life: float):
    """ln2 / half-life [1/s]; None when stable or unknown."""
    return math.log(2) / half_life if 0 < half_life < math.inf else None

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
        excitation_level=None if pd.isna(row.get("excitation")) else row.excitation,
        abundance=None if pd.isna(row.abundance) else row.abundance,
        decay=_decay_constant(row.half_life)
    )
    _isotope_registry[symbol] = iso
    return iso


def load_element(symbol: str):
    """Return Element object (loads all isotopes of element)."""
    if symbol in _element_registry:
        return _element_registry[symbol]

    nubase_df = _load_nubase()
    isotope_rows = nubase_df[nubase_df.element == symbol]

    if isotope_rows.empty:
        raise AttributeError(f"No element {symbol}")
    z = int(isotope_rows.Z.iloc[0])

    mass = 0
    abundance_dict = {}
    for _, row in isotope_rows.iterrows():
        iso = load_isotope(row.symbol)
        if not (iso.abundance is None):
            mass += iso.mass * iso.abundance/100
            abundance_dict[iso] = iso.abundance

    element = Element(
        Z=z,
        ZAID=z * 1000,
        symbol=symbol,
        mass=mass,
        abundance=abundance_dict)

    _element_registry[symbol] = element
    return element
