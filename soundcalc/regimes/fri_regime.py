from __future__ import annotations

import math
from typing import Optional, Dict, Any

from soundcalc.common.fri import get_FRI_query_phase_error
from soundcalc.common.utils import get_bits_of_security_from_error

from ..zkevms.zkevm import zkEVMParams


class FRIRegime:
    """
    A class representing a regime for FRI analysis. Soundcalc supports four regimes:
    - Unique Decoding Regime (UDR)
    - List Decoding up to Johnson Bound (JBR),
    - List Decoding up to Capacity Bound (CBR).
    Code for those regimes can be found in files across this directory.
    """

    def identifier(self) -> str:
        raise NotImplementedError


    def get_bound_on_list_size(self, params: zkEVMParams) -> int:
        """
        Returns an upper bound on the list size of this regime, i.e., the number of codewords
        a function is close to. For instance, this is 1 for the unique decoding regime.
        """
        raise NotImplementedError

    def get_theta(self, params: zkEVMParams) -> float:
        """
        Returns the theta for the query phase error.
        """
        raise NotImplementedError

    def get_batching_error(self, params: zkEVMParams) -> float:
        """
        Returns the error for the FRI batching step for this regime.
        """
        raise NotImplementedError

    def get_commit_phase_error(self, params: zkEVMParams) -> float:
        """
        Returns the error for the FRI commit phase for this regime.
        """
        raise NotImplementedError

    def get_rbr_levels(self, params: zkEVMParams) -> dict[str, int]:
        """
        Returns a dictionary that contains the round-by-round soundness levels.
        It maps from a label that explains which round it is for to an integer.
        If this integer is, say, k, then it means the error for this round is at
        most 2^{-k}.
        """
        bits = {}

        # Compute FRI errors for batching
        bits["FRI batching round"] = get_bits_of_security_from_error(self.get_batching_error(params))

        # Compute FRI error for folding / commit phase
        FRI_rounds = params.FRI_rounds_n
        for i in range(FRI_rounds):
            bits[f"FRI commit round {i+1}"] = get_bits_of_security_from_error(self.get_commit_phase_error(params))

        # Compute FRI error for query phase
        theta = self.get_theta(params)
        bits["FRI query phase"] = get_bits_of_security_from_error(get_FRI_query_phase_error(theta, params.num_queries, params.grinding_query_phase))

        return bits
