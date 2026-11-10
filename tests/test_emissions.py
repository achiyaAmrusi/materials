"""Decay lines from the bundled ENDF/B-VIII.1 table, against well-known values."""
import pytest

from materials.isotopes import Co60, Na24, emissions


def _line(df, energy_kev, tol_kev=1.0):
    near = df[(df.energy - energy_kev * 1e3).abs() < tol_kev * 1e3]
    assert len(near) == 1, near
    return near.iloc[0]


def test_co60_gammas_and_beta():
    g = Co60.gamma_lines()
    assert _line(g, 1173.2).intensity == pytest.approx(0.9985, abs=1e-3)
    assert _line(g, 1332.5).intensity == pytest.approx(0.9998, abs=1e-3)
    b = Co60.beta_endpoints()
    assert _line(b, 318.1).intensity == pytest.approx(0.9988, abs=1e-3)


def test_na24_by_symbol_tuple_and_object():
    a = emissions.gamma_lines("Na24")
    assert a.equals(emissions.gamma_lines((11, 24, 0))) and a.equals(Na24.gamma_lines())
    assert _line(a, 1368.6).intensity == pytest.approx(1.0, abs=1e-3)
    assert _line(a, 2754.0).intensity == pytest.approx(0.9986, abs=1e-3)


def test_isomer_numbering_nubase_to_endf():
    """NUBASE names are translated to ENDF states: Na24m is ENDF m=1 (472 keV IT); NUBASE's Ag110m
    is a 0.66 us level, its Ag110n is ENDF's 250 d Ag-110m1."""
    assert emissions.gamma_lines("Na24m").equals(emissions.gamma_lines((11, 24, 1)))
    assert _line(emissions.gamma_lines((11, 24, 1)), 472.2).intensity > 0.4
    ag = emissions.gamma_lines("Ag110n")
    assert ag.equals(emissions.gamma_lines((47, 110, 1))) and _line(ag, 657.8).intensity > 0.9
    with pytest.raises(LookupError):
        emissions.lines("Ag110m")


def test_positron_emitter():
    """Na-22: beta+ endpoint 546 keV (90 %), annihilation photons 2 x 0.90."""
    b = emissions.beta_endpoints("Na22")
    plus = b[b.radiation == "beta+"]
    assert _line(plus, 546.4).intensity == pytest.approx(0.899, abs=2e-3)
    ann = emissions.lines("Na22", "annihilation")
    assert ann.energy.iloc[0] == pytest.approx(510999, rel=1e-5)
    assert ann.intensity.iloc[0] == pytest.approx(2 * 0.8995, abs=3e-3)
    assert set(emissions.photon_lines("Na22").radiation) >= {"gamma", "annihilation"}


def test_alpha_and_pure_beta():
    assert _line(emissions.alpha_lines("Am241"), 5485.6).intensity == pytest.approx(0.848, abs=1e-3)
    assert emissions.gamma_lines("P32").empty
    assert _line(emissions.beta_endpoints("P32"), 1710.5).intensity == pytest.approx(1.0)


def test_stable_and_bad_input():
    assert emissions.lines("Al27").empty
    with pytest.raises(ValueError):
        emissions.lines("Na24", "neutrino")
    with pytest.raises(ValueError):
        emissions.lines("24Na")
    with pytest.raises(ValueError):
        emissions.lines("Na24m1")          # ENDF-style name: give (11, 24, 1)
