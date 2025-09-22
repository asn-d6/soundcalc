from __future__ import annotations

import math


from .regime import Regime
from ..zkevms.zkevm import zkEVMParams
from soundcalc.common.fri import get_johnson_parameter_m, get_FRI_soundness_error
from ..common.utils import get_rho_plus, get_proof_system_errors

class CapacityBoundRegime(Regime):
    """
    List decoding up to Capacity Bound Regime (CBR)

    This is Regime 3 from the RISC0 python calculator.
    This is a conjectured regime.
    """

    def identifier(self) -> str:
        return "capacity_bound"

    def estimate(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        self.params = params
        rho = params.rho

        # Default conjecture parameters
        c_1 = 1.0
        c_2 = 1.0
        c_3 = 1.0  # controls the list size

        # This is called epsilon in the RISC0 calculator, but it's usually eta elsewhere
        # It denotes how close we are to the capacity bound
        eta = 0.05

        m = get_johnson_parameter_m()

        # Compute theta for this regime
        theta = 1 - rho - eta

        # Compute the FRI error
        self.e_proximity_gap = self._get_proximity_gap_error(c_1, c_2, eta, rho)
        self.e_FRI_final, self.e_FRI_commit_phase, self.e_FRI_query_phase = get_FRI_soundness_error(
            params, self.e_proximity_gap, theta, m
        )

        # Compute list size under this regime
        L_plus = self._get_list_size(theta, c_3)

        # Compute remaining proof system errors
        (self.e_ALI, self.e_DEEP, self.e_PLONK, self.e_PLOOKUP) = get_proof_system_errors(L_plus, params)

        self.e_final = self.e_FRI_final + self.e_ALI + self.e_DEEP + self.e_PLONK + self.e_PLOOKUP

        return self.gets_bits_of_security()

    def _get_list_size(self, theta: float, C_rho: float) -> int:
        """
        Get list size for the capacity bound regime.
        This is conjectured (e.g. see Conjecture 5.6 in the STIR paper)
        """
        # ASN This computation is again kinda different between Ha22 and STIR conjecture.
        # Clarify and document why we are using this one.
        r_plus = get_rho_plus(self.params.H, self.params.D, self.params.max_combo)
        assert theta < 1 - r_plus
        eta_plus = 1 - r_plus - theta

        return math.ceil((self.params.D / eta_plus) ** C_rho)

    def _get_proximity_gap_error(self, c_1: float, c_2: float, eta: float, rho: float) -> float:
        """
        Get the proximity gap error for the capacity bound regime.
        This is the second item of Conjecture 8.4 in the BCIKS20 paper.
        """
        return 1 / ((eta * rho) ** c_1) * self.params.L * (self.params.D ** c_2) / self.params.F

