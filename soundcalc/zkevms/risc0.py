from __future__ import annotations

from .zkevm import zkEVMConfig, zkEVMParams
from ..common.fields import *


class Risc0Preset:
    @staticmethod
    def default() -> "Risc0Preset":
        """
        Populate a zkEVMConfig instance with zkVM parameters.

        For RISC0, we use the ones in https://github.com/risc0/risc0/blob/main/risc0/zkp/src/docs/soundness.ipynb
        Also, see section 3.2 from the RISC0 proof system technical report:
           https://dev.risczero.com/proof-system-in-detail.pdf
        """
        rho = 1 / 4.0
        H = 1 << 21

        field = BABYBEAR_4

        num_control = 16
        num_data = 223
        num_accum = 40
        C = num_control + num_data + num_accum
        L = C + 4
        s = 50
        max_combo = 9

        FRI_folding_factor = 16
        FRI_early_stop_degree = 2**8

        cfg = zkEVMConfig(
            name="risc0",
            rho=rho,
            H=H,
            field=field,
            C=C,
            L=L,
            s=s,
            max_combo=max_combo,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
            grinding_query_phase=0,
        )
        return zkEVMParams(cfg)


