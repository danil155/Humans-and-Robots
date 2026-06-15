import numpy as np
from scipy.optimize import linprog
from domain.models import ILPSolver, ProductionParams, LPOptimum


class ScipyLPSolver(ILPSolver):
    def solve(self, x: float, params: ProductionParams) -> LPOptimum:
        # Переходим к задаче минимизации целевой функции Z
        c = np.array([
            -(params.p - params.c_m),
            -(params.p - params.c_r),
            -(params.p - params.c_h)
        ])

        # Ограничения
        L_x = params.L * (1 - x)
        K_x = params.K0 * x

        A_ub = np.array([
            [params.a_m, 0, params.a_h],
            [0, params.b_r, params.b_h],
            [1, 1, 1],
            [-params.a_m, 0, 0]
        ])

        b_ub = np.array([
            L_x,
            K_x,
            params.D,
            -params.L_soc * (1 - x) * params.gamma
        ])

        # Неотрицательность
        bounds = [(0, None), (0, None), (0, None)]

        res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')

        if not res.success:
            return LPOptimum(0, 0, 0, float('-inf'))

        c_fire = params.compute_fire_cost(x)

        z_max = -res.fun - c_fire

        return LPOptimum(
            y_m=res.x[0],
            y_r=res.x[1],
            y_h=res.x[2],
            z_max=z_max,
            fire_cost=c_fire
        )
