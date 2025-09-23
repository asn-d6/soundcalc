from __future__ import annotations

from .regime import Regime
from ..zkevms.zkevm import zkEVMParams
from typing import Any
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

    def compute_security(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        self.params = params
        rho = params.rho

        theta = self._get_theta(rho)

        # Compute FRI errors
        self.e_proximity_gap = self._get_proximity_gap_error()
        self.e_FRI_commit_phase = self._get_FRI_commit_phase_error()

        self.e_FRI_query_phase = get_FRI_query_phase_error(theta, params.num_queries, params.grinding_query_phase)
        self.e_FRI_final = self.e_FRI_commit_phase + self.e_FRI_query_phase

        # For unique decoding, list size is naturally 1
        L_plus = 1

        # XXX might still need to do something with m_plus or rho_plus. See the hackmd.
        (self.e_ALI, self.e_DEEP, self.e_PLONK, self.e_PLOOKUP) = get_proof_system_errors(L_plus, params)

        self.e_final = self.e_FRI_final + self.e_ALI + self.e_DEEP + self.e_PLONK + self.e_PLOOKUP

        return self.gets_bits_of_security_from_error()

    def _get_theta(self, rho: float) -> float:
        """
        Compute theta for the unique decoding regime.
        """
        # XXX (BW): I think theta = UDR = (1-rho)/2 is correct. Not sure what the alpha does.
        alpha = 1 - (1 - rho) / 2  # XXX factcheck whether the "1 - " is correct here
        theta = 1 - alpha
        return theta

    def _get_proximity_gap_error(self) -> float:
        """
        Get the proximity gap error for the unique decoding regime.

        This is a direct application of Theorem 4.1 in the BCIKS20 paper: That is, what is the
        probability we sampled bad randomness when batching `self.num_polys` polynomials?
        """
        # XXX (BW) if I read Theorem 4.1 correctly, then num_polys should only play a role if we do
        # batching with randomness r^0, r^1, ..., r^(num_polys -1), but then we should point to
        # Theorem 1.5. If randomness is r_1 = 1, r_2, ... , r_num_polys, it should not play a role.
        return (self.params.D * self.params.num_polys) / self.params.F

    def _get_FRI_commit_phase_error(self) -> float:
        """
        Commit phase error for the Unique Decoding Regime (UDR).

        This function computes the error by taking the union bound over multiple folding rounds, and the probability that
        the verifier samples bad randomness during FRI folding. See Paul's hackmd for more details.

        Note: This function is used only in the UDR regime.
        """
        e_proximity_gap = self.e_proximity_gap
        D = self.params.D
        FRI_folding_factor = self.params.FRI_folding_factor
        FRI_rounds_n = self.params.FRI_rounds_n
        F = self.params.F

        # XXX (BW) 1: I think the FRI_rounds_n should not play a role here, as RO queries are domain-separated
        # XXX (BW) 2: why is it `D+1` and not `D`? In prox gaps paper the error in UDR is just domain size / field size
        fri_folding_errors = ((D + 1) * (FRI_folding_factor - 1) * FRI_rounds_n) / F
        return e_proximity_gap + fri_folding_errors
