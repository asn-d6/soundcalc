from __future__ import annotations

from .regime import Regime
from ..zkevms.zkevm import zkEVMParams
from soundcalc.common.fri import get_FRI_query_phase_error
from ..common.utils import get_rho_plus, get_proof_system_errors
import math

class UniqueDecodingRegime(Regime):
    """
    Unique decoding regime (UDR)

    This is Regime 4 from the RISC0 Python calculator
    """

    def identifier(self) -> str:
        return "unique_decoding"

    def estimate(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        self.params = params
        rho = params.rho

        alpha, theta = self._get_alpha_theta(rho)

        # Compute FRI error components
        # XXX Is this sufficient for the commit phase in the UDR?
        self.e_proximity_gap = self._get_proximity_gap_error(rho)
        self.e_FRI_commit_phase = self.e_proximity_gap

        self.e_FRI_query_phase = get_FRI_query_phase_error(theta, params.s)
        self.e_FRI_final = self.e_FRI_commit_phase + self.e_FRI_query_phase

        # For unique decoding, list size is naturally 1
        L_plus = 1

        (self.e_ALI, self.e_DEEP, self.e_PLONK, self.e_PLOOKUP) = get_proof_system_errors(L_plus, params)

        self.e_final = self.e_FRI_final + self.e_ALI + self.e_DEEP + self.e_PLONK + self.e_PLOOKUP

        return self.gets_bits_of_security()

    def _get_alpha_theta(self, rho: float) -> tuple[float, float]:
        """
        Compute alpha and theta for unique decoding regime.
        """
        alpha = 1 - (1 - rho) / 2  # XXX factcheck whether the "1 - " is correct here
        theta = 1 - alpha
        return alpha, theta

    def _get_proximity_gap_error(self, rho: float) -> float:
        """
        Get the proximity gap error for the unique decoding regime.
        This is the error of the commit phase of FRI as computed by the correlated agreement theorem in BCIKS20.
        """
        return (self.params.D + 1) * (self.params.L + (self.params.FRI_folding_factor - 1) * self.params.FRI_rounds_n) / self.params.F



