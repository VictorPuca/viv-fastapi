# -*- encoding: utf-8 -*-

from math import pi

"""
# Pipe dimensions [m]
d_s,  # Steel diameter
t_s,  # Steel thickness
t_conc,  # Concrete thickness
t_coat,  # Coating thickness

# Constants
nu,  # Poisson's ratio
alpha,  # Thermal coefficient
young,  # Young's Modulus
rho_water,  # Water density

# Functional loads
s_lay,  # S-Lay tension
pbar,  # Internal pressure
dt,  # Temperature difference

# Free Span data
l,  # Span length
h,  # Water depth
e,  # gap

# Concrete stiffness parameters
kc,
fcn,  # Construction strength of the concrete

# Densities
rho_s,  # Steel density
rho_conc,  # Concrete density
rho_coat,  # Coating density
rho_cont,  # Content density
"""

class Pipe:

    g = 9.81

    def __init__(
        self,
        d_s,
        t_s,
        t_conc,
        t_coat,
        nu,
        alpha,
        young,
        rho_water,
        s_lay,
        pbar,
        dt,
        h,
        l,
        e,
        kc,
        fcn,
        rho_s,
        rho_conc,
        rho_coat,
        rho_cont,
    ):
        self.d_s = d_s  # Steel diameter
        self.t_s = t_s  # Steel thickness
        self.t_conc = t_conc  # Concrete thickness
        self.t_coat = t_coat  # Coating thickness
        self.nu = nu  # Poisson's ratio
        self.alpha = alpha  # Thermal coefficient
        self.young = young  # Young's Modulus
        self.rho_water = rho_water  # Water density
        self.s_lay = s_lay  # S-Lay tension
        self.pbar = pbar  # Internal pressure
        self.dt = dt  # Temperature difference
        self.h = h  # Height
        self.l = l  # Span length
        self.e = e  # Gap
        self.kc = kc
        self.fcn = fcn  # Construction strength of the concrete
        self.rho_s = rho_s  # Steel density
        self.rho_conc = rho_conc  # Concrete density
        self.rho_coat = rho_coat  # Coating density
        self.rho_cont = rho_cont  # Content density

        # Calculated values
        self.pe = h / 10  # External pressure in bar
        self.d = d_s + 2 * (t_coat + t_conc)  # Outer Diameter
        # Added mass coefficient
        self.c_a = 1 if e / self.d >= 0.8 else 0.68 + \
            1.6 / (1 + 5 * e / self.d)

        # Areas
        self.a_cont = pi / 4 * (d_s - 2 * t_s) ** 2
        self.a_s = pi / 4 * (d_s ** 2 - (d_s - 2 * t_s) ** 2)
        self.a_coat = pi / 4 * ((d_s + 2 * t_coat) ** 2 - d_s ** 2)
        self.a_conc = pi / 4 * ((d_s + 2 * (t_coat + t_conc))
                                ** 2 - (d_s + 2 * t_coat) ** 2)
        self.a_e = pi / 4 * self.d ** 2

        # Bending Stiffness
        self.ei = pi / 64 * (d_s ** 4 - (d_s - 2 * t_s) ** 4) * young

        # Total mass
        self.m_tot = self.a_cont * rho_cont + self.a_s * rho_s + \
            self.a_coat * rho_coat + self.a_conc * rho_conc

        # Effective mass
        self.m_e = self.m_tot + \
            (pi * self.d ** 2 / 4) * self.c_a * rho_water

        # Submerged weight
        self.q = (self.m_tot - rho_water * (pi * self.d ** 2) / 4) * self.g

        # Concrete coating stiffness factor (CSF)
        self.i_conc = pi / 64 * (self.d ** 4 - (self.d - 2 * t_conc) ** 4)
        self.young_conc = 10000 * fcn ** 0.3 * 1000000
        self.ei_conc = self.young_conc * self.i_conc
        self.csf = kc * (self.ei_conc / self.ei) ** 0.75
        self.sc_fac = 1 + self.csf  # Stress concenctration factor

        # Specific density
        self.rho_specific = (self.m_tot / self.a_e) / self.rho_water

        # Effective axial force
        self.dpi = pbar * 100000  # in N/m²
        self.pe = self.pe * 100000  # in N/m²
        self.s_eff = s_lay - self.dpi * self.a_cont * \
            (1 - 2 * nu) - self.a_s * young * dt * alpha
        self.n_trw = self.s_eff + self.dpi * self.a_cont - self.pe * self.a_e
        self.sig_n = self.n_trw / self.a_s
        self.sig_h = (self.dpi - self.pe) * (d_s - t_s) / 2 / t_s

    def f0_rp(
        self,
        leffl,  # Effective length
        leffl_vs,
        c1, c2, c3, c6, # Boundary conditions coefficients
        delta=1
    ):
        ax_limit = -0.5  # s_eff / p_cr
        sag_limit = 2.5  # delta / d

        leff = leffl * self.l
        self.p_cr = (c2 * self.sc_fac * pi ** 2 * self.ei) / leff ** 2
        self.axial = self.s_eff / self.p_cr

        if delta != 0:
            self.delta = c6 * (self.q * (leffl_vs * self.l) ** 4) / \
                (self.ei * self.sc_fac * (1 + self.axial))
        else:
            self.delta = 0

        if self.axial < ax_limit:
            self.axial = ax_limit

        if abs(self.delta / self.d) > sag_limit:
            sag = c3 * sag_limit ** 2
        else:
            sag = c3 * (self.delta / self.d) ** 2

        return c1 * self.sc_fac ** 0.5 * \
            (self.ei / (self.m_e * leff ** 4) *
                (1 + self.axial + sag)) ** 0.5

    # Maximum unit diameter stress amplitude
    def sa_rp(
        self,
        leffl,
        c4
    ):
        d_s = self.d_s - self.t_s
        leff = leffl * self.l
        return c4 * self.sc_fac * self.d * self.young * d_s / (leff ** 2)
