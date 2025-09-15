from __future__ import annotations

from .zkevm import zkEVMConfig, zkEVMParams
from ..common.fields import BABYBEAR_4


class Risc0Preset:
    @staticmethod
    def default() -> "Risc0Preset":
        # See parameters in https://github.com/risc0/risc0/blob/main/risc0/zkp/src/docs/soundness.ipynb
        rho = 1 / (1 << 2)
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
        )
        return zkEVMParams(cfg)


