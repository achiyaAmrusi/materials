from materials import Material
from materials.isotopes import Na, I

NaI = Material(
    name='water',
    composition={Na:1, I:1},
    fraction_type='atomic',
    density = 3.67
)