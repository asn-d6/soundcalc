from __future__ import annotations

from .zkevm import zkEVMConfig, zkEVMParams
from ..common.fields import GOLDILOCKS_2


class MidenPreset:
    @staticmethod
    def default() -> "MidenPreset":
        # Parameters based on get_100_bits_security() in
        #   https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs
        # TODO Not sure if this is the actual parameters used in prod.

        # blowup_factor = 4 => rho = 1/4
        rho = 1 / (1 << 2)
        # trace_length = 2^18
        H = 1 << 18

        FRI_folding_factor = 2
        #  "let fri_remainder_max_degree = 127;"
        FRI_early_stop_degree = 2**7

        field = GOLDILOCKS_2

        # num_constraints =  100
        C = 100

        # num_committed_polys = 2 ???
        L = 2

        # num_queries = 119
        s = 119  # num_queries

        # XXX ???
        max_combo = 2

        cfg = zkEVMConfig(
            name="miden",
            rho=rho,
            H=H,
            field=field,
            C=C,
            L=L,
            s=s,
            max_combo=max_combo,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
        )
        return zkEVMParams(cfg)


