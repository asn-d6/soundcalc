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
        Return theta for the unique decoding regime.
        """
        theta = (1 - rho) / 2
        return theta

    def _get_proximity_gap_error(self) -> float:
        """
        Get the proximity gap error for the unique decoding regime.

        This is a direct application of Theorem 4.1 in the BCIKS20 paper: That is, what is the
        probability we sampled bad randomness when batching `self.num_polys` polynomials?
        """

        # Note: the errors for correlated agreement in the following two cases differ,
        # which is related to the batching method:
        #
        # Case 1: we batch with randomness r^0, r^1, ..., r^{num_polys-1}
        # This is what is called batching over parameterized curves in BCIKS20.
        # Here, the error depends on num_polys (called l in BCIKS20), and we find
        # the error in Theorem 6.1 and Theorem 1.5.
        #
        # Case 2: we batch with randomness r_0 = 1, r_1, r_2, r_{num_polys-1}
        # This is what is called batching over affine spaces in BCIKS20.
        # Here, the error does not depend on num_polys (called l in BCIKS20), and we find
        # the error in Theorem 1.6.
        #
        # Then easiest way to see the difference is to compare Theorems 1.5 and 1.6.

        error = self.params.num_polys / self.params.F
        if self.params.power_batching:
            error *= self.params.num_polys
        return error

    def _get_FRI_commit_phase_error(self) -> float:
        """
        Commit phase error for the Unique Decoding Regime (UDR).

        This function computes the error by taking the union bound over multiple folding rounds, and the probability that
        the verifier samples bad randomness during FRI folding. See Paul's hackmd for more details.

        Note: This function is used only in the UDR regime.
        """
        D = self.params.D
        FRI_folding_factor = self.params.FRI_folding_factor
        FRI_rounds_n = self.params.FRI_rounds_n
        F = self.params.F

        # XXX (BW) 1: I think the FRI_rounds_n should not play a role here, as RO queries are domain-separated
        fri_folding_errors = (D * (FRI_folding_factor - 1) * FRI_rounds_n) / F
        return self.e_proximity_gap + fri_folding_errors
