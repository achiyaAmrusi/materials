from materials import Material
from materials.isotopes import Na, I

water = Material(
    name='water',
    composition={Na:1, I:1},
    fraction_type='atomic',
    density = 3.67
)