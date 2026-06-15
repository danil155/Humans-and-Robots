from fastapi import APIRouter, HTTPException, status
import logging

from api.schemas import (
    SolveGameRequest,
    SolveGameResponse,
    StrategyResponse,
    PayoffsResponse,
    LPSolutionResponse
)
from domain.models import ProductionParams, GameParams
from infrastructure.lp_solver import ScipyLPSolver
from use_cases.game_solver import GameSolver

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/api', tags=['game'])


def _convert_to_domain_models(request: SolveGameRequest) -> tuple[ProductionParams, GameParams]:
    prod = request.production_params
    game = request.game_params

    prod_params = ProductionParams(
        p=prod.p,
        L=prod.L,
        L_soc=prod.L_soc,
        K0=prod.K0,
        D=prod.D,
        a_m=prod.a_m,
        a_h=prod.a_h,
        b_r=prod.b_r,
        b_h=prod.b_h,
        gamma=prod.gamma,
        raw_material_cost=prod.raw_material_cost,
        w_m=prod.w_m,
        w_h=prod.w_h,
        insurance_rate=prod.insurance_rate,
        robot_amortization=prod.robot_amortization,
        hours_per_person=prod.hours_per_person
    )

    game_params = GameParams(
        w_m=game.w_m,
        w_h=game.w_h,
        effort_cost=game.effort_cost,
        severance=game.severance,
        moral_sat=game.moral_sat,
        stress=game.stress,
        fine=game.fine,
        subsidy=game.subsidy,
        taxes_base=game.taxes_base,
        gdp_multiplier=game.gdp_multiplier,
        social_tension_cost=game.social_tension_cost
    )

    return prod_params, game_params


def _build_response(result: dict[str, any]) -> SolveGameResponse:
    equilibrium = result['equilibrium_path']
    payoffs = result['equilibrium_payoffs']

    full_tree = result.get('full_tree_eval', {})
    firm_strategy = equilibrium[0]
    lp_info = full_tree.get(firm_strategy, {}).get('lp_result', {})

    return SolveGameResponse(
        equilibrium=StrategyResponse(
            firm=equilibrium[0],
            people=equilibrium[1],
            regulator=equilibrium[2]
        ),
        payoffs=PayoffsResponse(
            u_firm=payoffs['Firm'],
            u_people=payoffs['People'],
            u_regulator=payoffs['Regulator']
        ),
        lp_solution=LPSolutionResponse(
            y_m=lp_info.get('y_m', 0),
            y_r=lp_info.get('y_r', 0),
            y_h=lp_info.get('y_h', 0),
            z_max=payoffs['Firm'],
            fire_cost=lp_info.get('fire_cost', 0),
            operational_profit=lp_info.get('operational_profit', 0),
            c_m=lp_info.get('c_m', 0),
            c_r=lp_info.get('c_r', 0),
            c_h=lp_info.get('c_h', 0)
        ),
        full_tree_eval=full_tree,
        analysis=result.get('analysis')
    )


@router.post('/solve', response_model=SolveGameResponse)
async def solve_game(request: SolveGameRequest) -> SolveGameResponse:
    try:
        prod_params, game_params = _convert_to_domain_models(request)

        lp_solver = ScipyLPSolver()
        game_solver = GameSolver(lp_solver, prod_params, game_params)

        result = game_solver.solve_backward_induction()
        analysis = game_solver.analyze_equilibrium(result)
        result['analysis'] = analysis

        response = _build_response(result)

        logger.info(f'Решение найдено: {response.equilibrium}')
        return response

    except Exception as e:
        logger.error(f'Ошибка при решении игры: {e}', exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {'status': 'ok'}
