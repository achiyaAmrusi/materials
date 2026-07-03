from materials import Material
from materials.isotopes import Si, O

glass = Material(
    name="Glass",
    composition={
    Si: 1,
    O: 2,
},
    fraction_type="atomic",
    density=2.2  # g/cm3
)
