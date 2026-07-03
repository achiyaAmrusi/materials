"""Tests for materials.Material: composition normalization and fraction conversion."""

import pytest

from materials import Material
from materials.isotopes import H, O, C


def test_composition_is_normalized():
    # un-normalized atomic ratios (water: H2O) should normalize to sum 1
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    assert sum(water.composition.values()) == pytest.approx(1.0)
    assert water.composition[H] == pytest.approx(2.0 / 3.0)
    assert water.composition[O] == pytest.approx(1.0 / 3.0)


def test_get_mass_fraction_from_atomic():
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    # mass fraction of O in water should be close to 16/18 ~ 0.888
    assert water.get_mass_fraction(O) == pytest.approx(0.888, abs=0.01)


def test_get_mass_fraction_missing_component_is_zero():
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    assert water.get_mass_fraction(C) == 0.0


def test_update_fraction_type_atomic_to_mass_sums_to_one():
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    water_mass = water.update_fraction_type("mass")
    assert water_mass._fraction_type == "mass"
    assert sum(water_mass.composition.values()) == pytest.approx(1.0)


def test_update_fraction_type_round_trip():
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    round_tripped = water.update_fraction_type("mass").update_fraction_type("atomic")
    assert round_tripped.composition[H] == pytest.approx(water.composition[H], rel=1.0e-6)
    assert round_tripped.composition[O] == pytest.approx(water.composition[O], rel=1.0e-6)


def test_update_fraction_type_is_noop_when_same():
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    assert water.update_fraction_type("atomic") is water


def test_repr_does_not_crash():
    water = Material(name="water", composition={H: 2, O: 1},
                      fraction_type="atomic", density=1.0)
    assert "water" in repr(water)
