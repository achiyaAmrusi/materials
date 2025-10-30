from materials import Material
from materials.isotopes import H, C

polypropylene = Material(
    name='polypropylene',
    composition={H:2, C:1},
    fraction_type='atomic',
    density = 0.9
)

polyethylene = Material(
    name='polyethylene',
    composition={H:2, C:1},
    fraction_type='atomic',
    density = 0.93
)

polystyrene = Material(
    name='polystyrene',
    composition={H:1, C:1},
    fraction_type='atomic',
    density = 1.06
)

