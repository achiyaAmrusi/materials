from materials import Material
from materials.isotopes import H, O

water = Material(
    name='water',
    composition={H:2, O:1},
    fraction_type='atomic',
    density = 1
)