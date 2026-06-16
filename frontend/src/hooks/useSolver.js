import { useState, useCallback } from "react";
import { solveGame } from "../api/solveApi";

export function useSolver() {
    const [result,  setResult]  = useState(null);
    const [loading, setLoading] = useState(false);
    const [error,   setError]   = useState(null);

    const solve = useCallback(async (productionParams, gameParams) => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const data = await solveGame({
                production_params: productionParams,
                game_params: gameParams,
            });

            const transformedResult = {
                equilibrium: {
                    firm: data.equilibrium.firm,
                    people: data.equilibrium.people,
                    regulator: data.equilibrium.regulator,
                },
                payoffs: {
                    u_firm: data.payoffs.u_firm,
                    u_people: data.payoffs.u_people,
                    u_regulator: data.payoffs.u_regulator,
                },
                lp_solution: {
                    y_m: data.lp_solution.y_m,
                    y_r: data.lp_solution.y_r,
                    y_h: data.lp_solution.y_h,
                    z_max: data.lp_solution.z_max,
                    fire_cost: data.lp_solution.fire_cost,
                    operational_profit: data.lp_solution.operational_profit,
                    c_m: data.lp_solution.c_m,
                    c_r: data.lp_solution.c_r,
                    c_h: data.lp_solution.c_h,
                    pi_1: data.lp_solution.pi_1,
                    pi_2: data.lp_solution.pi_2,
                    pi_3: data.lp_solution.pi_3,
                    pi_4: data.lp_solution.pi_4,
                },
                analysis: data.analysis,
                full_tree_eval: data.full_tree_eval
            };

            setResult(transformedResult);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    }, []);

    const reset = useCallback(() => {
        setResult(null);
        setError(null);
    }, []);

    return { result, loading, error, solve, reset };
}
