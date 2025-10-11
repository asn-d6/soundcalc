from __future__ import annotations


from ..zkevms.zkevm import zkEVMParams
from typing import Any
from ..common.utils import get_bits_of_security_from_error, get_proof_system_levels


def toy_problem_security(params: zkEVMParams) -> int:
    """
    Toy Problem Regime (TPR), also known as "ethSTARK conjecture"
    It uses the simplest and probably the most optimistic soundness analysis.

    Note: this is just for historical reference, the toy problem security has no real meaning.

    This is Regime 1 from the RISC0 Python calculator
    """

    # FRI errors under the toy problem regime
    # see "Toy problem security" in §5.9.1 of the ethSTARK paper
    commit_phase = 1 / params.F
    query_phase_without_grinding = params.rho ** params.num_queries
    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    query_phase_with_grinding = query_phase_without_grinding * 2 ** (-params.grinding_query_phase)

    # Compute proof system errors, but ignore ALI/DEEP under the toy problem regime
    levels_proof_system = get_proof_system_levels(params.num_polys, params)
    error_plonk = 2**(-levels_proof_system["PLONK"])
    error_plookup = 2**(-levels_proof_system["PLOOKUP"])

    final_error = commit_phase + query_phase_with_grinding + error_plonk + error_plookup
    final_level = get_bits_of_security_from_error(final_error)

    return final_level
