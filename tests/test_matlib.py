"""Import-time regression test for the pre-built material library.

Ensures every isotope/element referenced in matlib actually resolves
in the registry -- a typo'd symbol there raises AttributeError at
import time, which is exactly what this guards against.
"""


def test_matlib_imports_and_exposes_materials():
    from materials import matlib

    for name in ("air", "water", "stainless_304", "sand", "portland_concrete",
                 "magnetite", "baryte", "limestone", "Al", "Cu", "lead",
                 "polyethylene", "polypropylene", "polystyrene", "NaI", "glass"):
        assert hasattr(matlib, name), f"materials.matlib.{name} missing"


def test_matlib_materials_have_positive_density():
    from materials import matlib

    for name in ("air", "water", "stainless_304", "glass"):
        material = getattr(matlib, name)
        assert material.density > 0
