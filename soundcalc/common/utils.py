from __future__ import annotations

from ..zkevms.zkevm import zkEVMParams

def get_rho_plus(H: int, D: float, max_combo: int) -> float:
    """Compute rho+. See page 16 of Ha22"""
    # XXX Should this be (H + 2) / D? This part is cryptic in [Ha22]
    # TODO Figure out
    return (H + max_combo) / D

def get_proof_system_errors(L_plus: float, params: zkEVMParams):
    """
    Compute common proof system error components that are shared across regimes.

    Returns a tuple: (e_ALI, e_DEEP, e_PLONK, e_PLOOKUP)
    """

    # TODO Check that it holds for all regimes

    # XXX These proof system errors are actually quite RISC0 specific.
    # See Section 3.4 from the RISC0 technical report.
    # We might want to generalize this further for other zkEVMs.
    # For example, Miden also computes similar values for DEEP-ALI in:
    # https://github.com/facebook/winterfell/blob/2f78ee9bf667a561bdfcdfa68668d0f9b18b8315/air/src/proof/security.rs#L188-L210
    e_ALI = L_plus * params.num_columns / params.F
    e_DEEP = (
        L_plus
        * (4 * (params.trace_length + params.max_combo - 1) + (params.trace_length - 1))
        / (params.F - params.trace_length - params.D)
    )

    e_PLONK = params.field_extension_degree * 5 * params.trace_length / params.F  # XXX this 5 is a RISC0 magic number n_{σ_{mem}} == 5.
    e_PLOOKUP = params.field_extension_degree * 15 * params.trace_length / params.F  # XXX this 15 is a RISC0 magic number n_{σ_{bytes}} == 15.
    return e_ALI, e_DEEP, e_PLONK, e_PLOOKUP


