from __future__ import annotations

from .regime import Regime
from ..zkevms.zkevm import zkEVMParams
from typing import Any
from ..common.utils import get_rho_plus, get_proof_system_errors
from soundcalc.common.fri import (
    get_johnson_parameter_m,
    get_FRI_query_phase_error,
)
import math

class JohnsonBoundRegime(Regime):
    """
    List decoding up-to-Johnson bound regime (JBR)

    This is Regime 2 from the RISC0 Python calculator
    """

    def identifier(self) -> str:
        return "johnson_bound"

    def compute_security(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        self.params = params
        rho = params.rho
        m = get_johnson_parameter_m()

        alpha, theta = self._get_alpha_and_theta(rho, m)

        # Compute the FRI errors
        self.e_proximity_gap = self._get_proximity_gap_error(rho, m)
        self.e_FRI_commit_phase = get_batched_FRI_commit_phase_error(
            params.num_polys,
            self.e_proximity_gap,
            m,
            params.D,
            params.rho,
            params.F,
            params.FRI_rounds_n,
            params.FRI_folding_factor,
        )
        self.e_FRI_query_phase = get_FRI_query_phase_error(theta, params.num_queries, params.grinding_query_phase)
        self.e_FRI_final = self.e_FRI_commit_phase + self.e_FRI_query_phase

        # Compute Guruswami–Sudan list size
        L_plus = self._get_list_size(alpha, theta)

        (self.e_ALI, self.e_DEEP, self.e_PLONK, self.e_PLOOKUP) = get_proof_system_errors(L_plus, params)

        self.e_final = self.e_FRI_final + self.e_ALI + self.e_DEEP + self.e_PLONK + self.e_PLOOKUP

        return self.gets_bits_of_security_from_error()

    def _get_alpha_and_theta(self, rho: float, m: float) -> tuple[float, float]:
        """
        Compute alpha and theta. See Theorem 2 of Ha22.
        """
        # ASN Confusing because all the FRI papers (e.g. Ha22, eSTARK, etc.) define alpha as shown below
        # but looking at the function log_1_delta() from stir-whir-scripts,
        # we have: `alpha = 1 - sqrt(rho) - eta` which feels more natural.
        # BW: I think it is consistent if you set `theta = 1 - sqrt(rho) - eta`
        # for `eta = sqrt(rho) / (2m)` and `theta = 1 - alpha`.
        alpha = (1 + (1 / (2 * m))) * math.sqrt(rho)
        theta = 1 - alpha
        return alpha, theta

    def _get_minimal_m_plus(self, r_plus: float, alpha: float) -> int:
        # ASN RISC0 rust soundness also puts max_combo in here:
        #         let m_plus = 1.0 / (params.biggest_combo * (alpha / rho_plus.sqrt() - 1.0));
        return math.ceil(1 / (2 * (alpha / math.sqrt(r_plus) - 1)))

    def _get_list_size(self, alpha: float, theta: float) -> float:
        """
        Get list size for the Johnson bound regime.
        The value is from the Guruswami-Sudan decoder.
        """
        r_plus = get_rho_plus(self.params.trace_length, self.params.D, self.params.max_combo)
        assert theta < 1 - math.sqrt(r_plus)
        m_plus = self._get_minimal_m_plus(r_plus, alpha)
        assert theta <= 1 - math.sqrt(r_plus) * (1 + 1 / (2 * m_plus))

        # Note: Miden computes L differently (see Theorem 2 of https://eprint.iacr.org/2024/1553.pdf)
        #    L_miden = m / (params.rho - (2.0 * m / params.D));
        # Small difference for RISC0 parameters:
        #  RISC0=35, Miden=64
        return (m_plus + 0.5) / math.sqrt(r_plus)

    def _get_proximity_gap_error(self, rho: float, m: float) -> float:
        """
        Get the proximity gap error for the Johnson bound regime.
        This is the error of the commit phase of FRI as computed by the correlated agreement theorem in BCIKS20.
        Concretely, Theorem 5.1 in BCIKS20 (eprint) contains this bound.
        """
        return ((m + 0.5) ** 7) / (3 * (rho ** 1.5)) * (self.params.D ** 2) / self.params.F


def get_batched_FRI_commit_phase_error(
    num_polys: float,
    e_proximity_gap: float,
    m: int,
    D: float,
    rho: float,
    F: float,
    FRI_rounds_n: int,
    FRI_folding_factor: int,
) -> float:
    """
    See Theorem 8.3 of BCIKS20.
    Also, seen in Theorem 2 of Ha22, and Theorem 1 of eSTARK paper.

    Note: This function is used by both JBR and CBR.
    """
    last_term = (2 * m + 1) * (D + 1) * (FRI_rounds_n * FRI_folding_factor) / (math.sqrt(rho) * F)
    return (num_polys - 0.5) * e_proximity_gap + last_term
