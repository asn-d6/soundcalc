from __future__ import annotations

from .regime import Regime
from ..zkevms.zkevm import zkEVMParams
from soundcalc.common.fri import get_FRI_query_phase_error
from ..common.utils import get_proof_system_errors
import math

class UniqueDecodingRegime(Regime):
    """
    Unique decoding regime (UDR)

    This is Regime 4 from the RISC0 Python calculator

    Many thanks to the UDR-specific analysis of Paul Gafni and Al Kindi:
        https://hackmd.io/@pgaf/HkKs_1ytT
    """

    def identifier(self) -> str:
        return "unique_decoding"

    def estimate(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        self.params = params
        rho = params.rho

        theta = self._get_theta(rho)

        # Compute FRI error components
        self.e_proximity_gap = self._get_proximity_gap_error()
        self.e_FRI_commit_phase = self._get_FRI_commit_phase_error()

        self.e_FRI_query_phase = get_FRI_query_phase_error(theta, params.num_queries, params.grinding_query_phase)
        self.e_FRI_final = self.e_FRI_commit_phase + self.e_FRI_query_phase

        # For unique decoding, list size is naturally 1
        L_plus = 1

        # XXX might still need to do something with m_plus or rho_plus. See the hackmd.
        (self.e_ALI, self.e_DEEP, self.e_PLONK, self.e_PLOOKUP) = get_proof_system_errors(L_plus, params)

        self.e_final = self.e_FRI_final + self.e_ALI + self.e_DEEP + self.e_PLONK + self.e_PLOOKUP

        return self.gets_bits_of_security()

    def _get_theta(self, rho: float) -> float:
        """
        Compute theta for the unique decoding regime.
        """
        alpha = 1 - (1 - rho) / 2  # XXX factcheck whether the "1 - " is correct here
        theta = 1 - alpha
        return theta

    def _get_proximity_gap_error(self) -> float:
        """
        Get the proximity gap error for the unique decoding regime.

        This is a direct application of Theorem 4.1 in the BCIKS20 paper: That is, what is the
        probability we sampled bad randomness when batching `self.num_polys` polynomials?
        """
        return (self.params.D * self.params.num_polys) / self.params.F

    def _get_FRI_commit_phase_error(self) -> float:
        """
        Finish up the commit phase soundness error calculation for the UDR.

        This function computes the error by taking the union bound over multiple folding rounds, and the probability that the verifier samples bad randomness during FRI folding. See Paul's hackmd for more details.
        """
        fri_folding_errors = ((self.params.D + 1) * (self.params.FRI_folding_factor - 1) * self.params.FRI_rounds_n) / self.params.F
        return self.e_proximity_gap + fri_folding_errors