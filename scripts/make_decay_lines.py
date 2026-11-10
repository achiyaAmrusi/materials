"""Write materials/library/decay_lines.csv.gz from an ENDF-6 decay sublibrary.

    python scripts/make_decay_lines.py <decay directory> [--evaluation "ENDF/B-VIII.1"]

Needs openmc (openmc.data.Evaluation and Decay; only for this script, the materials package reads
the table with pandas).
One row per line (MF8/MT457 discrete spectra, intensities per decay times the discrete
normalization):

    radiation      energy                               intensity
    gamma          photon energy                        photons per decay
    xray           photon energy                        photons per decay
    annihilation   511 keV                              photons per decay (ENDF lists them as
                                                        X-rays at 511 keV; relabelled here)
    beta-          endpoint energy of the branch        branch intensity
    beta+          endpoint = transition energy - 2 m_e c^2   positrons per decay (EC excluded)
    alpha          alpha energy                         alphas per decay

Nuclides are numbered as the ENDF files number them (m = LISO, the isomer number).
"""
import argparse
import gzip
import warnings
from pathlib import Path

from openmc.data import Decay, Evaluation

TWO_ME = 1.02199895e6       # eV, 2 m_e c^2
HALF_ME = 0.510998950e6     # eV
KINDS = {"gamma": "gamma", "xray": "xray", "beta-": "beta-", "alpha": "alpha"}   # openmc's spectrum keys


def nominal(x) -> float:
    return float(getattr(x, "nominal_value", x))


def rows(decay: Decay):
    for key, spectrum in decay.spectra.items():
        norm = nominal(spectrum.get("discrete_normalization", 1.0))
        lines = spectrum.get("discrete") or []
        if key in KINDS:
            for line in lines:
                energy = nominal(line["energy"])
                kind = "annihilation" if key == "xray" and abs(energy - HALF_ME) < 10.0 else KINDS[key]
                yield kind, energy, norm * nominal(line["intensity"])
        elif key == "ec/beta+":
            for line in lines:
                p = norm * nominal(line.get("positron_intensity", 0.0))
                if p > 0:
                    yield "beta+", nominal(line["energy"]) - TWO_ME, p


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("decay_dir", type=Path)
    parser.add_argument("--evaluation", default="ENDF/B-VIII.1")
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).resolve().parents[1] / "materials/library/decay_lines.csv.gz")
    args = parser.parse_args()
    warnings.filterwarnings("ignore", message="Using UFloat objects with std_dev==0")

    out, skipped = [], []
    for path in sorted(p for p in args.decay_dir.iterdir() if p.is_file()):
        try:
            evaluation = Evaluation(path)
            decay = Decay(evaluation)
        except Exception as e:          # noqa: BLE001 - report and go on
            skipped.append(f"{path.name}: {e}")
            continue
        z, a, m = decay.nuclide["atomic_number"], decay.nuclide["mass_number"], decay.nuclide["isomeric_state"]
        for radiation, energy, intensity in rows(decay):
            if intensity > 0:
                out.append(f"{z},{a},{m},{radiation},{energy:.6g},{intensity:.6g}")

    with gzip.open(args.out, "wt") as fh:
        fh.write(f"# {args.evaluation} decay data, discrete lines; energy [eV], intensity per decay\n")
        fh.write("Z,A,m,radiation,energy,intensity\n")
        fh.write("\n".join(out) + "\n")
    print(f"{len(out)} lines -> {args.out}")
    if skipped:
        print(f"skipped {len(skipped)} files:", *skipped[:10], sep="\n  ")


if __name__ == "__main__":
    main()
