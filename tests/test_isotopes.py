"""Tests for materials.isotopes: registry loading and lazy attribute access."""

import pytest

from materials.isotopes import registry
from materials.isotopes.element import Element
from materials.isotopes.isotope import Isotope


def test_load_element_hydrogen():
    h = registry.load_element("H")
    assert isinstance(h, Element)
    assert h.Z == 1
    assert h.symbol == "H"
    assert 1.0 < h.mass < 1.1  # natural-abundance-weighted mass [amu]


def test_load_element_is_cached():
    a = registry.load_element("O")
    b = registry.load_element("O")
    assert a is b


def test_load_isotope_h1():
    h1 = registry.load_isotope("H1")
    assert isinstance(h1, Isotope)
    assert h1.Z == 1
    assert h1.A == 1
    assert h1.symbol == "H1"


def test_load_isotope_is_cached():
    a = registry.load_isotope("He4")
    b = registry.load_isotope("He4")
    assert a is b


def test_unknown_element_raises():
    with pytest.raises(AttributeError):
        registry.load_element("Xx")


def test_unknown_isotope_raises():
    with pytest.raises(AttributeError):
        registry.load_isotope("Xx99")


def test_module_getattr_dispatches_by_digit():
    # materials.isotopes.__getattr__: no digit -> element, digit -> isotope
    import materials.isotopes as isotopes

    h = isotopes.H
    assert isinstance(h, Element) and h.Z == 1

    h1 = isotopes.H1
    assert isinstance(h1, Isotope) and h1.A == 1


def test_element_mass_is_abundance_weighted_average():
    # element mass should sit between its isotopes' masses, not equal any
    # single isotope's mass exactly (it's a natural-abundance average)
    cl = registry.load_element("Cl")
    assert 34.0 < cl.mass < 37.0
