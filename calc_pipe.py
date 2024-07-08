# -*- encoding: utf-8 -*-

from Pipe import Pipe
from Soil import Soil


def calc_pipe(
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
    k_v,
    k_l,
    k_vs,
    boundary_condition
):
    pipe = Pipe(
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
    )

    soil = Soil(pipe.l, pipe.sc_fac, pipe.ei, k_v, k_l, k_vs, boundary_condition)

    # 1 - RP-F105 Span
    # 2 - Pinned-pinned
    # 3 - Fixed-fixed

    if boundary_condition == 1:
        f0_in = pipe.f0_rp(
            soil.leffl_l,
            soil.leffl_vs,
            soil.bc_coeffs["c1_in"],
            soil.bc_coeffs["c2_in"],
            0,
            soil.bc_coeffs["c6_in"],
            0
        )

        f0_cr = pipe.f0_rp(
            soil.leffl_v,
            soil.leffl_vs,
            soil.bc_coeffs["c1_cr"],
            soil.bc_coeffs["c2_cr"],
            soil.bc_coeffs["c3_cr"],
            soil.bc_coeffs["c6_cr"]
        )

        sa_in = pipe.sa_rp(
            soil.leffl_l,
            soil.bc_coeffs["c4_in"]
        )

        sa_cr = pipe.sa_rp(
            soil.leffl_v,
            soil.bc_coeffs["c4_cr"]
        )
    else:
        f0_in = pipe.f0_rp(
            1,
            1,
            soil.bc_coeffs["c1_in"],
            soil.bc_coeffs["c2_in"],
            0,
            soil.bc_coeffs["c6_in"],
            0
        )

        f0_cr = pipe.f0_rp(
            1,
            1,
            soil.bc_coeffs["c1_cr"],
            soil.bc_coeffs["c2_cr"],
            soil.bc_coeffs["c3_cr"],
            soil.bc_coeffs["c6_cr"]
        )

        sa_in = pipe.sa_rp(
            1,
            soil.bc_coeffs["c4_in"]
        )

        sa_cr = pipe.sa_rp(
            1,
            soil.bc_coeffs["c4_cr"]
        )

    return {
        # Areas
        "a_cont": pipe.a_cont,
        "a_s": pipe.a_s,
        "a_coat": pipe.a_coat,
        "a_conc": pipe.a_conc,
        "a_e": pipe.a_e,
        # Valores auxiliares
        "d": pipe.d,
        "ei_s": pipe.ei,
        "m_e": pipe.m_e,
        "s_eff": pipe.s_eff,
        "csf": pipe.csf,
        "l_over_d_s": pipe.l / pipe.d_s,
        # Dados de resposta
        "f0_in": f0_in,
        "f0_cr": f0_cr,
        "sa_in": sa_in / 1e6,
        "sa_cr": sa_cr / 1e6,
        "lambda": 1.29 * sa_in / pipe.d / 1e6,
        "delta_over_d": pipe.delta / pipe.d,
        "s_eff_over_p_cr": pipe.s_eff / pipe.p_cr
    }
