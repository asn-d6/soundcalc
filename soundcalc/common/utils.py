from __future__ import annotations

from ..zkevms.zkevm import zkEVMParams

def get_rho_plus(H: int, D: float, max_combo: int) -> float:
    """Compute rho+. See page 16 of Ha22"""
    # XXX Should this be (H + 2) / D?
    return (H + max_combo) / D

def get_proof_system_errors(L_plus: float, params: zkEVMParams):
    """
    Compute common proof system error components that are shared across regimes.

    Returns a tuple: (e_ALI, e_DEEP, e_PLONK, e_PLOOKUP)
    """
    e_ALI = L_plus * params.C / params.F
    e_DEEP = (
        L_plus
        * (4 * (params.H + params.max_combo - 1) + (params.H - 1))
        / (params.F - params.H - params.D)
    )
    e = params.field_extension_degree
    e_PLONK = e * 5 * params.H / params.F  # XXX this 5 is a RISC0 magic number n_{σ_{mem}} == 5.
    e_PLOOKUP = e * 15 * params.H / params.F  # XXX this 15 is a RISC0 magic number n_{σ_{bytes}} == 15.
    return e_ALI, e_DEEP, e_PLONK, e_PLOOKUP


