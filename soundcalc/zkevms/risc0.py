from __future__ import annotations

from .zkevm import zkEVMConfig, zkEVMParams
from ..common.fields import *


class Risc0Preset:
    @staticmethod
    def default() -> "Risc0Preset":
        """
        Populate a zkEVMConfig instance with zkVM parameters.

        For RISC0, we use the ones in https://github.com/risc0/risc0/blob/ebc18c770c4dd5a8e8dfdca1297edb181848405f/risc0/zkp/src/docs/soundness.ipynb
        (dated September 2024)
        Also, see section 3.2 from the RISC0 proof system technical report:
           https://dev.risczero.com/proof-system-in-detail.pdf

        Thanks a lot to Paul Gafni for helping out!
        """

        hash_size_bits = 256 # TODO: check if that is actually true

        rho = 1 / 4.0
        trace_length = 1 << 21

        field = BABYBEAR_4

        num_control = 16
        num_data = 223
        num_accum = 40
        C = num_control + num_data + num_accum
        L = C + 4
        s = 50
        max_combo = 9
        AIR_max_degree = 4 #They use 5 but in the DEEP-ALI error they use (d-1) so we put 4 here.

        FRI_folding_factor = 16
        FRI_early_stop_degree = 2**8

        # according to https://dev.risczero.com/proof-system-in-detail.pdf Sections C.6 and 3.4
        # Risc0 uses batching with coefficients r^0, r^1, r^2, ...
        power_batching = True

        cfg = zkEVMConfig(
            name="risc0",
            hash_size_bits=hash_size_bits,
            rho=rho,
            trace_length=trace_length,
            field=field,
            num_columns=C,
            num_polys=L,
            power_batching=power_batching,
            num_queries=s,
            max_combo=max_combo,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
            grinding_query_phase=0,
            AIR_max_degree=AIR_max_degree,
        )
        return zkEVMParams(cfg)
