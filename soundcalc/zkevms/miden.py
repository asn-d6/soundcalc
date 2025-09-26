from __future__ import annotations

from .zkevm import zkEVMConfig, zkEVMParams
from ..common.fields import *


class MidenPreset:
    @staticmethod
    def default() -> "MidenPreset":
        """
        Populate a zkEVMConfig instance with zkVM parameters.

        For Miden, we use the parameters from the `RECURSIVE_96_BITS` configuration in:
            https://github.com/0xMiden/miden-vm/blob/fde5256c7ea99112e7dc2677b4c57ad824f63dcb/air/src/options.rs#L47C15-L47C32

        Parts of the Miden proof system are described in the "STARK-based Signatures from the RPO Permutation" paper:
            https://eprint.iacr.org/2024/1553

        Thanks a lot to Al Kindi for the help!
        """

        # TODO Not sure if this is the actual parameters used in prod.

        # blowup_factor = 8 => rho = 1/8
        rho = 1 / 8.0

        grinding_query_phase = 16

        num_queries = 27

        FRI_folding_factor = 4
        # The Miden code uses 127 (likely for internal reasons) but we use a power of 2
        FRI_early_stop_degree = 2**7

        field = GOLDILOCKS_2

        # XXX That's actually inferred from the tests in
        #    https://github.com/facebook/winterfell/blob/main/air/src/proof/security.rs
        # Might be inaccurate?
        trace_length = 1 << 18    #note that this is smaller than for other VMs, thus the security is higher for the same settings
        # XXX need to check the numbers below by running the prover
        num_columns = 100
        num_polys = 100

        # XXX ???  TODO: ask the main Miden channel
        max_combo = 2

        cfg = zkEVMConfig(
            name="miden",
            rho=rho,
            trace_length=trace_length,
            field=field,
            num_columns=num_columns,
            num_polys=num_polys,
            num_queries=num_queries,
            max_combo=max_combo,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
            grinding_query_phase=grinding_query_phase,
        )
        return zkEVMParams(cfg)


