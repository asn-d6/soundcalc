from __future__ import annotations

from soundcalc.zkvms.whir_based_vm import WHIRBasedVM, WHIRBasedVMConfig


from ..common.fields import *


class DummyWHIRPreset:
    @staticmethod
    def default() -> "DummyWHIR":
        """
        A dummy zkVM using WHIR for testing WHIR
        """

        name = "DummyWHIR"
        hash_size_bits = 256
        log_inv_rate = 1 # rate 1/2
        num_iterations = 3
        folding_factor = 2
        field = GOLDILOCKS_3
        log_degree = 20
        constraint_degree = 1
        num_queries = [10,5]
        num_ood_samples = [2,2]


        cfg = WHIRBasedVMConfig(
            name=name,
            hash_size_bits=hash_size_bits,
            log_inv_rate=log_inv_rate,
            num_iterations=num_iterations,
            folding_factor=folding_factor,
            field=field,
            log_degree=log_degree,
            constraint_degree=constraint_degree,
            num_queries=num_queries,
            num_ood_samples=num_ood_samples
        )
        return WHIRBasedVM(cfg)
