from materials import Material
from materials.isotopes import H, C, O, Na, Mg, Al, Si, K, Ca, Fe, Ba, S

# Create the Material object
sand = Material(
    name="Sand",
    composition={
    H: 0.135402,
    C: 0.004874,
    O: 0.583891,
    Na: 0.012932,
    Al: 0.022215,
    Si: 0.226487,
    K: 0.005179,
    Ca: 0.004874,
    Fe: 0.004146
},
    fraction_type="atomic",
    density=1.7  # g/cm3
)

portland_concrete = Material(
    name="portland_concrete",
    composition={
    H: 0.168753,
    C: 0.001416,
    O: 0.562526,
    Na: 0.011838,
    Mg: 0.001400,
    Al: 0.021354,
    Si: 0.204119,
    K: 0.005656,
    Ca: 0.018674,
    Fe: 0.004264,
},
    fraction_type="atomic",
    density=2.3  # g/cm3, typical for Portland cement
)

magnetite = Material(
    name="magnetite",
    composition={
    Fe: 3,
    O: 4,
},
    fraction_type="atomic",
    density=5.17  # g/cm3, typical for Portland cement
)

baryte = Material(
    name="baryte",
    composition={
    Ba: 1,
    S: 1,
    O: 4,
},
    fraction_type="atomic",
    density=4.48  # g/cm3, typical for Portland cement
)

limestone = Material(
    name="limestone",
    composition={
        C: 0.190012,
        O: 0.603322,
        Si: 0.016659,
        Ca: 0.190007
    },
    fraction_type="atomic",
    density=2.6  # g/cm3
)