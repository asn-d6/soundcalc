from __future__ import annotations

from soundcalc.zkvms.fri_based_vm import FRIBasedVM


from ..common.utils import get_bits_of_security_from_error


def best_attack_security(params: FRIBasedVM) -> int:
    """
    Security level based on the best known attack.

    Currently, this is based on the toy problem also known as "ethSTARK conjecture".
    It uses the simplest and probably the most optimistic soundness analysis.

    Note: this is just for historical reference, the toy problem security has no real meaning.

    This is Regime 1 from the RISC0 Python calculator
    """

    # FRI errors under the toy problem regime
    # see "Toy problem security" in §5.9.1 of the ethSTARK paper
    commit_phase_error = 1 / params.F
    query_phase_error_without_grinding = params.rho ** params.num_queries
    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    query_phase_error_with_grinding = query_phase_error_without_grinding * 2 ** (-params.grinding_query_phase)

    final_error = commit_phase_error + query_phase_error_with_grinding
    final_level = get_bits_of_security_from_error(final_error)

    return final_level
