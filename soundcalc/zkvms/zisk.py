from __future__ import annotations

from soundcalc.zkvms.fri_based_vm import FRIBasedVM, FRIBasedVMConfig

from ..common.fields import *


class ZiskPreset:
    @staticmethod
    def default() -> "ZiskPreset":
        """
        Populate a zkEVMConfig instance with zkVM parameters.

        For ZisK, we populate the trace parameters from its constraint description:
            https://github.com/0xPolygonHermez/zisk/blob/main/pil/zisk.pil

        The rest of the parameters are adapted from the "eSTARK: Extending STARKs with Arguments" paper:
           https://eprint.iacr.org/2023/474
        """

        field = GOLDILOCKS_3

        # We generate a STARK proof of different traces with different parameters.
        # Therefore, in what follows, I put the parameters for our worst-case trace in terms of area.

        # The blowup factor is dinamically chosen by this tool:
        #       https://github.com/0xPolygonHermez/pil2-proofman-js/blob/main/src/pil2-stark/pil_info/imPolsCalculation/imPolynomials.js#L96
        # by chosing the one (greater or equal than 2) that yields the lowest number of columns.
        # Here we just fix it to 2 for simplicity.
        blowup_factor = 2
        rho = 1 / blowup_factor

        trace_length = 1 << 22
        num_columns = 66
        num_polys = num_columns + 2 # +2 for the composition polynomials

        num_queries = 128 // int(math.log2(blowup_factor))

        AIR_max_degree = blowup_factor + 1

        FRI_folding_factor = 2**4
        FRI_early_stop_degree = 2**5

        max_combo = 3

        hash_size_bits = 256 # TODO: check if that is actually true

        cfg = FRIBasedVMConfig(
            name="ZisK",
            hash_size_bits=hash_size_bits,
            rho=rho,
            trace_length=trace_length,
            field=field,
            num_columns=num_columns,
            num_polys=num_polys,
            power_batching=True,
            num_queries=num_queries,
            AIR_max_degree=AIR_max_degree,
            FRI_folding_factor=FRI_folding_factor,
            FRI_early_stop_degree=FRI_early_stop_degree,
            max_combo=max_combo,
            grinding_query_phase=0,
        )
        return FRIBasedVM(cfg)
