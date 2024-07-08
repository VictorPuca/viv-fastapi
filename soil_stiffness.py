# -*- encoding: utf-8 -*-

# from math import pi

pi = 3.1415926


def soil_stiffness(
    d_s,
    t_s,
    t_conc,
    t_coat,
    rho_s,
    rho_conc,
    rho_coat,
    rho_cont,
    rho_water,
    soil_type
):
    d = d_s + 2 * (t_coat + t_conc)

    a_cont = pi / 4 * (d_s - 2 * t_s) ** 2
    a_s = pi / 4 * (d_s ** 2 - (d_s - 2 * t_s) ** 2)
    a_coat = pi / 4 * ((d_s + 2 * t_coat) ** 2 - d_s ** 2)
    a_conc = pi / 4 * ((d_s + 2 * (t_coat + t_conc))
                       ** 2 - (d_s + 2 * t_coat) ** 2)
    a_e = pi / 4 * d ** 2

    m_tot = a_cont * rho_cont + a_s * rho_s + a_coat * rho_coat + a_conc * rho_conc

    rho_specific = (m_tot / a_e) / rho_water

    if soil_type == "Sand - Loose":
        c_v = 10500000
        c_l = 9000000
        k_vs = 250000
    elif soil_type == "Sand - Medium":
        c_v = 14500000
        c_l = 12500000
        k_vs = 530000
    elif soil_type == "Sand - Dense":
        c_v = 21000000
        c_l = 18000000
        k_vs = 1350000
    elif soil_type == "Clay - Very soft":
        c_v = 600000
        c_l = 500000
        k_vs = 75000
    elif soil_type == "Clay - Soft":
        c_v = 1400000
        c_l = 1200000
        k_vs = 210000
    elif soil_type == "Clay - Firm":
        c_v = 3000000
        c_l = 2600000
        k_vs = 650000
    elif soil_type == "Clay - Stiff":
        c_v = 4500000
        c_l = 3900000
        k_vs = 1300000
    elif soil_type == "Clay - Very stiff":
        c_v = 11000000
        c_l = 9500000
        k_vs = 2500000
    elif soil_type == "Clay - Hard":
        c_v = 12000000
        c_l = 10500000
        k_vs = 3400000

    if soil_type.split()[0] == 'Clay':
        nu_soil = 0.45
    elif soil_type.split()[0] == 'Sand':
        nu_soil = 0.35

    k_v = c_v / (1 - nu_soil) * (2 * rho_specific / 3 + 1 / 3) * d ** 0.5
    k_l = c_l * (1 + nu_soil) * (2 * rho_specific / 3 + 1 / 3) * d ** 0.5

    return {
        "k_v": k_v,# round(k_v, 2),
        "k_l": k_l,# round(k_l, 2),
        "k_vs": k_vs# round(k_vs, 2)
    }
