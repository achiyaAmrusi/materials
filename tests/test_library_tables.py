"""The bundled tables built by sources/nubase.ipynb and sources/endf_decay.ipynb."""
import importlib.resources as pkg_resources
import math

import pandas as pd
import pytest

from materials.isotopes import registry


def _csv(name, **kw):
    with pkg_resources.as_file(pkg_resources.files("materials.library") / name) as path:
        return pd.read_csv(path, **kw)


@pytest.fixture(scope="module")
def nubase():
    return _csv("nubase2020.csv").set_index("symbol")


def test_nubase_symbols_unique_and_x_isomers_kept(nubase):
    assert nubase.index.is_unique
    assert nubase.loc["Lu174", "half_life"] == pytest.approx(3.31 * 365.2422 * 86400, rel=1e-6)
    assert nubase.loc["Lu174m", "excitation"] == pytest.approx(170.83)
    assert "Lu174x" in nubase.index                # NUBASE's letter x (state 6)


def test_nubase_units_and_abundances(nubase):
    assert nubase.loc["H4", "half_life"] == pytest.approx(1.39e-22)    # 'ys' is yoctoseconds
    assert nubase.loc["Bi209", "abundance"] == 100.0
    assert nubase.loc["Al27", "half_life"] == math.inf and "decay" not in nubase.columns
    assert "Cu76m" not in nubase.index             # NUBASE: non-existent state


def test_registry_decay_constant_from_half_life():
    assert registry.load_isotope("Na24").decay == pytest.approx(math.log(2) / (14.956 * 3600), rel=1e-3)
    assert registry.load_isotope("Al27").decay is None


def test_registry_carries_excitation():
    assert registry.load_isotope("Na24m").excitation_level == pytest.approx(472.207)
    assert registry.load_isotope("Co60").excitation_level == 0


def test_endf_states_match():
    states = _csv("endf_states.csv", keep_default_na=False)
    row = states[(states.Z == 47) & (states.A == 110) & (states.m == 1)].iloc[0]
    assert (row.nubase, row.match) == ("Ag110n", "energy")
    named = states[states.nubase != ""]
    assert named.nubase.is_unique
    assert set(states.match) <= {"ground", "energy", "half-life", "none", "ambiguous"}
