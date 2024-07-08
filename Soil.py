# -*- encoding: utf-8 -*-

from math import log10


class Soil:

    def __init__(self, l, sc_fac, ei, k_v, k_l, k_vs, boundary_condition):
        """
        k_v = vertical dynamic soil stiffness
        k_l = lateral dynamic soil stiffness
        k_vs = vertical, static soil stiffness
        """
        beta_v = log10((k_v * l ** 4) / (sc_fac * ei))
        beta_l = log10((k_l * l ** 4) / (sc_fac * ei))
        beta_vs = log10((k_vs * l ** 4) / (sc_fac * ei))

        # leffl = L_eff / L
        if beta_v < 2.7:
            self.leffl_v = 4.73 / (0.036 * beta_v ** 2 + 0.61 * beta_v + 1)
        else:
            self. leffl_v = 4.73 / \
                (-0.066 * beta_v ** 2 + 1.02 * beta_v + 0.63)

        if beta_l < 2.7:
            self.leffl_l = 4.73 / (0.036 * beta_l ** 2 + 0.61 * beta_l + 1)
        else:
            self. leffl_l = 4.73 / \
                (-0.066 * beta_l ** 2 + 1.02 * beta_l + 0.63)

        if beta_vs < 2.7:
            self.leffl_vs = 4.73 / (0.036 * beta_vs ** 2 + 0.61 * beta_vs + 1)
        else:
            self. leffl_vs = 4.73 / \
                (-0.066 * beta_vs ** 2 + 1.02 * beta_vs + 0.63)

        # Boundary condition coefficients
        # 1 - RP-F105 Span
        # 2 - Pinned-pinned
        # 3 - Fixed-fixed
        if boundary_condition == 2:
            self.bc_coeffs = {
                # In-line
                "c1_in": 1.57,
                "c2_in": 1,
                "c3_in": 0.8,
                "c4_in": 4.93,
                "c5_in": 1 / 8,
                "c6_in": 5 / 384,
                # Cross-flow
                "c1_cr": 1.57,
                "c2_cr": 1,
                "c3_cr": 0.8,
                "c4_cr": 4.93,
                "c5_cr": 1 / 8,
                "c6_cr": 5 / 384
            }
        elif boundary_condition == 3:
            self.bc_coeffs = {
                # In-line
                "c1_in": 3.56,
                "c2_in": 4,
                "c3_in": 0.2,
                "c4_in": 14.1,
                "c5_in": 1 / 12,
                "c6_in": 1 / 384,
                # Cross-flow
                "c1_cr": 3.56,
                "c2_cr": 4,
                "c3_cr": 0.2,
                "c4_cr": 14.1,
                "c5_cr": 1 / 12,
                "c6_cr": 1 / 384
            }
        else:
            self.bc_coeffs = {
                # In-line
                "c1_in": 3.56,
                "c2_in": 4,
                "c3_in": 0.4,
                "c4_in": max(14.1 * (1 / self.leffl_l) ** 2, 8.6),
                "c5_in": max(1 / (18 * (self.leffl_vs) ** 2 - 6), 1 / 24),
                "c6_in": 1 / 384,
                # Cross-flow
                "c1_cr": 3.56,
                "c2_cr": 4,
                "c3_cr": 0.4,
                "c4_cr": max(14.1 * (1 / self.leffl_v) ** 2, 8.6),
                "c5_cr": max(1 / (18 * (self.leffl_vs) ** 2 - 6), 1 / 24),
                "c6_cr": 1 / 384
            }
            