from materials import Material
from materials.isotopes import Cu, Al

copper = Material(
    name="copper",
    composition={
    Cu: 1,
},
    fraction_type="atomic",
    density=8.96  # g/cm3
)

aluminum = Material(
    name="aluminum",
    composition={
    Al: 1,
},
    fraction_type="atomic",
    density=2.6989  # g/cm3
)
