# Materials: material description in Python for nuclear data and calculations

---

## **Overview**

Materials is one part of a future project: a convenient toolkit for basic nuclear science. It
provides:
- **isotopes and elements** from NUBASE2020: masses, excitation energies, half-lives, natural
  abundances;
- their **decay emission lines** from ENDF/B-VIII.1: gamma, X-ray and annihilation photons, beta
  endpoints, alpha lines;
- **materials**: compositions by atomic or mass fractions, with a density.

The only dependency is pandas: all data ships with the package as tables.

---

## **Install**

```bash
pip install git+ssh://git@github.com/achiyaAmrusi/materials.git
```

For development, as an editable install that PyCharm can see:
```bash
pip install --no-deps --no-build-isolation -e . --config-settings editable_mode=compat
```

---

## **Isotopes and elements**

```python
from materials.isotopes import Co60, Na24m, H
Co60.mass, Co60.decay              # 59.9338 u, ln2 / half-life [1/s]
Na24m.excitation_level             # 472.2 keV: Na-24's isomer
H.abundance, H.mass                # {H1: 99.9855, H2: 0.0145} [%], abundance-weighted mass [u]
```

Every NUBASE2020 nuclide and excited state is an attribute of `materials.isotopes`, loaded on first
use. Elements are the symbols without a mass number (`H`, `Fe`).

An `Isotope` has:

| attribute | value |
|---|---|
| `Z`, `A` | atomic and mass number |
| `symbol` | element + A + NUBASE state letter: `Co60`, `Na24m`, `Ag110n` |
| `ZAID` | `1000 Z + A`; `10 (1000 Z + A) + i` for NUBASE's excited state i |
| `mass` | atomic mass [u] |
| `excitation_level` | [keV]; 0 for ground states |
| `decay` | ln2 / half-life [1/s]; `None` if stable or unknown |
| `abundance` | natural abundance [%] |

An `Element` has `Z`, `symbol`, `mass` and `abundance` (`{Isotope: %}`).

---

## **Decay emission lines**

```python
from materials.isotopes import Co60, emissions
Co60.gamma_lines()                  # energy [eV], intensity [per decay]
Co60.beta_endpoints()               # radiation (beta-/beta+), endpoint energy [eV], intensity
emissions.photon_lines("Na22")      # gamma + X-ray + annihilation (511 keV)
emissions.alpha_lines("Am241")
emissions.lines((47, 110, 1))       # every line of a state, by ENDF numbering (Z, A, m)
```

The lines come from the ENDF/B-VIII.1 decay sublibrary's discrete spectra (MF8/MT457), per decay:

| radiation | energy | intensity |
|---|---|---|
| `gamma`, `xray` | photon energy | photons per decay |
| `annihilation` | 511 keV | photons per decay (≈ 2 × the positron intensity) |
| `beta-` | endpoint energy of each branch | branch intensity |
| `beta+` | positron endpoint | positrons per decay (electron capture excluded) |
| `alpha` | alpha energy | alphas per decay |

A stable nuclide, or one without discrete data, gives an empty table.

### Isomer names: NUBASE and ENDF

NUBASE names every excited state, including short-lived levels. ENDF numbers only the states that have
decay data (m = LISO). So the two differ for about 50 isomers. Ag-110 is an example:
- NUBASE's `Ag110m` is a 0.66 µs level, which ENDF doesn't have;
- NUBASE's `Ag110n` is the 250 d isomer, which ENDF calls m = 1.

Lookups accept both numberings:
- **NUBASE:** a symbol (`"Ag110n"`) or an `Isotope`. It's translated to its ENDF state through
  `library/endf_states.csv`, where the states were matched by excitation energy, else by half-life.
  A NUBASE state with no ENDF decay data raises `LookupError`.
- **ENDF:** a `(Z, A, m)` tuple, or any object with `Z`, `A` and `m`.

---

## **Materials**

```python
from materials import Material
from materials.isotopes import H, O
water = Material("water", composition={H: 2, O: 1}, fraction_type="atomic", density=1.0)
water.update_fraction_type("mass")      # {H: 0.112, O: 0.888} by mass
```

A composition can mix isotopes and elements. The fractions are relative and get normalized. The
density is in g/cm³. `materials.matlib` has ready materials: air, water, concrete, metals,
stainless steel, glass, detectors, thermoplastics.

---

## **Layout**

| path | what |
|---|---|
| `materials/material.py` | `Material` |
| `materials/isotopes/` | `Isotope`, `Element`, the registry (loads `nubase2020.csv`), `emissions` |
| `materials/matlib/` | ready materials |
| `materials/library/` | the bundled tables (below) |
| `sources/` | the notebooks that build the tables, and their raw data |
| `examples/user_example.ipynb` | a tour of the package |

---

## **Data tables**

The package ships three tables in `materials/library/`:

| table | from | content |
|---|---|---|
| `nubase2020.csv` | NUBASE2020 (Kondev et al., Chin. Phys. C 45, 030001 (2021)) | one row per nuclide or excited state: Z, A, ZAID, symbol, mass, excitation, half-life, abundance |
| `decay_lines.csv.gz` | ENDF/B-VIII.1 decay sublibrary | the emission lines above |
| `endf_states.csv` | both | every ENDF decay state with its NUBASE name and how it was matched |

They are built by the notebooks in `sources/` (`nubase.ipynb`, then `endf_decay.ipynb`), which
document each step. See `sources/README.md` for the raw files and how to rebuild them.

---

## **Tests**

```bash
pytest tests
```
The tests cover the isotopes and materials, the emission lines against known values (Co-60, Na-24,
Na-22, Am-241, P-32), the isomer naming, and the bundled tables.
