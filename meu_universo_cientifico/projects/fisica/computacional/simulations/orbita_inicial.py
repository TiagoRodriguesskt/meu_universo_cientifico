import math

import matplotlib.pyplot as plt
from astropy import units as u
from poliastro.bodies import Earth
from poliastro.core.elements import coe2rv
from poliastro.plotting import OrbitPlotter3D
from poliastro.twobody import Orbit

Req = Earth.R.to(u.km).value
Earth_k = Earth.k


def keplerian2cartesian(kepler):

    a = (kepler[0] + kepler[1] + Req * 2) * 1000 / 2  # m
    e = (kepler[0] - kepler[1]) / (kepler[0] + kepler[1] + Req * 2)
    p = a * (1 - e**2)

    return coe2rv(Earth_k, p, e, kepler[2], kepler[3], kepler[4], kepler[5])


op = OrbitPlotter3D()

r0, v0 = keplerian2cartesian(
    [8000, 600, 64.3 * math.pi / 180, 0, 300 * math.pi / 180, 0]
)
r1, v1 = keplerian2cartesian(
    [39754, 600, 64.3 * math.pi / 180, 0, 270 * math.pi / 180, 0]
)
r2, v2 = keplerian2cartesian(
    [2000, 800, 80 * math.pi / 180, 0, 300 * math.pi / 180, math.pi]
)

o0 = Orbit.from_vectors(Earth, r0 * u.km / 1000, v0 * u.km / u.s / 1000)
o1 = Orbit.from_vectors(Earth, r1 * u.km / 1000, v1 * u.km / u.s / 1000)
o2 = Orbit.from_vectors(Earth, r2 * u.km / 1000, v2 * u.km / u.s / 1000)

op.plot(o0)
op.plot(o1)
op.plot(o2)

plt.show()
