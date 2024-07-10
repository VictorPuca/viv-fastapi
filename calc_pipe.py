# -*- encoding: utf-8 -*-

import Pipe
import Soil
import json

from math import pi

def iter_calc_pipe(pipe_name):
    with open('./db.json', 'r') as file:
        original_data = json.load(file)
    data = original_data.copy()
    with open('./db2.json', 'r') as file:
        data2 = json.load(file)
        
    # Busca o duto específico pelo nome
    pipe = next((pipe for pipe in data['pipes'] if pipe['pipe'] == pipe_name), None)
    
    if not pipe:
        print(f"Duto com o nome '{pipe_name}' não encontrado.")
        return

    result = calc_pipe(
        pipe['d_s'],
        pipe['t_s'],
        data2['t_conc'],
        data2['t_coat'],
        data2['nu'],
        data2['alpha'],
        data2['young'],
        data2['rho_water'],
        data2['s_lay'],
        data2['pbar'],
        data2['dt'],
        data2['h'],
        data2['l'],
        data2['e'],
        data2['kc'],
        data2['fcn'],
        data2['rho_s'],
        data2['rho_conc'],
        data2['rho_coat'],
        data2['rho_cont'],
        data2['k_v'],
        data2['k_l'],
        data2['k_vs'],
        data2['boundary_condition']
    )
    
    try:
        with open('./result.json', 'r') as file:
            data_to_save = json.load(file)
    except FileNotFoundError:
        data_to_save = {}
    
    data_to_save[pipe['pipe']] = result
    
    with open('./result.json', 'w') as file:
        json.dump(data_to_save, file, indent=4)
        

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
    pipe = Pipe.Pipe(
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

    soil = Soil.Soil(pipe.l, pipe.sc_fac, pipe.ei, k_v, k_l, k_vs, boundary_condition)

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

if __name__ == '__main__':
    # Especifique o nome do duto
    pipe_name = "24 (pol) STD"
    iter_calc_pipe(pipe_name)