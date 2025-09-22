from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..zkevms.zkevm import zkEVMParams

def get_FRI_query_phase_error(theta: float, num_queries: int, grinding_query_phase_bits: int) -> float:
    """
    Compute the FRI query phase soundness error.
    See the last term of Equation 7 in Theorem 2 of Ha22.

    It includes `grinding_query_phase_bits` bits of grinding.
    """
    FRI_query_phase_error = (1 - theta) ** num_queries

    # Add bits of security from grinding (see section 6.3 in ethSTARK)
    FRI_query_phase_error *= 2 ** (-grinding_query_phase_bits)

    return FRI_query_phase_error

def get_johnson_parameter_m() -> float:
    """
    Return m from https://eprint.iacr.org/2022/1216.pdf
    """
    # ASN This is hardcoded to 16, whereas winterfell brute forces it:
    #    https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs#L290-L306
    return 16.0

def get_num_FRI_folding_rounds(
    witness_size: int,
    field_extension_degree: int,
    folding_factor: int,
    fri_early_stop_degree: int,
) -> int:
    """
    Compute the number of FRI folding rounds.
    Stolen from:
      https://github.com/risc0/risc0/blob/release-2.0/risc0/zkp/src/prove/soundness.rs#L125
    """
    rounds = 0
    n = int(witness_size)
    while n // int(field_extension_degree) > int(fri_early_stop_degree):
        n //= int(folding_factor)
        rounds += 1
    return rounds



def _get_batched_FRI_commit_phase_error(
    num_polys: float,
    e_proximity_gap: float,
    m: int,
    D: float,
    h: int,
    rho: float,
    F: float,
    FRI_rounds_n: int,
    FRI_folding_factor: int,
) -> float:
    """
    See Theorem 8.3 of BCIKS20.
    Also, seen in Theorem 2 of Ha22, and Theorem 1 of eSTARK paper.
    """
    last_term = (2 * m + 1) * (D + 1) * (FRI_rounds_n * FRI_folding_factor) / (math.sqrt(rho) * F)
    return (num_polys - 0.5) * e_proximity_gap + last_term


def get_FRI_soundness_error(
    params: "zkEVMParams",
    e_proximity_gap: float,
    theta: float,
    m: float,
) -> tuple[float, float, float]:
    """
    Given regime-specific proximity gaps error, and parameters for FRI, compute the FRI soundness errors.
    """
    # Compute FRI commit phase error
    e_FRI_commit_phase = _get_batched_FRI_commit_phase_error(
        params.num_polys, e_proximity_gap, m,
        params.D, params.h, params.rho, params.F,
        params.FRI_rounds_n, params.FRI_folding_factor
    )

    # Compute FRI query phase error (includes grinding internally)
    e_FRI_query_phase = get_FRI_query_phase_error(theta, params.num_queries, params.grinding_query_phase)

    # Total FRI error
    e_FRI_final = e_FRI_commit_phase + e_FRI_query_phase

    return e_FRI_final, e_FRI_commit_phase, e_FRI_query_phase
