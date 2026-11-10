# sources: where the bundled tables come from

The package ships tables in `materials/library/`. Each is built by one notebook here, from raw data in
`raw/`. Run a notebook from this directory to rebuild its tables. The notebooks explain every step, so
they are also the documentation of the tables.

| notebook | reads | writes (`materials/library/`) |
|---|---|---|
| `nubase.ipynb` | `raw/nubase_4.mas20.txt` | `nubase2020.csv`: one row per nuclide or excited state: Z, A, ZAID, symbol, mass, excitation, half-life, abundance. Elements and decay constants are derived from it by the registry |
| `endf_decay.ipynb` | the ENDF/B-VIII.1 decay sublibrary (`ENDF_DECAY_DIR`; not in this repo, about 3,800 files) | `decay_lines.csv.gz`: gamma, X-ray, annihilation, beta endpoint and alpha lines per decay. `endf_states.csv`: every ENDF state with its NUBASE name |

Run `nubase.ipynb` first: `endf_decay.ipynb` matches the ENDF states to its table. The notebooks need
pandas and numpy, and `endf_decay.ipynb` also needs openmc. The package itself needs only pandas.

## raw/

| file | what | source | used by |
|---|---|---|---|
| `nubase_4.mas20.txt` | NUBASE2020: masses, excitation energies, half-lives, spins, decay modes, abundances | Kondev et al., Chin. Phys. C 45, 030001 (2021); AMDC, https://www-nds.iaea.org/amdc/ | `nubase.ipynb` |
| `nndc_nudat_data_export.csv` | NuDat 3 export (NNDC): ground and isomeric states with half-lives, decay modes and branchings, mass excess, Q-values and separation energies | https://www.nndc.bnl.gov/nudat3/ | nothing yet; kept as a reference |

## Isomer numbering

NUBASE and ENDF number isomers differently:
- **NUBASE** labels every excited state: the index i in the `ZZZi` column, or the letters m, n, p, q, r, x.
  This includes short-lived levels.
- **ENDF** numbers only the states that have their own decay file (LISO).

Ag-110 is an example. NUBASE's `Ag110m` is a 0.66 µs level, and its `Ag110n` is the 250 d isomer, which
is ENDF's m = 1.

`endf_decay.ipynb` matches the two:
- by excitation energy, within max(2 keV, 1%);
- else by half-life, within 25%.

`materials.isotopes.emissions` uses that table, so `emissions.lines("Ag110n")` gives the 250 d isomer's
lines.
