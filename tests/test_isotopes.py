"""Tests for materials.isotopes: the public import surface.

The intended usage is `from materials.isotopes import H2` (or any other
element/isotope symbol) -- materials.isotopes.__getattr__ dispatches to
the registry, loading an Element if the name has no digit or an Isotope
if it does. These tests exercise that same clean import style rather
than reaching into the registry internals directly.
"""

import pytest

from materials.isotopes import H, O, Cl, H2, He4
from materials.isotopes.element import Element
from materials.isotopes.isotope import Isotope


def test_import_element_by_symbol():
    assert isinstance(H, Element)
    assert H.Z == 1
    assert H.symbol == "H"
    assert 1.0 < H.mass < 1.1  # natural-abundance-weighted mass [amu]


def test_import_isotope_by_symbol():
    assert isinstance(H2, Isotope)  # deuterium
    assert H2.Z == 1
    assert H2.A == 2
    assert H2.symbol == "H2"


def test_imported_elements_are_cached_singletons():
    from materials.isotopes import O as O_again
    assert O is O_again


def test_imported_isotopes_are_cached_singletons():
    from materials.isotopes import He4 as He4_again
    assert He4 is He4_again


def test_unknown_element_import_fails():
    with pytest.raises(ImportError):
        from materials.isotopes import Xx  # noqa: F401


def test_unknown_isotope_import_fails():
    with pytest.raises(ImportError):
        from materials.isotopes import Xx99  # noqa: F401


def test_element_mass_is_abundance_weighted_average():
    # element mass should sit between its isotopes' masses, not equal any
    # single isotope's mass exactly (it's a natural-abundance average)
    assert 34.0 < Cl.mass < 37.0
