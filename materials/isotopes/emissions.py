"""Decay emission lines of radionuclides: gamma and X-ray lines, beta endpoints, alpha lines.

    from materials.isotopes import emissions
    emissions.gamma_lines("Co60")          # DataFrame: energy [eV], intensity [per decay]
    emissions.photon_lines("Na22")         # gamma + xray + annihilation (511 keV)
    emissions.beta_endpoints("Cu64")       # beta- and beta+ branches: radiation, endpoint energy, intensity
    emissions.alpha_lines("Am241")
    emissions.lines((11, 24, 1))           # every line of Na-24m1

Data: the ENDF/B-VIII.1 decay sublibrary, discrete spectra (MF8/MT457), bundled as
library/decay_lines.csv.gz (made by scripts/make_decay_lines.py). Per decay:
    gamma, xray      photon energy, photons per decay
    annihilation     511 keV, photons per decay (ENDF's 511 keV X-ray entries, ~2 x positrons)
    beta-            endpoint energy of each branch, branch intensity
    beta+            positron endpoint (transition energy - 2 m_e c^2), positrons per decay
    alpha            alpha energy, alphas per decay
A nuclide with no row (stable, or no discrete data) gives an empty table.

Nuclides: a symbol ("Co60", "Na24m1"), a (Z, A, m) tuple, or an object with Z and A (and m, or
the materials package's ZAID). Isomers are numbered as ENDF numbers them (m = LISO). NUBASE,
behind this package's Isotope objects, numbers some isomers differently (its "Na24m" is ENDF's
Na24m1, but for ~100 nuclides the m differs), so for isomers prefer (Z, A, m) taken from ENDF.
"""
import re
from functools import lru_cache
import importlib.resources as pkg_resources

import pandas as pd

RADIATIONS = ("gamma", "xray", "annihilation", "beta-", "beta+", "alpha")
PHOTONS = ("gamma", "xray", "annihilation")
_SYMBOL = re.compile(r"^([A-Z][a-z]?)(\d+)(?:m(\d*))?$")


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
    """(Z, A, m) of a symbol, a tuple or an object with Z and A."""
    if isinstance(nuclide, tuple):
        z, a, m = (tuple(nuclide) + (0,))[:3]
        return int(z), int(a), int(m)
    if isinstance(nuclide, str):
        match = _SYMBOL.match(nuclide)
        if match is None:
            raise ValueError(f"not a nuclide symbol: {nuclide!r} (e.g. 'Co60', 'Na24m1')")
        element, a, m = match.groups()
        m = 0 if m is None else int(m or 1)
        return _atomic_number(element), int(a), m
    z, a = int(nuclide.Z), int(nuclide.A)
    m = getattr(nuclide, "m", None)
    if m is None:       # materials Isotope: ZAID is Z*1000+A, or (Z*1000+A)*10+m for isomers
        zaid = int(getattr(nuclide, "ZAID", z * 1000 + a))
        m = zaid % 10 if zaid >= 10000 * z + 10 * a else 0
    return z, a, int(m)


@lru_cache(maxsize=None)
def _atomic_number(element: str) -> int:
    with pkg_resources.as_file(pkg_resources.files("materials.library") / "nubase2020.csv") as path:
        nubase = pd.read_csv(path, usecols=["Z", "symbol"])
    symbols = nubase.symbol.str.extract(r"^([A-Z][a-z]?)")[0]
    found = nubase.Z[symbols == element]
    if found.empty:
        raise ValueError(f"unknown element {element!r}")
    return int(found.iloc[0])


@lru_cache(maxsize=1)
def _table() -> pd.DataFrame:
    with pkg_resources.as_file(pkg_resources.files("materials.library") / "decay_lines.csv.gz") as path:
        return pd.read_csv(path, comment="#")
