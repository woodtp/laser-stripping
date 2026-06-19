#-----------------------------------------------------
# Track bunch with r and p through the external field
# The field is 1 T and has direction (0,1,0)
#-----------------------------------------------------

import math

from orbit.core.bunch import Bunch
from orbit.core.trackerrk4 import PyExternalEffects, RungeKuttaTracker, ExtEffectsContainer
from laserstripping import ConstEMfield
from laserstripping import HermiteGaussianLFmode, TwoLevelAtom


# ---------------------- Bunch/particle kinematic parameters ---------------------- #

TK = 1.0                             # energy of particle [GeV]
mass = 0.938256 + 0.000511           # mass [GeV]
charge = 0                           # [e]
E = mass + TK
P = math.sqrt(E * E - mass * mass)
beta = P / E
# g = E / mass
c = 299792458                        # speed of light
vz = c * beta                        # speed of particle

b = Bunch()
b.charge(charge)
b.mass(mass)
b.addParticle(0, 0, 0, 0, 0, P)


# ---------------------- Bunch/particle quantum parameters ---------------------- #

n_states = 3                         # excitation between the 1st (ground) and the 3rd excited state
delta_E = 1. / 2. - 1. / (2. * n_states * n_states)  # energy transition between 1st and 3rd excited state
dip_trans = math.sqrt(
    256 * n_states**7 * (n_states - 1)**(2 * n_states - 5) /
    3 / (n_states + 1)**(2 * n_states + 5)
)

# ta = 2.418884326505e-17            # atomic unit of time


# ---------------------- Laser beam parameters ---------------------- #

la0 = 2 * math.pi * 5.291772108e-11 / 7.297352570e-3 / delta_E  # resonance wavelength at rest frame
la = 355.0e-9                        # laser wavelength at the laboratory frame
te = TK - b.mass() * (la / la0 - 1) # temporal variable
kz = te / math.sqrt(P * P - te * te) # variable defining angle of interaction

print("design angle of interaction =", math.atan2(1, -kz) * 360 / 2 / math.pi,
      "direction of laser pulse =", (-1, 0, kz))

power = 1.0e6          # peak power of laser pulse in Watt
sigma_t = 25e-12       # rms time of Gaussian profile of laser pulse

wx, wy, fx, fy = 0.001, 0.001, 1, 1   # default (non-critical) laser parameters
zl = -5 * sigma_t * c                  # initial shift of laser pulse before interaction

LFS = HermiteGaussianLFmode(
    math.sqrt(power), 0, 0,
    abs(wx), abs(wy), fx, fy,
    la, zl, sigma_t * c
)

rx, ry, ax, ay = 0.2e-3, 0.2e-3, 0.5e-3, 0.5e-3  # rms size and divergence half angle at interaction point
LFS.setLocalParameters(abs(rx), abs(ry), ax, ay)

# Orientation of beam (k-vector) {-1, 0, kz} and E-field polarization {kz, 0, 1}
LFS.setLaserFieldOrientation(
    0., 0., 0.,
    -1., 0., kz,
    kz, 0., 1.,
    kz, 0., 1.
)
# LFS.setLaserFieldOrientation(0., 0., 0., -1., 0., kz, kz, 0., 1., 0., 1., 0.)  # parallel polarization

eff = TwoLevelAtom(LFS, delta_E, dip_trans)  # excitation effect (ground state by default)


class ExternalEffects(PyExternalEffects):
    def __init__(self):
        PyExternalEffects.__init__(self)

    def setupEffects(self, bunch):
        pass

    def prepareEffects(self, bunch, t):
        pass

    def finalizeEffects(self, bunch):
        pass

    def applyEffects(self, bunch, t, t_step, field_source, tracker):
        if int(t / t_step) % (n_step // 1000) == 0:
            print(b.z(0), "\t", b.partAttrValue("Populations", 0, 2))

    def applyEffectsForEach(self, bunch, index, inVct, outVct, t, t_step, field_source, tracker):
        pass


print_excitation_track = ExternalEffects()
cont_eff = ExtEffectsContainer()
# cont_eff.AddEffect(print_excitation_track)  # prints excitation as a function of z
cont_eff.AddEffect(eff)

b.z(0, b.z(0) - 5 * sigma_t * vz)   # initial shift (z-coordinate) before interaction

# Tracking time is supposed to be 2*(5*sigma_t)
n_step = 1000000                         # number of tracking steps
time_step = 2 * (5 * sigma_t) / n_step  # time step of tracking

tracker = RungeKuttaTracker(0)
fS = ConstEMfield(0, 0, 0, 0, 0, 0)     # permanent field E=0, B=0 (formally required by tracker)
tracker.track(b, 0, time_step * n_step, time_step, fS, cont_eff)  # track from 0 for time_step*n_step

print(b.partAttrValue("Populations", 0, 1))         # ground state population after excitation
print(b.partAttrValue("Populations", 0, 2))         # 3rd excited state after excitation
print(b.partAttrValue("Populations", 0, 1)
      + b.partAttrValue("Populations", 0, 2))        # sum must equal 1 for TwoLevelAtom model
