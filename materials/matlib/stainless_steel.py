from materials import Material
from materials.isotopes import C, Mn, P, S, Si, Cr, Ni, Fe

# Create the Material object
stainless_304 = Material(
    name="Stainless Steel 304",
    composition={
    C: 0.003635,
    Mn: 0.019870,
    P: 0.000793,
    S: 0.000511,
    Si: 0.019434,
    Cr: 0.199443,
    Ni: 0.088343,
    Fe: 0.667971
},
    fraction_type="atomic",
    density=8.03  # g/cm3
)