from __future__ import annotations

import math

from .regime import Regime
from ..zkevms.zkevm import zkEVMParams
from typing import Any
from ..common.utils import get_proof_system_errors


class EthStarkRegime(Regime):
    """
    ethSTARK conjecture

    This is Regime 1 from the RISC0 Python calculator
    """

    def identifier(self) -> str:
        return "ethstark"

    def estimate(self, params: zkEVMParams) -> tuple[float, dict[str, Any]]:
        # Store for helper access consistency with other regimes
        self.params = params
        rho = params.rho

        # FRI errors under ethSTARK conjecture
        self.e_FRI_commit_phase = 1 / params.F
        self.e_FRI_query_phase = math.pow(rho, params.s)
        self.e_FRI_final = self.e_FRI_commit_phase + self.e_FRI_query_phase

        # Compute proof system errors, but ignore ALI/DEEP under ethSTARK conjecture
        (_, _, self.e_PLONK, self.e_PLOOKUP) = get_proof_system_errors(params.L, params)

        self.e_final = self.e_FRI_final + self.e_PLONK + self.e_PLOOKUP

        return self.gets_bits_of_security()

