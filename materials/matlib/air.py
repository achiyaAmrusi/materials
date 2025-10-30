from materials import Material
from materials.isotopes import C, N, O, Ar

air = Material(
    name='air',
    composition={C:0.00015, N:0.784429, O:0.21075, Ar:0.004671},
    fraction_type='atomic',
    density = 0.001205
)