"""Decay emission lines of radionuclides: gamma and X-ray lines, beta endpoints, alpha lines.

    from materials.isotopes import Co60, emissions
    Co60.gamma_lines()                     # DataFrame: energy [eV], intensity [per decay]
    emissions.photon_lines("Na22")         # gamma + xray + annihilation (511 keV)
    emissions.beta_endpoints("Cu64")       # beta- and beta+ branches: radiation, endpoint energy, intensity
    emissions.alpha_lines("Am241")
    emissions.lines((47, 110, 1))          # every line of ENDF's Ag-110m1 (250 d)

Data: the ENDF/B-VIII.1 decay sublibrary, discrete spectra (MF8/MT457), bundled as
library/decay_lines.csv.gz (built by sources/endf_decay.ipynb). Per decay:
    gamma, xray      photon energy, photons per decay
    annihilation     511 keV, photons per decay (ENDF's 511 keV X-ray entries, ~2 x positrons)
    beta-            endpoint energy of each branch, branch intensity
    beta+            positron endpoint (transition energy - 2 m_e c^2), positrons per decay
    alpha            alpha energy, alphas per decay
A nuclide with no row (stable, or no discrete data) gives an empty table.

Nuclides, in two numberings of isomers:
    NUBASE (this package)   a symbol ("Co60", "Ag110n") or a materials Isotope: looked up in the
                            registry; an isomer is translated to its ENDF state through
                            library/endf_states.csv (matched by excitation energy, else half-life)
    ENDF                    a (Z, A, m) tuple or an object with Z, A and m (an isotopes ZAID), m = LISO
The two differ for ~50 isomers: NUBASE's Ag110m is a 0.66 us level, its Ag110n is ENDF's (47, 110, 1).
A NUBASE isomer without an ENDF state raises LookupError.
"""
from functools import lru_cache
import importlib.resources as pkg_resources

import pandas as pd

from materials.isotopes import registry

RADIATIONS = ("gamma", "xray", "annihilation", "beta-", "beta+", "alpha")
PHOTONS = ("gamma", "xray", "annihilation")


def lines(nuclide, radiation=None) -> pd.DataFrame:
    """Lines of a nuclide: columns radiation, energy [eV], intensity [per decay], sorted by
    energy; radiation: one of RADIATIONS or a tuple of them (default: all)."""
    z, a, m = _key(nuclide)
    table = _table()
    rows = table[(table.Z == z) & (table.A == a) & (table.m == m)]
    if radiation is not None:
        kinds = (radiation,) if isinstance(radiation, str) else tuple(radiation)
        unknown = set(kinds) - set(RADIATIONS)
        if unknown:
            raise ValueError(f"unknown radiation {sorted(unknown)}; choose from {RADIATIONS}")
        rows = rows[rows.radiation.isin(kinds)]
    return rows[["radiation", "energy", "intensity"]].sort_values("energy").reset_index(drop=True)


def gamma_lines(nuclide) -> pd.DataFrame:
    """Gamma lines: energy [eV], intensity [per decay]."""
    return lines(nuclide, "gamma")[["energy", "intensity"]]


def photon_lines(nuclide) -> pd.DataFrame:
    """Every photon: gamma, X-ray and annihilation lines (radiation, energy, intensity)."""
    return lines(nuclide, PHOTONS)


def beta_endpoints(nuclide) -> pd.DataFrame:
    """Beta branches: radiation (beta- / beta+), endpoint energy [eV], intensity."""
    return lines(nuclide, ("beta-", "beta+"))


def alpha_lines(nuclide) -> pd.DataFrame:
    """Alpha lines: energy [eV], intensity [per decay]."""
    return lines(nuclide, "alpha")[["energy", "intensity"]]


def _key(nuclide) -> tuple[int, int, int]:
    """(Z, A, m) in ENDF numbering of a NUBASE symbol or Isotope, a tuple or a ZAID."""
    if isinstance(nuclide, tuple):
        z, a, m = (tuple(nuclide) + (0,))[:3]
        return int(z), int(a), int(m)
    if isinstance(nuclide, str):
        try:
            nuclide = registry.load_isotope(nuclide)
        except AttributeError:
            raise ValueError(f"{nuclide!r} is not a NUBASE symbol (e.g. 'Co60', 'Ag110n'); "
                             "for ENDF numbering give (Z, A, m)") from None
    if hasattr(nuclide, "m"):           # isotopes ZAID / Isotope: ENDF numbering
        return int(nuclide.Z), int(nuclide.A), int(nuclide.m)
    return _endf_state(nuclide.symbol, int(nuclide.Z), int(nuclide.A), int(nuclide.ZAID))


def _endf_state(symbol: str, z: int, a: int, zaid: int) -> tuple[int, int, int]:
    """The ENDF state of a NUBASE state (endf_states.csv); a ground state is m = 0."""
    states = _states()
    found = states[states.nubase == symbol]
    if len(found):
        row = found.iloc[0]
        return int(row.Z), int(row.A), int(row.m)
    if zaid == 1000 * z + a:
        return z, a, 0
    raise LookupError(f"NUBASE state {symbol} has no ENDF decay state (see library/endf_states.csv)")


@lru_cache(maxsize=1)
def _states() -> pd.DataFrame:
    with pkg_resources.as_file(pkg_resources.files("materials.library") / "endf_states.csv") as path:
        return pd.read_csv(path, keep_default_na=False, na_values={"excitation": [""], "half_life": [""]})


@lru_cache(maxsize=1)
def _table() -> pd.DataFrame:
    with pkg_resources.as_file(pkg_resources.files("materials.library") / "decay_lines.csv.gz") as path:
        return pd.read_csv(path, comment="#")
